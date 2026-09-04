#!/usr/bin/env python3
"""
GPT REVIEW PASS 3 -- independent audit of the ``_same_convention`` widening.

WHAT WAS CHANGED, AND WHY IT NEEDS ITS OWN AUDIT
------------------------------------------------

Pass 2B widened ``oral_supersession._same_convention``:

    OLD   two digests are comparable IFF ``len(a) == len(b)``
          compared with ``a == b``

    NEW   two digests are comparable IFF ``len(a) == len(b)``
          OR one is 16 characters and the other is 64
          compared with ``_digests_agree`` -- equality on the COMMON PREFIX

That is a governance predicate shared by every generation-2 validator, and it
was widened in the same pass that needed the widening.  "The tests still pass"
is not evidence: the tests that pass are the ones written before the change
plus the ones written to justify it.  This file is the adversarial half --
every way the new rule could be too permissive, asked directly.

THE CLAIM UNDER TEST
--------------------

The widening is narrow.  Specifically:

    * only 16 and 64 are accepted widths -- 32, 20, 8, 0 are not;
    * a 16-character digest matches a 64 only when it IS that 64's prefix;
    * two DIFFERENT digests never become equivalent, at any width;
    * prefix agreement alone is not enough -- the predecessor must own the
      same card, and must still pin what the successor says it pins;
    * the widening is LOAD-BEARING, not decorative: the real E5 chain does
      not resolve without it, and does not resolve without the authorised
      correction record either.

The last clause is why section 4 runs the OLD predicate against the REAL
digest pair.  A widening that the corpus does not actually need would be an
unjustified weakening however well it tests.

NOTHING HERE MUTATES THE REPOSITORY.  Sections 1-3 are synthetic records in
memory.  Sections 4-6 READ the real manifests and the real live page and then
filter the record list in memory -- no manifest is edited, moved or deleted,
so this file is safe to run beside anything.
"""

import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_supersession import (                                     # noqa: E402
    CardRecord, build_chain, load_card_records,
    resolve_authorised_card_state, _same_convention, _digests_agree,
    LIVE_TERMINAL, SUPERSEDED_OK, PIN_MISMATCH, CHAIN_BREAK, WRONG_CARD,
    DIGEST_CONVENTION_MISMATCH, PREDECESSOR_PIN_ALTERED, ORPHAN_SUCCESSOR,
    AMBIGUOUS_ROOT, CHAIN_FORK)
from validate_batch_b import card_digests                           # noqa: E402

COUNT = [0]
FAILURES = []


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%-6s %-72s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILURES.append(name)


def section(title):
    print("\n" + "=" * 110)
    print(title)
    print("=" * 110)


def old_same_convention(a, b):
    """The pre-Pass-2B predicate, kept here so the widening can be measured."""
    return isinstance(a, str) and isinstance(b, str) and len(a) == len(b)


# Two real, unrelated 64-character digests from the live corpus, used as the
# raw material for every synthetic case.  Real values rather than "a"*64 so a
# prefix collision cannot be an artefact of the fixture.
X = hashlib.sha256(b"card-X").hexdigest()
Y = hashlib.sha256(b"card-Y").hexdigest()
Z = hashlib.sha256(b"card-Z").hexdigest()
TARGET = ("QB_FIXTURE.html", "q1")


def rec(manifest, aid, pre, post, supersedes=None, target=TARGET):
    return CardRecord(manifest=manifest, action_id=aid,
                      file=target[0], anchor=target[1],
                      pre_edit_digest=pre, post_edit_digest=post,
                      supersedes=supersedes)


def chain_status(records, target=TARGET):
    chain, problem = build_chain(target, records=records)
    return (None if problem is None else problem[0]), chain, problem


def two_link(pred_post, succ_pre, claim_post=None, pred_pre=None):
    """A minimal two-state chain: root -> successor."""
    claim = {"manifest": "root_manifest.json", "action_id": "ROOT-01",
             "post_edit_digest": pred_post if claim_post is None else claim_post}
    return [
        rec("root_manifest.json", "ROOT-01", pred_pre or X[:16], pred_post),
        rec("successor_manifest.json", "SUCC-01", succ_pre, Z, claim),
    ]


# =============================================================================
section("1. THE PREDICATE ITSELF -- every width, in isolation")
# =============================================================================

check("1  same 64 <-> same 64 is comparable", _same_convention(X, X), "64/64")
check("1  same 16 <-> same 16 is comparable", _same_convention(X[:16], X[:16]),
      "16/16")
check("2  16 <-> 64 is comparable (the widening)",
      _same_convention(X[:16], X) and _same_convention(X, X[:16]),
      "both orders")
check("5  32 <-> 64 is NOT comparable", not _same_convention(X[:32], X), "32/64")
check("5  32 <-> 16 is NOT comparable", not _same_convention(X[:32], X[:16]),
      "32/16")
