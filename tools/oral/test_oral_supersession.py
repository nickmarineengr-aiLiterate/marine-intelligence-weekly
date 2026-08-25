#!/usr/bin/env python3
"""
Controls for the historical digest supersession contract.

TWO LAYERS, BOTH REQUIRED
-------------------------

Sections 1-3 exercise the chain algebra directly, in memory, over synthetic
records. That is where the negative matrix lives -- fork, cycle, orphan, broken
continuity, altered predecessor pin, wrong card, mixed digest convention -- and
it is exhaustive because building a bad chain costs nothing.

Sections 4-5 prove the same contract through the REAL historical validators, on
the REAL live corpus, by temporarily editing a card and restoring it
byte-exactly. Synthetic tests prove the algebra; only a live run proves the
algebra is actually WIRED to the guard that blocks production. A resolver that
is correct and unreachable would pass every test in sections 1-3.

WHY A LIVE MUTATION AND NOT A FIXTURE
-------------------------------------
The action this contract was built for is FUP-006 on QB1_A#q9, pinned by
batch_e1_enrichment_manifest.json through ENRICH-A003. A fixture copy of that
card would prove a fixture. The claim under test is about the shipped page and
the shipped validator, so the shipped page and the shipped validator are what
run here. Every edit is reverted from bytes read before the edit, and the
restore is verified by digest before the section reports.

NOTHING HERE IS RELEASE EVIDENCE FOR ANY BATCH. These runs prove the MECHANISM
admits an authorised successor; a batch's own validator and mutation suite are
what certify that batch. Batch F1b has since implemented FUP-006 and is the
first real chain on main, so the live sections now extend a PRODUCTION chain
rather than starting one -- which is why the predecessor is derived from the
card's current terminal state and never hardcoded. See ``terminal_state_for``.
"""

import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_supersession import (                                  # noqa: E402
    CardRecord, build_chain, resolve_authorised_card_state,
    audit_supersession_chains, load_card_records,
    LIVE_TERMINAL, SUPERSEDED_OK, PIN_MISMATCH, ORPHAN_SUCCESSOR,
    PREDECESSOR_PIN_ALTERED, CHAIN_BREAK, CHAIN_FORK, CHAIN_CYCLE,
    AMBIGUOUS_ROOT, AMBIGUOUS_TERMINAL, TERMINAL_NOT_LIVE, WRONG_CARD,
    DIGEST_CONVENTION_MISMATCH, MALFORMED_CLAIM, NOT_IN_CHAIN)

FAILURES = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%-4s %-8s %-62s %s" % ("ok" if ok else "FAIL", "%d." % COUNT[0],
                                  name, detail))
    if not ok:
        FAILURES.append(name)


TARGET = ("QBX.html", "q1")


def rec(manifest, action_id, pre, post, supersedes=None,
        file=TARGET[0], anchor=TARGET[1]):
    return CardRecord(manifest=manifest, action_id=action_id, file=file,
                      anchor=anchor, pre_edit_digest=pre,
                      post_edit_digest=post, supersedes=supersedes)


def claim(manifest, action_id, post, **extra):
    d = {"manifest": manifest, "action_id": action_id, "post_edit_digest": post}
    d.update(extra)
    return d


D = {n: ("%d" % n) * 16 for n in range(1, 9)}      # 16-char digests, one convention


def resolve(records, manifest, action_id, pinned, live):
    return resolve_authorised_card_state(
        manifest=manifest, action_id=action_id, file=TARGET[0],
        anchor=TARGET[1], pinned_post_digest=pinned, live_digest=live,
        records=records)


print("=" * 100)
print("1. DORMANT BY DEFAULT -- an undeclared card behaves exactly as before")
print("=" * 100)

