# Laptop independent review — Question Intelligence v2, Phase 3A.1

**Reviewer** Laptop, Claude Code Opus 5 · **Date** 2026-08-18
**Question** Is QI-v2 safe, portable and deterministic enough to scale into dated
historical ingestion?

**Verdict** **HOLD — one final bounded repair.**

Thirteen of the fourteen Phase-3A.1 claims are independently confirmed. One is
not: portability is real, but it is **not load-bearing**. Removing the committed
bank extract silently disables the headline Phase-3A.1 repair and the validator
still exits 0.

---

## A. Repo truth

| | SHA |
|---|---|
| `main` = `origin/main` = HEAD | `3b55bfb` |
| `origin/research/question-intelligence-v2-phase3a` | `893912d` |
| `origin/review/question-intelligence-v2-phase3a` (prior) | `286c0c5` |
| this review | `review/question-intelligence-v2-phase3a1` |

All three matched the brief. Working tree clean; nothing merged.

## B. Scope

`git diff origin/main...893912d` — **37 files added, 7,885 insertions, 0
modifications, 0 deletions.** Desktop's report said 36 / 7,772; the difference is
the last commit (`893912d`, the repair register) landing after the report was
written. Not a discrepancy of substance.

Every path is research-owned (`intelligence/v2/**`, `sources/official/dgshipping/`).
**Zero** changes under `specs/`, `solvedQP`, `SQ`, payment, entitlements, refund,
homepage or magazine. No candidate or commercial contamination.

## C. Portability — CONFIRMED, but see R-1

Review ran from a worktree on **C:**, a different drive from the F: canonical
repo, so any absolute-path assumption fails loudly rather than resolving by luck.

- Repository-wide search for drive letters, usernames and absolute roots across
  `intelligence/v2/`: **zero executable references.** The only `D:` occurrence is
  the docstring in `tools/qi_paths.py` describing the closed defect — acceptable.
- `qi_paths.py` derives every path from `__file__`; all four consumers import it.
- Bank extract: **53,194 bytes, 185 items, sha256
  `ba841f9a98c49ffbd15599481b2d62dd3b56b2cdc0a6dc43ecb83b6252bb9f8c`, zero CRLF**
  despite `core.autocrlf=true`, because `.gitattributes` pins `*.json` to LF.
  This is the trap that has bitten content-hashed assets before; it holds here.

## D/E/F. Reproduction from the clean worktree

Every Desktop number reproduced exactly, first try, no local artefacts:

| Harness | Desktop | Laptop |
|---|---|---|
| `validate_families.py` | 200 checks / 0 skips / 0 failures | **identical** |
| `validate_families.py --mutate` | 39 mutations / 0 escapes | **identical** |
| `adversarial_controls.py` | 38 controls / 0 failures | **identical** |
| `adversarial_controls.py --mutate` | 9 mutations / 0 escapes | **identical** |
| `match_bank_to_corpus.py` | 45 exact/near, 37 same-core, 82 reportable | **identical** |
| QP2608 Paper DNA | 48/144 = 33.3%; 58/144 = 40.3% | **identical** |

---

## R-1 — BLOCKING. Portability is not load-bearing.

**Section 6 of the review brief is explicit:** remove the committed bank extract
and validation must fail loudly — *not* skip, warn and continue, or silently
reduce the check count. It does all three.

```
$ mv sources/official/dgshipping/dgs_meo_cl1_bank_items.json /tmp/
$ python validate_families.py
  extract     : ABSENT - two checks skipped
  checks run  : 170
  SKIPPED     : 5
    ~ C32 curated bank text matches the 185-item extract
    ~ C33 the (Oct-05) annotation is derived, not remembered
    ~ C40 occurrence ancestors lie within the family declaration
    ~ C41 the family representative fits its declared ancestor
    ~ C42 no undeclared bank item fits the family better
  FAILURES    : 0
EXITCODE=0
```

C40/C41/C42 **are the Phase-3A.1 headline repair** — the semantic
wrong-but-valid-ancestor guard built to close the Laptop LC-3 finding. Deleting
one file switches them off, drops the check count 200 to 170, and reports success.