for width in (8, 20, 40, 63, 65):
    check("5  %d <-> 64 is NOT comparable" % width,
          not _same_convention((X * 2)[:width], X), "%d/64" % width)
check("6  non-string is never comparable",
      not _same_convention(None, X) and not _same_convention(X, None)
      and not _same_convention(b"x" * 64, X) and not _same_convention(5, 5),
      "None, bytes, int all refused")
check("6  empty string against 64 is not comparable",
      not _same_convention("", X), "0/64")

# Comparison, once comparability is established.
check("1  identical 64s agree", _digests_agree(X, X), "X==X")
check("2  a 16 prefix agrees with its own 64", _digests_agree(X[:16], X), "prefix")
check("3  a 16 prefix does NOT agree with a different 64",
      not _digests_agree(X[:16], Y), "X[:16] vs Y")
check("4  two unrelated 16s do not agree",
      not _digests_agree(X[:16], Y[:16]), "X[:16] vs Y[:16]")
check("6  empty / None never agree",
      not _digests_agree("", X) and not _digests_agree(None, X)
      and not _digests_agree("", ""), "no vacuous agreement")
# The one property that makes prefix comparison safe at all.
check("   a one-character change at position 0 breaks agreement",
      not _digests_agree(("f" if X[0] != "f" else "0") + X[1:16], X),
      "single nibble flip caught")

# =============================================================================
section("2. THE PREDICATE INSIDE A CHAIN -- the same seven cases, end to end")
# =============================================================================

status, chain, problem = chain_status(two_link(X, X))
check("1  same 64 -> same 64 builds a chain", status is None and len(chain) == 2,
      "2 states")

status, chain, problem = chain_status(
    two_link(X[:16], X, claim_post=X[:16], pred_pre=Y[:16]))
check("2  a 64-char successor descends from a 16-char predecessor",
      status is None and len(chain) == 2, "16 -> 64 accepted")

status, _, problem = chain_status(
    two_link(X[:16], Y, claim_post=X[:16], pred_pre=Y[:16]))
check("3  a 64 that does NOT extend the 16 is a CHAIN_BREAK",
      status == CHAIN_BREAK, problem[1][:70] if problem else "-")

status, _, problem = chain_status(
    two_link(X[:16], Y[:16], claim_post=X[:16], pred_pre=Z[:16]))
check("4  two unrelated 16s are a CHAIN_BREAK", status == CHAIN_BREAK,
      problem[1][:70] if problem else "-")

status, _, problem = chain_status(two_link(X, X[:32]))
check("5  a 32-char successor is DIGEST_CONVENTION_MISMATCH",
      status == DIGEST_CONVENTION_MISMATCH, problem[1][:70] if problem else "-")

status, _, problem = chain_status(two_link(X, "zzzz" * 4))
check("6  a non-hex 16 does not agree with a 64 (fails closed)",
      status == CHAIN_BREAK, problem[1][:70] if problem else "-")

status, _, problem = chain_status(two_link(X, None))
check("6  a NULL pre-digest is DIGEST_CONVENTION_MISMATCH",
      status == DIGEST_CONVENTION_MISMATCH, problem[1][:70] if problem else "-")

# 7. correct prefix, WRONG CARD.  The predecessor action exists, pins exactly
#    what the claim says it pins, and the successor's pre-digest is a genuine
#    prefix of it -- everything the digest layer can see is correct.  It must
#    still fail, because the predecessor owns a different card.
other = ("QB_FIXTURE.html", "q2")
records = [
    rec("root_manifest.json", "ROOT-01", Y[:16], X, target=other),
    rec("successor_manifest.json", "SUCC-01", X[:16], Z,
        {"manifest": "root_manifest.json", "action_id": "ROOT-01",
         "post_edit_digest": X}),
]
status, _, problem = chain_status(records)
check("7  a genuine prefix on the WRONG CARD is refused", status == WRONG_CARD,
      problem[1][:70] if problem else "-")

# 7b. and a predecessor whose real pin no longer matches the claim.
records = [
    rec("root_manifest.json", "ROOT-01", Y[:16], X),
    rec("successor_manifest.json", "SUCC-01", Y[:16], Z,
        {"manifest": "root_manifest.json", "action_id": "ROOT-01",
         "post_edit_digest": Y}),
]
status, _, problem = chain_status(records)
check("7b a rebaselined predecessor pin is PREDECESSOR_PIN_ALTERED",
      status == PREDECESSOR_PIN_ALTERED, problem[1][:70] if problem else "-")