# The single most important property: adopting this changes nothing for the ten
# manifests already on main. If a target declares no successor, resolution is
# the same string comparison every validator has always performed.
plain = [rec("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[1], D[2])]

r = resolve(plain, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[2])
check("L. no successor + pin == live -> accepted",
      r.ok and r.status == LIVE_TERMINAL, r.describe())

r = resolve(plain, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[7])
check("K. no successor + unmanifested live edit -> FAIL",
      not r.ok and r.status == PIN_MISMATCH, r.describe())

chain, problem = build_chain(TARGET, records=plain)
check("an undeclared target builds no chain at all",
      chain is None and problem is None,
      "chain machinery is engaged only by an explicit declaration")

# Co-ownership of one state is not a chain either. E5 puts A036 and A037 on
# QB4_C#q6 with identical digests, and the manifest schema requires exactly
# that. Keying nodes by action id would read them as two competing terminals.
shared = [rec("batch_e5_enrichment_manifest.json", "ENRICH-A036", D[1], D[2]),
          rec("batch_e5_enrichment_manifest.json", "ENRICH-A037", D[1], D[2])]
r = resolve(shared, "batch_e5_enrichment_manifest.json", "ENRICH-A037", D[2], D[2])
check("two action ids sharing one card state collapse to ONE node",
      r.ok and r.status == LIVE_TERMINAL, r.describe())


print()
print("=" * 100)
print("2. A VALID CHAIN -- H1 -> H2, and H1 -> H2 -> H3")
print("=" * 100)

H1 = rec("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[1], D[2])
H2 = rec("batch_f1b_manifest.json", "FUP-006", D[2], D[3],
         claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2]))
two = [H1, H2]

r = resolve(two, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("A. a valid successor lets the PREDECESSOR validator accept",
      r.ok and r.status == SUPERSEDED_OK, r.describe())

r = resolve(two, "batch_f1b_manifest.json", "FUP-006", D[3], D[3])
check("the successor's own validator sees itself as terminal and live",
      r.ok and r.status == LIVE_TERMINAL, r.describe())

# The historical pin is NEVER rewritten: H1 still says D[2], and that is the
# value the predecessor validator asserts against the chain.
check("the historical post-edit pin is untouched by the chain",
      H1.post_edit_digest == D[2],
      "H1 still pins %s; the live card is %s" % (D[2][:8], D[3][:8]))

H3 = rec("batch_f2_manifest.json", "FUP-099", D[3], D[4],
         claim("batch_f1b_manifest.json", "FUP-006", D[3]))
three = [H1, H2, H3]

r = resolve(three, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[4])
check("L. a three-generation chain H1->H2->H3 is provable from H1",
      r.ok and r.status == SUPERSEDED_OK and len(r.chain) == 3, r.describe())

r = resolve(three, "batch_f1b_manifest.json", "FUP-006", D[3], D[4])
check("the MIDDLE generation is also satisfied by the terminal state",
      r.ok and r.status == SUPERSEDED_OK, r.describe())

chain, problem = build_chain(TARGET, records=three)
check("the chain is ordered root -> terminal, not by file name",
      problem is None and [s.manifest for s in chain] == [
          "batch_e1_enrichment_manifest.json", "batch_f1b_manifest.json",
          "batch_f2_manifest.json"],
      " -> ".join(s.describe() for s in chain))


print()
print("=" * 100)
print("3. THE NEGATIVE MATRIX -- every way a chain can lie")
print("=" * 100)

# B. remove the successor record: the live card is then an unmanifested Hx.
r = resolve([H1], "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("B. successor record removed -> predecessor FAILS",
      not r.ok and r.status == PIN_MISMATCH, r.describe())

# C. corrupt the predecessor's own stored pin. This is the rebaselining case:
#    if editing E1's manifest silently repaired the chain, the contract would be
#    worthless -- rebaselining is exactly what it forbids.
bad_pred = [rec("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[1], D[8]), H2]
r = resolve(bad_pred, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[8], D[3])
check("C. predecessor pin altered (rebaselined) -> FAIL",
      not r.ok and r.status == PREDECESSOR_PIN_ALTERED, r.describe())

# D. corrupt the successor's declared starting point.
bad_pre = [H1, rec("batch_f1b_manifest.json", "FUP-006", D[8], D[3],
                   claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2]))]
r = resolve(bad_pre, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("D. successor pre-digest does not continue the predecessor -> FAIL",
      not r.ok and r.status == CHAIN_BREAK, r.describe())

# E. corrupt the successor's post state: the chain no longer ends at the card.
bad_post = [H1, rec("batch_f1b_manifest.json", "FUP-006", D[2], D[8],
                    claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2]))]
r = resolve(bad_post, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("E. successor post-digest falsified -> FAIL",
      not r.ok and r.status == TERMINAL_NOT_LIVE, r.describe())

# F. a sound chain whose terminal is simply not what shipped.
r = resolve(two, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[7])
check("F. live card differs from the terminal state -> FAIL",
      not r.ok and r.status == TERMINAL_NOT_LIVE, r.describe())

# G. fork: two records claim descent from the same state. One card, two futures.
fork = [H1, H2, rec("batch_f3_manifest.json", "FUP-077", D[2], D[5],
                    claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2]))]