The skip branch was *correct* in Phase 3A, when the extract genuinely lived
outside the repository. Phase 3A.1 committed the extract but left the fallback
in place, which inverts its meaning: what used to say "this machine lacks the
intake" now says "someone removed the evidence", and the validator answers that
with exit 0. The stale banner — "two checks skipped" when five skip — confirms
the path was not revisited after C40 to C42 were added.

**Repair (small, one function):** the extract is now tracked. Its absence is a
tampering or checkout failure, not an environment difference. `load_extracted_bank()`
should raise, or `validate()` should register a hard failure, and the five
`rep.skip` calls should become `rep.check(..., False, ...)`. Keep an explicit
`--allow-missing-extract` escape hatch if a genuine use case exists, but the
default must fail. Then re-run `--mutate` to prove the new check fires.

## R-2 — Recommended in the same repair. Numeric dimension gaps.

Claim 6 ("decimal / technical numbers are load-bearing") is **substantially**
true — my own pairs for sulphur %, ppm, volts, years, degrees C and minutes all
raise a conflict and correctly cap the pair at `SAME_CORE_ASK`, below exact/near.

But `_UNIT_OF` has no FORCE, VISCOSITY, TONNAGE, NAUTICAL-DISTANCE or MICRON
dimension, and a bare integer above 20 with no recognised unit is dropped
entirely. The Founder's own section 13 list exposes this:

| pair | conflict |
|---|---|
| `2.2 kN` vs `4.4 kN` | True — but only because they are *decimals*, not because kN is understood |
| **`70 N` vs `100 N`** | **False** — both extract to `[]` |
| `380 cSt` vs `180 cSt` (fuel viscosity) | False |
| `50000 dwt` vs `70000 dwt` | False |
| `200` vs `500 nautical miles` | False |
| `25 microns` vs `10 microns` | False |

The last row reproduces, with a different unit, the *exact* asymmetry the
`numbers()` docstring says Phase 3A.1 fixed: `25 microns` gives `[]` but
`10 microns` gives `[('COUNT','10')]`, because 10 happens to fall in the 1-20
window. The conflict test requires both sides non-empty, so it stays silent.

This does not mis-classify anything in the corpus today — the 96-row sweep is
unchanged. It matters **because we are about to scale**: a missed numeric
conflict lets a pair reach `NEAR_VERBATIM`/`EXACT_REPEAT` that should not, which
is a false recurrence claim, and recurrence is the product. Adding the five
dimensions is a few lines in one table.

## R-3 — Note only, no action required.

`_MARKS` strips any parenthesised 1-3 digit number **before** unit detection, so
`operate within (30) seconds` extracts nothing where `within 30 seconds` extracts
`TIME_SECOND 30`. Real exam stems rarely parenthesise a quantity, and the
adjacent case `No. (4) unit` is *correctly* suppressed twice over — `no.` is also
an instrument-number prefix, and "No. 4 unit" is a designator, not a magnitude.
The section 14 requirement is met in the cases that occur; recording the edge for
completeness.

---

## G-N. Model verification

**G. Single classifier** — `tools/qi_similarity.py` is the only file in the
pastpapers tree defining `classify`, `demand_compatibility` or
`_containment_class`. The other three tools import it. No rival.

**H. Multi-demand `max()`** — genuinely fixed, verified by reading the
implementation and by behaviour, not by grepping for absence.
`demand_compatibility` splits primary command from secondary task and combines
with `min()`. The old `_demand_compat_max` survives *only* behind
`opts.demand_aggregate_max`, reachable solely from the mutation table, and
restoring it breaks P31-D1.

**I. Describe vs criticise** — my fresh pairs, none copied from Desktop fixtures:

| case | demand | class |
|---|---|---|
| describe vs critically evaluate CE bunkering responsibilities | 0.25 | `TOPIC_ONLY` |
| outline vs justify blackout actions | 0.40 | `TOPIC_ONLY` |
| compare vs calculate propulsion merits | 0.10 | `TOPIC_ONLY` |
| identical enclosed-space procedure (control) | 1.00 | `EXACT_REPEAT` |
| list vs explain crankcase causes | 0.40 | `UNSCOREABLE_SHORT_STEM` |
| discuss advantages vs state disadvantages | 0.35 | `UNSCOREABLE_SHORT_STEM` |
| explain surveyor vs explain CE responsibilities | 1.00 | `UNSCOREABLE_SHORT_STEM` |