records = [
    rec("successor_manifest.json", "SUCC-01", X[:16], Z,
        {"manifest": "nowhere.json", "action_id": "GHOST-01",
         "post_edit_digest": X}),
]
status, _, problem = chain_status(records)
check("7c an invented predecessor is ORPHAN_SUCCESSOR", status == ORPHAN_SUCCESSOR,
      problem[1][:70] if problem else "-")

# =============================================================================
section("3. THE UNNAMED THIRD CHANGE -- digestless records skipped in _states_for")
# =============================================================================

# Pass 2B also stopped treating a record that pins NO post-digest and claims no
# descent as a chain state.  That is a widening too and it was not in the
# brief, so it is audited here rather than taken on trust.
gen1 = rec("batch_d_manifest.json", "PROMNEW-01", None, None)
records = two_link(X, X) + [gen1]
status, chain, problem = chain_status(records)
check("8  a digestless generation-1 record is not a phantom root",
      status is None and len(chain) == 2, "chain still 2 states")

# ...but a record that pins nothing AND claims descent is malformed, and must
# still fail loudly rather than be skipped.
liar = rec("batch_d_manifest.json", "PROMNEW-02", None, None,
           {"manifest": "root_manifest.json", "action_id": "ROOT-01",
            "post_edit_digest": X})
status, _, problem = chain_status(two_link(X, X) + [liar])
check("8  a digestless record that CLAIMS descent still fails",
      status is not None, "%s" % (status or "SILENTLY ACCEPTED"))

# and a second REAL root is still ambiguous -- the skip did not blanket-disable
# the AMBIGUOUS_ROOT guard.
extra_root = rec("other_manifest.json", "OTHER-01", Y[:16], Y)
status, _, problem = chain_status(two_link(X, X) + [extra_root])
check("8  a second PINNED root is still AMBIGUOUS_ROOT", status == AMBIGUOUS_ROOT,
      problem[1][:70] if problem else "-")

# =============================================================================
section("4. THE REAL CHAIN -- QB9_H#q4, E5 -> CORR-MSACT2B-GREEN-20260904")
# =============================================================================

LIVE = card_digests((REPO / "meoclass1" / "QB9_H.html")
                    .read_text(encoding="utf-8", newline=""))["q4"]
real = load_card_records(HERE)
q4 = [r for r in real if r.target == ("QB9_H.html", "q4")]
e5 = [r for r in q4 if r.manifest == "batch_e5_enrichment_manifest.json"]
corr = [r for r in q4 if r.manifest.startswith("correction_corr_msact2b_green")]

check("9  the real chain has exactly one E5 state and one correction state",
      len(e5) == 1 and len(corr) == 1,
      "%s / %s" % ([r.action_id for r in e5], [r.action_id for r in corr]))
check("9  E5 pins 16 characters and the correction pins 64",
      len(e5[0].post_edit_digest) == 16 and len(corr[0].pre_edit_digest) == 64,
      "%s... / %s..." % (e5[0].post_edit_digest, corr[0].pre_edit_digest[:16]))
check("9  the correction's 64-char pre-digest BEGINS with E5's 16",
      corr[0].pre_edit_digest.startswith(e5[0].post_edit_digest),
      "%s == %s" % (corr[0].pre_edit_digest[:16], e5[0].post_edit_digest))
check("9  the live page IS the correction's post state",
      LIVE == corr[0].post_edit_digest, "live %s..." % LIVE[:16])

res = resolve_authorised_card_state(
    manifest=e5[0].manifest, action_id=e5[0].action_id,
    file="QB9_H.html", anchor="q4",
    pinned_post_digest=e5[0].post_edit_digest, live_digest=LIVE, records=real)
check("8  E5's own pin resolves as SUPERSEDED against the live page",
      res.ok and res.status == SUPERSEDED_OK, res.describe()[:80])

res = resolve_authorised_card_state(
    manifest=corr[0].manifest, action_id=corr[0].action_id,
    file="QB9_H.html", anchor="q4",
    pinned_post_digest=corr[0].post_edit_digest, live_digest=LIVE, records=real)
check("8  the correction resolves as LIVE_TERMINAL",
      res.ok and res.status == LIVE_TERMINAL, res.describe()[:80])

# THE WIDENING IS LOAD-BEARING.  Under the old predicate, this real pair is
# not comparable at all -- which is the whole reason the record could not be
# written.  If this check ever reports "old rule also accepts", the widening
# has become unjustified and should be reverted.
check("   NON-VACUITY: the OLD width-equality rule REJECTS this real pair",
      not old_same_convention(corr[0].pre_edit_digest, e5[0].post_edit_digest),
      "16 vs 64 -- the exact wall CORR-MSACT2B-GREEN hit")

# =============================================================================
section("5. THE REAL CHAIN REFUSES A FABRICATED SUCCESSOR")
# =============================================================================