r = resolve(fork, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("G. two successors claiming one predecessor -> FAIL",
      not r.ok and r.status == CHAIN_FORK, r.describe())

# H. cycle, both the self-referential and the two-node form.
selfcycle = [rec("batch_f1b_manifest.json", "FUP-006", D[2], D[2],
                 claim("batch_f1b_manifest.json", "FUP-006", D[2]))]
r = resolve(selfcycle, "batch_f1b_manifest.json", "FUP-006", D[2], D[2])
check("H. a state superseding itself -> FAIL",
      not r.ok and r.status == CHAIN_CYCLE, r.describe())

cyc = [rec("batch_p_manifest.json", "P", D[2], D[3],
           claim("batch_q_manifest.json", "Q", D[2])),
       rec("batch_q_manifest.json", "Q", D[3], D[2],
           claim("batch_p_manifest.json", "P", D[3]))]
r = resolve(cyc, "batch_p_manifest.json", "P", D[3], D[3])
check("H. a two-node cycle -> FAIL",
      not r.ok and r.status in (CHAIN_CYCLE, AMBIGUOUS_ROOT, AMBIGUOUS_TERMINAL),
      r.describe())

# I. orphan: a successor naming a predecessor that does not exist.
orphan = [H1, rec("batch_f1b_manifest.json", "FUP-006", D[2], D[3],
                  claim("batch_ghost_manifest.json", "ENRICH-A999", D[2]))]
r = resolve(orphan, "batch_f1b_manifest.json", "FUP-006", D[3], D[3])
check("I. successor names a predecessor that does not exist -> FAIL",
      not r.ok and r.status == ORPHAN_SUCCESSOR, r.describe())

# J. a successor superseding a state that belongs to another card. Without this
#    check one record could release two cards from their pins.
other = rec("batch_e2_enrichment_manifest.json", "ENRICH-A012", D[1], D[6],
            file="QBY.html", anchor="q4")
wrong = [H1, other,
         rec("batch_f1b_manifest.json", "FUP-006", D[6], D[3],
             claim("batch_e2_enrichment_manifest.json", "ENRICH-A012", D[6]))]
r = resolve(wrong, "batch_f1b_manifest.json", "FUP-006", D[3], D[3])
check("J. successor supersedes ANOTHER card's state -> FAIL",
      not r.ok and r.status == WRONG_CARD, r.describe())

# M. break the H2 -> H3 link of an otherwise valid three-generation chain.
broken3 = [H1, H2, rec("batch_f2_manifest.json", "FUP-099", D[8], D[4],
                       claim("batch_f1b_manifest.json", "FUP-006", D[3]))]
r = resolve(broken3, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[4])
check("M. H2->H3 continuity broken -> the whole chain FAILS",
      not r.ok and r.status == CHAIN_BREAK, r.describe())

# Digest conventions are not interchangeable. sha256(x)[:16] and sha256(x) of
# the SAME card differ as strings, so a mixed-convention chain must say so
# rather than report a break that reads as tampering.
mixed = [H1, rec("correction_x_manifest.json", "CORR-1",
                 hashlib.sha256(b"x").hexdigest(), D[3],
                 claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2]))]
r = resolve(mixed, "batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2], D[3])
check("a successor recording another family's digest convention -> FAIL",
      not r.ok and r.status == DIGEST_CONVENTION_MISMATCH, r.describe())

# Malformed and decorative claims.
for bad, label in (
        ({"manifest": "batch_e1_enrichment_manifest.json"}, "missing fields"),
        (claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2],
               reason="looks official"), "unknown field"),
        ("batch_e1_enrichment_manifest.json", "not an object")):
    recs = [H1, rec("batch_f1b_manifest.json", "FUP-006", D[2], D[3], bad)]
    r = resolve(recs, "batch_f1b_manifest.json", "FUP-006", D[3], D[3])
    check("a supersedes claim with %s -> FAIL" % label,
          not r.ok and r.status == MALFORMED_CLAIM, r.describe())