Semantically sound throughout. Three of my cases hit the short-stem floor rather
than the demand model, which is the conservative outcome — the classifier
declines to score rather than guessing. Correct posture before scale.

**J. Negation** — load-bearing and it does not over-fire. Six polarity pairs
(required/not required, permitted/prohibited, shall/shall not, with/without
approval, may/may not, allowed/not allowed) all raise `requirement_conflict` and
cap at `TOPIC_ONLY`. Critically, my incidental-negation control —
*"...for a passenger ship, not including cargo ships"* vs the same stem without
the clause — correctly stays `SAME_CORE_ASK`. Not every "not" is catastrophic.

**K/L. Numeric semantics and mark exclusion** — see R-2/R-3. Mark allocations are
correctly excluded: `(4)` vs `(6)` and `[4 marks]` vs `[6 marks]` on an otherwise
identical stem both stay `EXACT_REPEAT`.

**M/N. Bank ancestors — five independent corruptions, none from Desktop's tables:**

| corruption | result |
|---|---|
| primary ancestor `BANK-160` to `BANK-054` (valid, wrong) | **CAUGHT** — C40, C41, C42 |
| declared secondary `BANK-085` to `BANK-018` (valid, undeclared) | **CAUGHT** — C40, C42 |
| control: untouched tree with legitimate secondary ancestor | **PASSES** (0 failures) |
| representative stem replaced by another family's real stem | **CAUGHT** — C41, C42, C43 |
| occurrence repointed to a different real question id | **CAUGHT** — C7, C8, C43 |

C42 is the strong one and it does the real work: a swapped-in item cannot outrank
the item the family actually descends from. Secondary ancestors are supported in
**both** directions — the declared `FAMILY-EM-0004` to `BANK-085` passes
untouched, an undeclared substitute fails.

## O-X. Data and documentary checks

**O. Item 182** — coherent (Bill of Lading / charter survey). **Item 181** still
preserves the genuine DGS `a, b, d, c` ordering typo. **P. Oct-05** attaches to
BANK-3 (dry-docking fire); C33 derives rather than remembers it. Zero U+FFFD
replacement characters across all 185 items.

**Q/R. EM-0008 / EM-0009** — consistent across all seven artefacts that name them.
`FAMILY-EM-0008` = unseaworthy vessels = `BANK-160`; `FAMILY-EM-0009` = casualty =
`BANK-039`. Both corrections are disclosed in place rather than quietly rewritten,
and `QUESTION_FAMILIES.json` carries the renumbering note. C44 is mutation-proven:
re-labelling a section with another family id, and giving a worked example another
family's sitting months, are both caught.

**S. MSA 2025** — S.O. 1244(E), notified 10 March 2026, commenced 15 March 2026,
s.324(1) repeal structure quoted verbatim. Matches the standing project record.

**T. Coastal Shipping Act 2025** — the omission I raised is properly added, and
handled better than asked: commencement is explicitly **not asserted**, and the
document goes further by flagging that its own MSA/CSA interlock statement
"becomes wrong the moment the CSA's commencement is notified." No unsupported
commencement is implied anywhere.

**U. Part XIV** — disambiguated, with a naming convention adopted in section 5B:
1958 Part XIV is *Control of Indian Ships and Coasting Trade*; 2025 Part XIV is
*Offences and Penalties*. No bare ambiguous usage remains in the research layer.

**V. W-1 / W-2** — both re-verified against the live files and both accurately
described. `oralnotes/miw-notes-mgmt-p15.html:432` does say the 2025 Act repeals
the 1958 Act "(retaining only limited savings under Part XIV)", which mis-describes
a substantive Part as a transitional one. `QB9_E.html:642` is as quoted.
**Nothing candidate-facing was edited by Desktop or by this review.**

