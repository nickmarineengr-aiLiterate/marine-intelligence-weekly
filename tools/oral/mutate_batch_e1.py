"""Adversarial mutation harness for the E1 enrichment guard.

Each mutation breaks one property validate_batch_e1.py claims to hold, runs the
validator, and requires it to FAIL for the intended reason. A mutation that is
applied but not caught is an ESCAPE. A mutation whose write changed no bytes is
a NO-OP and is reported as such rather than silently counted as a pass - a
stale anchor that no longer matches silently no-ops, which is how a mutation
harness comes to certify a guard it never actually exercised.

Beyond the standard set, E1 carries the mutations its subject matter needs.
This is the first batch about standard-form contract wording and market
practice, where the wrong answer is not a missing token but a plausible
over-simplification:

  P    assert that P&I simply covers everything H&M does not. It is the single
       most common wrong answer about the collision split, it is forbidden by
       the batch brief by name, and no positive-token check can see it because
       every required token is still present.
  Q    relabel BARECON 2017 optional Part IV as a Hire/Purchase Agreement. That
       is the 2001 mechanism. Mixing the two editions is the exact contract-
       edition trap the brief warns about, and it reads perfectly plausibly.
  O/R/V/W  flatten a distinction while leaving every positive token intact -
       the BARECON edition contrast (A008), what the Insurance Act 2015
       actually abolished (A005), the attribution of maritime security to the
       MSC rather than the Legal Committee (A006), and the mass-versus-volume
       energy distinction (A010).
  S/X  break the ten-actions-on-nine-cards cardinality. Every earlier
       enrichment batch was one action per card, so this property has never
       been exercised before; without S and X, dropping ENRICH-A007 or
       ENRICH-A008 from the shared card could pass as arithmetic.
  U    revert one authorised card to its baseline. Deliberately aimed at
       QB5_J.html, the one CRLF file in the batch, so the harness also proves
       the guard's LF normalisation works in the direction that matters.
  N    falsify a recorded digest, so the manifest stops describing reality.
  T    edit a timed block on an authorised card. Enrichment is body-only; a
       15/60-second block that drifts is out of scope even on a card the batch
       legitimately owns.

Mutation C deliberately targets a card that NO manifest owns, which is what
proves the sibling-manifest delegation in validate_batch_e1.py is an exemption
rather than a hole: an unowned card must still fail. Ownership is asserted at
run time rather than trusted.

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
MANIFEST = TOOLS / "batch_e1_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e1.py"
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


def drop_key(action_id, key):
    def _f(text):
        d = json.loads(text)
        for c in d["cards"]:
            if c["action_id"] == action_id:
                c.pop(key, None)
        return json.dumps(d, indent=1, ensure_ascii=False)
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
                                if c["action_id"] != "ENRICH-A006"]},
                     indent=1, ensure_ascii=False),
                 "authorised_action_set"),

        Mutation("B", "point an action at the wrong target card (A005)",
                 MANIFEST,
                 lambda t: t.replace('"anchor": "q19"', '"anchor": "q18"', 1),
                 "authorised_targets"),

        Mutation("C", "modify a neighbouring card no manifest owns",
                 QB_DIR / UNOWNED[0],
                 sub_once(r'(<div class="q-card"[^>]*id="%s")' % UNOWNED[1],
                          r'\1 data-e1mut="1"'),
                 "only_authorised_cards_changed"),

        Mutation("D", "blank an added missing limb (A001 cross-liabilities)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace("Cross-liabilities basis of settlement",
                                     "Shared basis of settlement", 1),
                 "missing_limb_supplied"),

        Mutation("E", "inject an internal action id into candidate text",
                 QB_DIR / "QB1_A.html",
                 sub_once(r"(Collision Liability \(RDC\) Actually Works)",
                          r"\1 [ENRICH-A001]"),
                 "no_candidate_visible_metadata"),

        Mutation("F", "add a new q-card to a QB page",
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

        Mutation("H", "remove a required legal authority (A003 CMI Guidelines)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace(
                     "CMI Guidelines relating to General Average",
                     "adjusting guidelines", 1),
                 "required_authority_cited"),

        Mutation("I", "alter a target card's candidate question text (A009)",
                 QB_DIR / "QB2_B.html",
                 lambda t: t.replace("Explain the container shipping",
                                     "Explain the containerised shipping", 1),
                 "q_text_and_anchors_stable"),

        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 lambda t: t.replace('"expected_examiner_relationships": 960',
                                     '"expected_examiner_relationships": 961'),
                 "examiner_relationship_delta_zero"),

        Mutation("K", "delete baseline text from an authorised card (A001)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace(
                     "<li>Wilful misconduct of the assured</li>", "", 1),
                 "edits_purely_additive"),

        Mutation("L", "break manifest/consolidation identity (A001 priority)",
                 MANIFEST,
                 lambda t: t.replace('"priority": "E-P1"',
                                     '"priority": "E-P3"', 1),
                 "authorised_enrichment_disposition"),

        Mutation("M", "declare that this batch creates new cards",
                 MANIFEST,
                 lambda t: t.replace('"creates_new_cards": false',
                                     '"creates_new_cards": true'),
                 "manifest_declares_no_new_cards"),

        Mutation("N", "falsify a recorded post-edit digest in the manifest",
                 MANIFEST,
                 sub_once(r'"post_edit_digest": "[0-9a-f]{16}"',
                          '"post_edit_digest": "0000000000000000"'),
                 "manifest_digests_match"),

        Mutation("O", "flatten the BARECON edition contrast (A008)",
                 QB_DIR / "QB9_H.html",
                 lambda t: t.replace("BARECON 2017 changed this",
                                     "BARECON 2017 is comparable", 1),
                 "required_qualifiers_kept"),

        Mutation("P", "assert P&I covers everything H&M does not (A001)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace(
                     "So the P&amp;I side of a collision is the residual",
                     "P&amp;I covers everything not covered by H&amp;M. "
                     "So the P&amp;I side of a collision is the residual", 1),
                 "unsubstantiated_claims_absent"),

        Mutation("Q", "relabel BARECON 2017 Part IV as hire/purchase (A008)",
                 QB_DIR / "QB9_H.html",
                 lambda t: t.replace(
                     "<strong>Part IV is now a purchase option</strong>",
                     "<strong>Part IV is still the BARECON 2017 "
                     "Hire/Purchase Agreement</strong>", 1),
                 "unsubstantiated_claims_absent"),

        Mutation("R", "flatten what the Insurance Act 2015 abolished (A005)",
                 QB_DIR / "QB1_B.html",
                 lambda t: t.replace("was abolished", "was clarified", 1),
                 "required_qualifiers_kept"),

        Mutation("S", "drop the shared-target declaration (A007/A008)",
                 MANIFEST,
                 drop_key("ENRICH-A007", "shared_target_note"),
                 "shared_target_declared"),

        Mutation("T", "edit a timed block on an authorised card (A001)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace(
                     "ITC(H) is the standard London-market hull",
                     "ITC(H) is the standard London market hull", 1),
                 "timed_blocks_unchanged"),

        Mutation("U", "revert one authorised card to its baseline (A010, CRLF)",
                 QB_DIR / "QB5_J.html",
                 sub_once(r" *<h4>Why the Owner Argues an Alternative Fuel"
                          r".*?</ul>\r?\n", "", flags=re.S),
                 "every_authorised_card_changed"),

        Mutation("V", "credit the Legal Committee with maritime security (A006)",
                 QB_DIR / "QB1_G.html",
                 lambda t: t.replace("is not the Legal Committee",
                                     "is squarely the Legal Committee", 1),
                 "required_qualifiers_kept"),

        Mutation("W", "flatten the mass-versus-volume distinction (A010)",
                 QB_DIR / "QB5_J.html",
                 lambda t: t.replace("not a volumetric one",
                                     "also a volumetric one", 1),
                 "required_qualifiers_kept"),

        Mutation("X", "misstate the distinct target-card count",
                 MANIFEST,
                 lambda t: t.replace('"distinct_target_cards": 9',
                                     '"distinct_target_cards": 10'),
                 "action_and_target_cardinality"),

        # P injects the claim entity-encoded ("H&amp;M"), which is how these
        # pages actually spell it and how it escaped the first time. Y injects
        # the SAME claim with a bare ampersand. Both must be caught, or the
        # entity fix has merely moved the blind spot rather than closed it.
        Mutation("Y", "assert the same claim with a bare ampersand (A001)",
                 QB_DIR / "QB1_A.html",
                 lambda t: t.replace(
                     "So the P&amp;I side of a collision is the residual",
                     "P&I covers everything not covered by H&M. "
                     "So the P&amp;I side of a collision is the residual", 1),
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
        print("  %-2s %-58s %s" % (k, d, v))

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