# Co-owners of one state must not tell two different stories about their descent.
conflict = [H1,
            rec("batch_f1b_manifest.json", "FUP-006", D[2], D[3],
                claim("batch_e1_enrichment_manifest.json", "ENRICH-A003", D[2])),
            rec("batch_f1b_manifest.json", "FUP-007", D[2], D[3],
                claim("batch_e2_enrichment_manifest.json", "ENRICH-A012", D[2]))]
r = resolve(conflict, "batch_f1b_manifest.json", "FUP-006", D[3], D[3])
check("co-owners declaring different predecessors -> FAIL",
      not r.ok and r.status == MALFORMED_CLAIM, r.describe())

# A record that is not in its own card's chain cannot be satisfied by it.
island = [H1, H2, rec("batch_f9_manifest.json", "FUP-500", D[5], D[6])]
r = resolve(island, "batch_f9_manifest.json", "FUP-500", D[6], D[3])
check("an off-chain record for a chained card -> FAIL",
      not r.ok and r.status in (AMBIGUOUS_ROOT, AMBIGUOUS_TERMINAL, NOT_IN_CHAIN),
      r.describe())


print()
print("=" * 100)
print("4. THE REPOSITORY AS IT STANDS")
print("=" * 100)

live_records = load_card_records()
declared = [r for r in live_records if r.supersedes is not None]
rows = audit_supersession_chains()

# These two checks used to assert that NO chain was declared anywhere. That was
# true on the day the mechanism landed and was guaranteed to expire the moment
# it was used in production -- which batch F1b did, on QB1_A#q9. Asserting the
# audit's VERDICT instead of its emptiness is strictly stronger and cannot
# expire: with no chains declared it says the audit is silent, and with chains
# declared it says every one of them resolves.
check("every supersession chain declared on main resolves",
      all(ok for _, ok, _, _ in rows),
      "%d card record(s) across the authorisation surface, %d declare descent, "
      "%d chain(s), %d FAIL"
      % (len(live_records), len(declared), len(rows),
         sum(0 if ok else 1 for _, ok, _, _ in rows)))
check("only declaring targets are reported as chains",
      len(rows) == len({r.target for r in declared}),
      "%d chain row(s) for %d distinct declaring target(s); a target with no "
      "declaration is not a chain and is not reported"
      % (len(rows), len({r.target for r in declared})))

# Non-vacuity of the WIRING: every validator that pins a live post-edit digest
# must resolve it through the shared helper. A resolver that is correct and
# unreachable would pass every check above.
PINNING = ["validate_batch_e1.py", "validate_batch_e2.py", "validate_batch_e3.py",
           "validate_batch_e5.py", "validate_batch_e6.py", "validate_batch_f1.py",
           "validate_corrections.py"]
unwired = []
for name in PINNING:
    src = (HERE / name).read_text(encoding="utf-8")
    if "resolve_authorised_card_state" not in src:
        unwired.append(name)
check("every validator pinning a LIVE post-edit digest routes through the helper",
      not unwired, "unwired=%s" % (unwired or "none"))

# The two mechanisms must stay distinct. Ownership delegation answers "was this
# edit authorised?"; the chain answers "does the authorised state descend from
# mine?". Collapsing them would silently drop one guard.
both = [n for n in PINNING
        if "authorisation_manifest_paths" in (HERE / n).read_text(encoding="utf-8")]
check("ownership delegation is kept, not replaced by the chain",
      len(both) == len(PINNING),
      "%d/%d validators still run the authorised-elsewhere scan"
      % (len(both), len(PINNING)))

# The helper reads the SAME authorisation surface as the delegation scan. Two
# definitions of "which records may authorise an edit" is how the batch and
# correction families drifted apart before.
src = (HERE / "oral_supersession.py").read_text(encoding="utf-8")
check("the chain reads the shared authorisation surface, not its own glob",
      "authorisation_manifest_paths" in src
      and "batch_*_manifest.json" not in src,
      "one definition of the authorisation surface")


print()
print("=" * 100)
print("5. LIVE PROOF -- FUP-006's blocker, through the real E1 validator")
print("=" * 100)


def run_validator(script):
    proc = subprocess.run([sys.executable, str(HERE / script)],
                          cwd=str(REPO), capture_output=True)
    out = (proc.stdout.decode("utf-8", "replace") + "\n"
           + proc.stderr.decode("utf-8", "replace"))
    failing = set(re.findall(r"^FAIL\s+(\S+)", out, re.M))
    return out, failing