**W. Dated filenames** — H1-H5 are now subject-based. A sweep of all v2 paths for
`2010-2012`, `JUN`, `MAR`, `APR`, `OCT`, `DEC` returns one hit:
`H4_QP2608_Q4_MARINE_INSURANCE.md`, where `MAR` is inside `MARINE`. No unsupported
date survives in a filename. C45 is mutation-proven.

**X. Date-evidence model** — all five date-derivation mutations still caught
(bank-only ancestor promoted to HIGH; bank-only given a date; advanced to
DATE_VERIFIED; a prior sitting rested on the bank alone; dated sources stripped).

## Y-AD. Metrics and posture

**Y/Z.** 45 exact/near and 37 same-core recomputed independently — identical, not
preserved artificially. **AA.** QP2608 Paper DNA 33.3% / 40.3%, whole/limb
double-counting prevented, parent inheritance intact. **AB.** 2010-2012 remains
unsupported; DGS Wayback not reopened; no candidate date publication. **AC.**
Prototypes have not regressed — the bank-only Type B block reads "IN THE OFFICIAL
QUESTION BANK" and nothing else, behind an explicit forbidden-phrase table
covering *asked before*, any year or month, frequency, *due again*, *revival*,
*dormant*, *last seen*. **AD.** Answer-impact enum stays internal; no
implementation, nothing candidate-facing.

## AE-AG. Founder decisions

**AE. Company / Administration actors — DEFER TO PHASE 3B.** Agreeing with the
default and with Desktop's restraint. Actor is load-bearing now; adding taxonomy
members changes classification behaviour, and a hardening pass is the wrong place
to do that. Expand only from adjudicated cases that ingestion actually produces.

**AF. EXPLAIN vs LIST — ACCEPT CURRENT CALIBRATION.** It is context-dependent:
"list the causes" and "explain the causes" ask for the same *content* but
different *depth*, and depth is what a Class I answer is marked on. My independent
run scored 0.40 and the pair did not reach `SAME_CORE_ASK`. Do not tune a number
upward because it feels low — before scale, under-claiming recurrence costs far
less than over-claiming it. Revisit only if ingestion surfaces real pairs where
the conservative call is demonstrably wrong.

**AG. Coastal Shipping commencement — accept `COMMENCEMENT_UNVERIFIED`.** I did
not independently locate primary commencement authority and did not broaden the
search. Force is not inferred from enactment. This does not block scaling: the
temporal prototype rests on the MSA's 15 March 2026 commencement, which *is*
pinned.

## AH-AL. Status

Clean-worktree proof: cross-drive, no Desktop intake, no untracked artefacts, no
manual copies — every headline number reproduced. Candidate-facing status
**NOT PUBLISHED** (C23 fails any `CANDIDATE_PUBLISHED` family unconditionally;
nothing is even `DATE_VERIFIED`). Bullet Exam Plan, commercial/payment code and
magazine work all **untouched** — confirmed by the diff, not by assertion.

## AM. Research integration

**Option A — Phase 3A.1 remains branch-only; Phase 3B proceeds on top of it,
after R-1.** Minimum irreversible change. Merging buys nothing while QI is
research-only, and holding the branch keeps a clean revert if ingestion reshapes
the model. Revisit merging when historical ingestion stabilises the schema.

## AN. Phase 3B authorisation — NOT YET

Blocked on R-1 only. That is a small repair in one function plus a mutation to
prove it. Once the validator fails loudly on a missing extract — and, strongly
recommended, once R-2's five dimensions are added — Phase 3B is authorised on the
scope below, which I reviewed and accept as written: statutory mapping, the 12
official dated DGS Class-I files from 2013-2015, hashed provenance, question
extraction, dated-sitting-to-bank-ancestor linking, occurrence/family expansion,
Paper DNA recomputation, temporal deltas where current-law comparison helps, and
**no candidate publication**. Phase 3B must not become UI work.

## AO. Next action

Desktop: repair R-1 (and R-2) on `research/question-intelligence-v2-phase3a`,
re-run all four harnesses plus a new mutation proving a missing extract fails,
and hand back for a short confirmatory check. Do not begin ingestion first.