fake_pre = ("f" if LIVE[0] != "f" else "0") + LIVE[1:]
forged = rec("correction_corr_forged_20260904_manifest.json", "FORGED-01",
             fake_pre, hashlib.sha256(b"forged").hexdigest(),
             {"manifest": corr[0].manifest, "action_id": corr[0].action_id,
              "post_edit_digest": corr[0].post_edit_digest},
             target=("QB9_H.html", "q4"))
status, _, problem = chain_status(real + [forged], ("QB9_H.html", "q4"))
check("9  a forged successor whose pre-digest is off by ONE NIBBLE is refused",
      status == CHAIN_BREAK, problem[1][:70] if problem else "-")

# A forgery that gets the digests right but lies about which action it descends
# from is refused too.
forged2 = rec("correction_corr_forged_20260904_manifest.json", "FORGED-02",
              corr[0].post_edit_digest, hashlib.sha256(b"forged2").hexdigest(),
              {"manifest": corr[0].manifest, "action_id": corr[0].action_id,
               "post_edit_digest": e5[0].post_edit_digest},
              target=("QB9_H.html", "q4"))
status, _, problem = chain_status(real + [forged2], ("QB9_H.html", "q4"))
check("9  a forged successor misquoting the predecessor's pin is refused",
      status == PREDECESSOR_PIN_ALTERED, problem[1][:70] if problem else "-")

# TWO successors claiming ONE predecessor is two futures for one card, and the
# widening must not have made a fork resolvable just because both agree on a
# prefix. Both are given the predecessor's exact post state, so the ONLY thing
# that can reject them is the fork rule itself.
fork_a = rec("correction_corr_forkeda_20260904_manifest.json", "FORK-A",
             corr[0].post_edit_digest, hashlib.sha256(b"fa").hexdigest(),
             {"manifest": corr[0].manifest, "action_id": corr[0].action_id,
              "post_edit_digest": corr[0].post_edit_digest},
             target=("QB9_H.html", "q4"))
fork_b = rec("correction_corr_forkedb_20260904_manifest.json", "FORK-B",
             corr[0].post_edit_digest, hashlib.sha256(b"fb").hexdigest()[:16],
             {"manifest": corr[0].manifest, "action_id": corr[0].action_id,
              "post_edit_digest": corr[0].post_edit_digest},
             target=("QB9_H.html", "q4"))
status, _, problem = chain_status(real + [fork_a, fork_b], ("QB9_H.html", "q4"))
check("9  two successors claiming one predecessor is a CHAIN_FORK",
      status == CHAIN_FORK, problem[1][:70] if problem else "-")

# AND THE HONEST LIMIT, recorded rather than hidden. A successor that pins a
# 16-character TRUNCATION of the live digest does resolve: that is precisely
# what "16 and 64 are one function at two truncations" means, and it is the
# reach the widening bought. It is not a forgery capability -- writing such a
# record means committing a manifest, which validate_corrections then audits
# in the 64-character convention -- but it IS the boundary, so it is asserted
# here rather than left for a later reader to discover.
truncating = rec("correction_corr_truncating_20260904_manifest.json", "TRUNC-01",
                 corr[0].post_edit_digest, LIVE[:16],
                 {"manifest": corr[0].manifest, "action_id": corr[0].action_id,
                  "post_edit_digest": corr[0].post_edit_digest},
                 target=("QB9_H.html", "q4"))
status, chain, problem = chain_status(real + [truncating], ("QB9_H.html", "q4"))
check("   BOUNDARY: a successor pinning live[:16] DOES resolve (documented reach)",
      status is None and chain is not None and len(chain) == 3,
      "%s -- 16/64 interchange is the widening's whole purpose"
      % (status or "chain of %d" % (len(chain) if chain else 0)))

# =============================================================================
section("6. THE AUTHORISED RECORD IS LOAD-BEARING")
# =============================================================================

without = [r for r in real
           if not r.manifest.startswith("correction_corr_msact2b_green")]
res = resolve_authorised_card_state(
    manifest=e5[0].manifest, action_id=e5[0].action_id,
    file="QB9_H.html", anchor="q4",
    pinned_post_digest=e5[0].post_edit_digest, live_digest=LIVE,
    records=without)
check("10 without the correction record, E5 goes red (PIN_MISMATCH)",
      not res.ok and res.status == PIN_MISMATCH, res.describe()[:80])

status, chain, problem = chain_status(without, ("QB9_H.html", "q4"))
check("10 and no chain exists for the card at all",
      chain is None and problem is None, "dormant, as designed")

print()
print("=" * 110)
print("%d checks, %d FAIL" % (COUNT[0], len(FAILURES)))
if FAILURES:
    for name in FAILURES:
        print("  FAILED: %s" % name)
print("=" * 110)
sys.exit(1 if FAILURES else 0)