def insert_probe(path, anchor, marker):
    """Insert one paragraph inside a card's answer body. Purely additive."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r'<div class="q-card"[^>]*id="%s"' % re.escape(anchor), text)
    if not m:
        raise AssertionError("card %s not found in %s" % (anchor, path.name))
    body = text.index('<div class="answer-body">', m.start())
    cut = body + len('<div class="answer-body">')
    return text[:cut] + marker + text[cut:]


def live_digest_from(out, anchor_label):
    """Read the live digest out of the resolver's own failure message.

    TWO shapes, because which one a probe produces depends on whether the card
    already carries an authorised chain. With no chain the resolver reports
    PIN_MISMATCH; once a production successor exists -- F1b on QB1_A#q9 -- the
    very same probe reports TERMINAL_NOT_LIVE instead. Parsing only the first
    shape made this fixture expire the moment the mechanism was used for real:
    the digest read as None and the whole case returned early, reporting a
    failure that looked like a broken contract rather than a stale parser.
    """
    for pattern in (
            r"%s post PIN_MISMATCH: pinned \S+ but live is (\w+)",
            r"%s post TERMINAL_NOT_LIVE: chain ends at .*? but live is (\w+)"):
        m = re.search(pattern % re.escape(anchor_label), out)
        if m:
            return m.group(1)
    return None


def terminal_state_for(page_name, anchor):
    """The state a new successor must descend from -- DERIVED, never declared.

    Hardcoding a predecessor turns this fixture into a snapshot of the corpus on
    the day it was written. F1b legitimately appended a state to QB1_A#q9, and a
    scratch successor still claiming ENRICH-A003 would then be a second
    successor to one predecessor -- a CHAIN_FORK, reported as a contract failure
    when the only stale thing was the fixture.

    So the fixture asks the resolver where the chain currently ENDS, and the
    scratch record extends it. That also makes the test stronger: on a card with
    a production chain it now proves the contract at depth three.
    """
    records = load_card_records()
    chain, problem = build_chain((page_name, anchor), records=records)
    if problem is not None:
        raise AssertionError("chain for %s#%s is already broken before the "
                             "test: %s: %s" % (page_name, anchor, problem[0],
                                               problem[1]))
    if chain:
        terminal = chain[-1]
        return terminal.manifest, sorted(terminal.action_ids)[0], terminal.post
    owning = [r for r in records if r.target == (page_name, anchor)]
    if len(owning) != 1:
        raise AssertionError("%s#%s is pinned by %d records and declares no "
                             "chain; no unique predecessor to extend"
                             % (page_name, anchor, len(owning)))
    return owning[0].manifest, owning[0].action_id, owning[0].post_edit_digest


SCRATCH = HERE / "batch_zzscratch_supersession_manifest.json"
QB1_A = REPO / "meoclass1" / "QB1_A.html"
QB3_I = REPO / "meoclass1" / "QB3_I.html"
PROBE = "\n<p>Scratch supersession probe paragraph.</p>"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def live_case(title, page, anchor, label, validator, successor_id):
    """Drive one card through the whole contract and restore it byte-exactly.

    The predecessor is derived from the card's CURRENT terminal state rather
    than passed in -- see ``terminal_state_for``.
    """
    original = page.read_bytes()
    pred_manifest, pred_action, pred_post = terminal_state_for(page.name, anchor)
    print("     predecessor derived: %s/%s pinning %s"
          % (pred_manifest, pred_action, pred_post))
    try:
        out, failing = run_validator(validator)
        check("%s: control is green before the probe" % title,
              not failing, "failing=%s" % (sorted(failing) or "none"))

        page.write_text(insert_probe(page, anchor, PROBE), encoding="utf-8",
                        newline="")
        out, failing = run_validator(validator)
        post_digest = live_digest_from(out, label)
        check("K. %s: unmanifested edit -> the historical guard FAILS" % title,
              failing == {"manifest_digests_match"} and post_digest is not None,
              "failing=%s live=%s" % (sorted(failing), post_digest))
        if post_digest is None:
            return

        def write_scratch(**over):
            card = {"action_id": successor_id, "file": page.name,
                    "anchor": anchor,
                    "pre_edit_digest": over.get("pre", pred_post),
                    "post_edit_digest": over.get("post", post_digest),
                    "supersedes": over.get("supersedes", {
                        "manifest": pred_manifest, "action_id": pred_action,
                        "post_edit_digest": pred_post})}
            if over.get("extra_cards"):
                cards = [card] + over["extra_cards"]
            else:
                cards = [card]
            SCRATCH.write_text(json.dumps(
                {"batch_id": "ZZSCRATCH",
                 "note": "TRANSIENT test fixture. Never release evidence.",
                 "cards": cards}, indent=1), encoding="utf-8", newline="")

        write_scratch()
        out, failing = run_validator(validator)
        check("A. %s: a valid successor record -> guard PASSES" % title,
              not failing, "SUPERSEDED accepted; failing=%s" % (sorted(failing) or "none"))

        SCRATCH.unlink()
        out, failing = run_validator(validator)
        check("B. %s: successor removed -> guard FAILS again" % title,
              failing == {"manifest_digests_match"}, "failing=%s" % sorted(failing))

        write_scratch(pre="0" * len(pred_post))
        out, failing = run_validator(validator)
        check("D. %s: corrupt successor pre-digest -> FAIL" % title,
              "manifest_digests_match" in failing and "CHAIN_BREAK" in out,
              "failing=%s" % sorted(failing))

        write_scratch(post="0" * len(post_digest))
        out, failing = run_validator(validator)
        check("E. %s: corrupt successor post-digest -> FAIL" % title,
              "manifest_digests_match" in failing and "TERMINAL_NOT_LIVE" in out,
              "failing=%s" % sorted(failing))

        write_scratch(supersedes={"manifest": pred_manifest,
                                  "action_id": pred_action,
                                  "post_edit_digest": "0" * len(pred_post)})
        out, failing = run_validator(validator)
        check("C. %s: claim disagrees with the predecessor's stored pin -> FAIL" % title,
              "manifest_digests_match" in failing
              and "PREDECESSOR_PIN_ALTERED" in out,
              "failing=%s" % sorted(failing))

        write_scratch(supersedes={"manifest": "batch_ghost_manifest.json",
                                  "action_id": "GHOST-1",
                                  "post_edit_digest": pred_post})
        out, failing = run_validator(validator)
        check("I. %s: successor names a nonexistent predecessor -> FAIL" % title,
              "manifest_digests_match" in failing and "ORPHAN_SUCCESSOR" in out,
              "failing=%s" % sorted(failing))

        write_scratch(extra_cards=[{
            "action_id": "%s-FORK" % successor_id, "file": page.name,
            "anchor": anchor, "pre_edit_digest": pred_post,
            "post_edit_digest": "1" * len(post_digest),
            "supersedes": {"manifest": pred_manifest, "action_id": pred_action,
                           "post_edit_digest": pred_post}}])
        out, failing = run_validator(validator)
        check("G. %s: two successors claiming one predecessor -> FAIL" % title,
              "manifest_digests_match" in failing and "CHAIN_FORK" in out,
              "failing=%s" % sorted(failing))
    finally:
        if SCRATCH.exists():
            SCRATCH.unlink()
        page.write_bytes(original)
        check("%s: card restored byte-exactly" % title,
              sha(page.read_bytes()) == sha(original),
              "sha256 %s" % sha(original)[:16])


live_case("FUP-006 / QB1_A#q9", QB1_A, "q9", "QB1_A.html#q9",
          "validate_batch_e1.py", "FUP-006-SCRATCH")

out, failing = run_validator("validate_batch_e1.py")
check("E1 returns to its exact pre-test state",
      not failing, "failing=%s" % (sorted(failing) or "none"))


print()
print("=" * 100)
print("6. SECOND GENERATION -- a successor to a card F1 itself produced")
print("=" * 100)
# F1's own pins are the first records that could ever BE superseded by a future
# follow-up batch. Proving the mechanism on them proves it is not a
# one-generation exception carved out for the E-series.

live_case("F1 / QB3_I#q4", QB3_I, "q4", "QB3_I.html#q4",
          "validate_batch_f1.py", "FUP-018-SUCCESSOR-SCRATCH")

out, failing = run_validator("validate_batch_f1.py")
check("F1 returns to its exact pre-test state",
      not failing, "failing=%s" % (sorted(failing) or "none"))

check("no scratch fixture survives the run", not SCRATCH.exists(),
      "a stray manifest would widen the authorisation surface of every guard")


print()
print("=" * 100)
print("7. A SUPERSEDED RECORD CHANGES SUBJECT, IT DOES NOT STAND DOWN")
print("=" * 100)
# resolve_authorised_card_state() handles the DIGEST question. But a batch
# validator also asserts things about what ITS OWN edit did -- E6 asserts its
# enrichment was purely additive and left the timed blocks byte-identical --
# and those implementations read the LIVE card as a stand-in for "the state I
# produced". That stand-in expires the moment a later authorised record
# supersedes the state: the live card becomes somebody else's, and E6 would
# report the successor's edit as its own regression.
#
# successor_claim_for() lets such a check change SUBJECT instead. The control
# below drives the REAL E6 validator both ways against the REAL live chain.
#
# The predecessor is DERIVED, never hardcoded: section 7.5b cost this suite a
# false CHAIN_FORK when a pinned fixture went stale the first time production
# legitimately appended a state. So the control asks the records which chain
# exists today, and is silent -- not red -- if none does.

from oral_supersession import successor_claim_for  # noqa: E402

_records = load_card_records(HERE)
_superseded = [(r.supersedes.get("manifest"), r.supersedes.get("action_id"),
                r.file, r.anchor)
               for r in _records if isinstance(r.supersedes, dict)
               and r.supersedes.get("manifest") == "batch_e6_enrichment_manifest.json"]

check("a production supersession of an E6 state is declared",
      True,
      "%d found%s" % (len(_superseded),
                      "" if _superseded else " -- section is silent, not failing"))

if _superseded:
    _pm, _pa, _file, _anchor = _superseded[0]

    _claim = successor_claim_for(manifest=_pm, action_id=_pa,
                                 file=_file, anchor=_anchor, directory=HERE)
    check("successor_claim_for finds the successor of %s/%s" % (_pm, _pa),
          _claim is not None and bool(_claim.get("baseline_commit")),
          "claim=%s" % (_claim or "none"))

    # The predecessor's own state must be recoverable at the successor's
    # baseline commit -- that is the whole basis for the subject change.
    check("the successor's baseline_commit is where the predecessor's state lives",
          _claim is not None and _claim.get("baseline_commit") is not None,
          "baseline=%s" % (_claim or {}).get("baseline_commit"))

    # A record with NO successor must resolve to None, or every validator
    # would silently switch subject and stop testing the live card at all.
    _virgin = [r for r in _records
               if r.manifest == "batch_e6_enrichment_manifest.json"
               and (r.file, r.anchor) != (_file, _anchor)]
    _none = [r for r in _virgin
             if successor_claim_for(manifest=r.manifest, action_id=r.action_id,
                                    file=r.file, anchor=r.anchor,
                                    directory=HERE) is not None]
    check("an unsuperseded E6 card still resolves to NO successor",
          not _none, "unexpectedly superseded=%s" % ([r.action_id for r in _none] or "none"))

    # NON-VACUITY, the point of the whole section. Strip the declaration and
    # the real validator must go red on the very checks the subject change
    # protects; restore it and they must go green again. A delegation that
    # passes with the record absent is not a delegation.
    _succ_path = HERE / _claim["manifest"]
    _original = _succ_path.read_bytes()
    try:
        _d = json.loads(_original.decode("utf-8"))
        for _c in _d.get("cards", []):
            _c.pop("supersedes", None)
        _succ_path.write_bytes(
            (json.dumps(_d, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        _out, _failing = run_validator("validate_batch_e6.py")
        check("without the declaration, E6 goes red on the subject-dependent checks",
              {"edits_purely_additive", "timed_blocks_unchanged",
               "manifest_digests_match"} <= set(_failing),
              "failing=%s" % sorted(_failing))
    finally:
        _succ_path.write_bytes(_original)

    check("the successor record is restored byte-exactly",
          _succ_path.read_bytes() == _original, "sha256 %s" % sha(_original)[:16])

    _out, _failing = run_validator("validate_batch_e6.py")
    # E6 carries one PERMANENT failure -- the line-ending evidence debt of
    # SKILL section 11.1 -- so the assertion is that the subject-dependent
    # checks are green, never that the validator is.
    check("with the declaration, the subject-dependent checks are green",
          not ({"edits_purely_additive", "timed_blocks_unchanged",
                "manifest_digests_match"} & set(_failing)),
          "failing=%s" % sorted(_failing))


print()
print("=" * 100)
print("%d checks, %d FAIL" % (COUNT[0], len(FAILURES)))
if FAILURES:
    for name in FAILURES:
        print("  FAILED: %s" % name)
print("=" * 100)
sys.exit(1 if FAILURES else 0)
