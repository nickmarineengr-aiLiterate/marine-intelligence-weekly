# Oral follow-up production — batch F1

**Date:** 21 August 2026
**Baseline:** `67842df` (clean, `HEAD == main == origin/main`)
**Authorisation:** `tools/oral/oral_followup_register.json` (committed, 35 actions)
**Production record:** `tools/oral/batch_f1_manifest.json`

F1 is the first production batch derived from the committed follow-up
authorisation register rather than from the enrichment consolidation.

| | |
|---|---|
| Authorised | FUP-006, FUP-018, FUP-033 |
| Implemented | **FUP-018, FUP-033** |
| Held | **FUP-006** — `HELD_GOVERNANCE`, not a content or target problem |
| Retargeted | none |
| Canonical questions | 721, unchanged |
| Question-bearing files | 86, unchanged |
| New canonical cards | 0 |

---

## 1. What was implemented

### FUP-018 — `QB3_I#q4`, EXPECTED_DETAIL, examiner John

> *"Hydrogel - why barnacles not attaching?"*

**Live recheck: PARTIALLY_COVERED.** The card already set up the mechanism
generically — *"marine organisms rely on biological adhesives requiring a solid
substrate"* — but never delivered the barnacle-specific step the examiner
pushed for. That is precisely the `EXPECTED_DETAIL` semantic, so the limb was
placed as a deeper section of the parent answer rather than as a new card.

**The answer.** Barnacles settle as **cyprids**, and the cyprid's cement is laid
down in two phases: a hydrophobic **lipid** phase first, which displaces water
from the interface and leaves a locally dry footprint, and only then the
**phosphoprotein** cement that bonds to the substrate. A hydrogel defeats phase
one — its water is *bound into* the polymer network rather than resting on it —
so the cement never reaches a solid substrate and settlement fails at the cyprid
stage. The hydrogel is not toxic and is not slippery; it denies the barnacle the
dry footing its own adhesive chemistry requires.

**Authority.** Gohad *et al.*, *Nature Communications* 5:4414 (2014),
DOI 10.1038/ncomms5414; Murosaki, Ahmed & Gong, *Science and Technology of
Advanced Materials* 12(6):064706 (2011). The Nature paper hedges — lipids
*"possibly"* displace water — and that hedge is preserved on the card as
"understood to displace water" rather than hardened into a settled finding.

**Not a duplicate.** `QB3_I#q3` mentions barnacles only for foul-release
silicone (low surface energy, weak adhesion) — a different mechanism. The new
limb draws that distinction explicitly, which reinforces the card's existing
*Common CE Failures* warning against confusing the two.

### FUP-033 — `QB9_C#q5`, FOLLOW_UP, examiner Nair

> *"Diff.btwn marine insurance and car insurance"*

**Live recheck: MISSING.** Grepped corpus-wide for "car insurance", "motor
insurance", "motor policy" and "automobile insurance" — **zero hits**.

**Target adjudication.** The register's hand-chosen parent is `QB9_C#q5`
(insurance principles). The *score's* pick was `QB10_B#q1` — *"a consolidated
overview of SOLAS and MARPOL amendments entering into force from 2024 through
2028"*, at coverage 0.27. Inspected and rejected on sight: topically unrelated.
This is the register's own caveat firing in the open — only 4 of 39 follow-ups
had their parent chosen by a person, and this is one of them.

**The answer.** Five statute-anchored contrasts: commercial adventure vs
statutorily compulsory cover (MV Act 1988 Ch. XI s.146); interest at the time of
loss and "lost or not lost" (MIA 1906 s.6); valued policy conclusive in the
absence of fraud (MIA 1906 s.27(3)) vs Insured Declared Value after
depreciation; general average and salvage having no motor equivalent; liability
carried by a P&I mutual rather than a commercial policy. Closed with the Indian
mirror statute, the Marine Insurance Act 1963.

**Placement.** The register calls it "an opening follow-up". Read as a framing
device *within the limb*, not as a re-ordering of the card — putting a
comparison ahead of the six principles would displace the answer to the question
actually asked. The directed edge is additionally recorded in the card's
existing **Examiner Chain**, so a later examiner simulator can walk it as data
rather than parse it out of prose.

---

## 2. Why FUP-006 is `HELD_GOVERNANCE`

The hold is recorded as **structure, not prose**, in the manifest's
`held_actions` block: id, governed status, target, blocker, blocking manifest /
action / validator / check, the empirical proof, the resolution owner, and
`work_still_owed: true`. `held_actions` is classified `LOAD_BEARING` in
`oral_manifest.FIELD_CLASSES` and asserted by `audit_manifest`, so it cannot
decay into decoration.

`HELD_GOVERNANCE` is deliberately **not** `REJECTED`, **not**
`RETARGET_REQUIRED`, **not** `ALREADY_COVERED` and **not** a withdrawal. Each of
those would erase the fact that the work is still owed. The register's own entry
for FUP-006 stays `AUTHORISED_NOT_STARTED`, unedited — the batch carries the
status, so there is exactly one status source and the register was not adjusted
to disguise the hold. `validate_batch_f1` asserts that too
(`register_status_of_held_action_untouched`, mutation X).


**The adjudication is sound and independently corroborated twice.** The register
records `decision_basis: "hand adjudication against current answer bodies"`, and
E1's own `ENRICH-A003` record — written months earlier, without reference to
this batch — already names GAP-0620 on this target as *"Different limb — a
worked casualty application — and NOT implemented here."* Live recheck agrees:
`QB1_A#q9` carries an Ever Given casualty anchor but never works the YAR Rule A
elements through the Ever Given facts, which is exactly what the examiner asked.

**The blocker is governance.** `QB1_A#q9` is the only F1 target pinned by an
earlier record. `batch_e1_enrichment_manifest.json` pins its post-edit digest
`a1deaf3445bc1c88`, and `validate_batch_e1.py` compares that pin to the **live**
page. Anchor-level sibling delegation exempts the card from
`only_authorised_cards_changed` — but **not** from `manifest_digests_match`,
which has no delegation path in any of the eleven batch validators.

**Proved, not assumed.** A scratch insert into `QB1_A#q9` took
`validate_batch_e1.py` to *25 checks, 1 FAIL*, failing exactly
`manifest_digests_match ['QB1_A.html#q9 post']` and nothing else — 24 other
checks, including `edits_purely_additive` and `only_authorised_cards_changed`,
stayed green. The scratch edit was then restored byte-exactly
(sha256 `9aab34d4…`, verified).

**This is structural, not a one-off.** Eight of the 35 register actions are
colocated on cards a shipped enrichment already edited — FUP-003, 006, 008, 009,
013, 017, 025, 034 — and every one of them will hit this same wall.

Implementing FUP-006 today would have required either shipping a red historical
guard, or rebaselining E1's manifest, which is forbidden. Both are precisely
what this pipeline exists to prevent, so the action is held rather than forced.

### Recommended bounded fix (NOT done here — it is a Founder decision)

A **post-pin supersession contract** in `oral_manifest.py`, the single shared
authorisation surface:

* a later batch manifest may declare `supersedes_post_pins` naming the earlier
  record, the `file#anchor`, and its own post-edit digest;
* the earlier validator's digest check consults that declaration instead of
  failing, and only when the superseding record's own pin matches live — so the
  live state stays pinned by exactly one record and nothing is merely switched
  off;
* non-vacuity is testable in both directions, the way delegation already is:
  remove the later manifest and the earlier guard must go red again.

This touches release evidence (`validate_batch_e*.py`) and changes the meaning
of every historical digest pin in the repo, so it is deliberately a separate,
reviewed change and not a side effect of a content batch.

---

## 3. Verification

| Action | Verification class | Basis | Currentness |
|---|---|---|---|
| FUP-018 | `PRIMARY_AUTHORITY_REQUIRED` | asserts a published experimental mechanism attributed to named papers, so not `TECHNICAL_REASONING_ONLY` (whose recorded meaning here is "no external claim beyond standard architecture") | **NOT_REQUIRED** — re-inspected against the §6 trigger list; no office-holder, limit, convention status, adoption date, guidance, institution or contact |
| FUP-033 | `PRIMARY_AUTHORITY_REQUIRED` | every point anchored to statute | **VERIFIED_CURRENT** — the register's floor said no exposure, but the limb *does* assert current statutory status (compulsory motor third-party cover in India; the governing Indian marine statute). Both checked, not assumed |

The register's `currentness_required` is a **floor, not a ceiling**, and FUP-033
is a worked example of the floor being under-inclusive.

**Deliberately excluded from FUP-033:** the UK Insurance Act 2015 reform of the
duty of fair presentation, which interacts with the card's pre-existing
statement that non-disclosure lets the underwriter avoid from inception. That
statement is canonical text outside the authorised limb; it is recorded as debt
below rather than silently rewritten.

---

## 4. Additivity and product invariants

| Property | Result |
|---|---|
| Character-level opcodes | `equal` + `insert` only — **0 non-insert ops** on both cards |
| Line-level (`git numstat`) | QB3_I `4/0`; QB9_C `10/1` — the single deletion is the Examiner Chain line being extended in place |
| q-text | unchanged on both |
| Anchors | unchanged; each target anchor appears exactly once |
| Timed blocks (15s / 60s) | untouched |
| Canonical total | 721 → 721 |
| Question-bearing files | 86 |
| New / removed cards | 0 / 0 |
| Held action's target `QB1_A#q9` | untouched (asserted, and mutation C proves the assertion fires) |
| Line endings | homogeneous per file — QB3_I stays CRLF (550/550), QB9_C stays LF. Inserts were built with each file's own EOL, so neither became mixed |
| Control bytes | `oral_bytes.py`: scanned 2, hits 0 |
| DOM | both pages parse with 0 errors and 0 residual open tags; both cards sit directly under `div#q-feed` |

**Not browser verified** — the Browser pane cannot serve this static tree in
this environment. Verification is static/DOM only, stated rather than faked.

---

## 5. Guards

* `tools/oral/validate_batch_f1.py` — **30 checks, 0 FAIL**. Fails closed: an
  unreadable register, manifest, sibling record, baseline or content index
  reports `unavailable` and returns non-zero rather than skipping. Loads the
  baseline corpus with **one `git archive`** rather than 86 `git show` calls,
  because a slow guard is a guard people skip.
* `tools/oral/mutate_batch_f1.py` — **19 mutations, 0 escapes, 0 no-ops, 0
  crashes**. Every mutation must trip its **own named check**; breaking a
  different check counts as an escape. Preflight proves every mutation changes
  bytes before the probe phase runs. The suite also parses its own summary line
  back with the shared `parse_summary` and requires agreement.
* **Mutation N is the important one.** It removes `batch_f1_manifest.json` from
  the authorisation surface and requires an *earlier* guard
  (`validate_batch_e4`) to go red. Without it, "all guards green" would only
  mean the guards were switched off.
* **Mutation C** edits the held action's parent card and requires
  `held_action_target_untouched` to fire — a held action leaves no `cards[]`
  trace, so nothing else in the pipeline would notice it being quietly worked
  on. **Mutation O** drops FUP-006 from the manifest's declaration and requires
  `held_action_is_still_declared_with_a_reason` to fire, so the hold cannot be
  tidied away.

### The full release surfaced a second latent blocker — at gate 28

The first `--full` run (46 gates, 5407.9s) **stopped at gate 28 of 46**:

```
[27/46] validate_batch_e6   PRE_EXISTING_BASELINE  22.6s  failing=[line_endings_homogeneous_per_file]
[28/46] batch_e6_mutate     UNAVAILABLE            22.9s  exit=2
RELEASE-CRITICAL FAILURE at batch_e6_mutate -- stopping.
```

`mutate_batch_e6.py:300` refuses to run unless its control validator is green:

```
PRE-RUN validator is not green (['line_endings_homogeneous_per_file']) - aborting
```

So the **known E6 line-ending evidence debt does not merely make the validator
amber — it makes the E6 mutator unrunnable altogether.** The debt was correctly
classified for the validator; nobody traced the consequence for the mutator,
which hard-aborts with exit 2, and the runner treats `UNAVAILABLE` as
release-critical.

**This is pre-existing and not caused by F1.** The runner's own derived baseline
proves it: it re-ran `validate_batch_e6` in a clean worktree of `origin/main`
and reported `baseline_failing: ["line_endings_homogeneous_per_file"]`,
identical to live. Since the mutator aborts iff that validator is non-green, it
aborts on clean `origin/main` too.

It was **latent** rather than new: E6's own session passed because its working
copy still held the pre-normalisation CRLF that its manifest pinned. A fresh
checkout normalised those files to LF under `.gitattributes`, breaking the pin —
and nothing re-ran the E6 mutator until this release.

Deliberately **not repaired here** (it is unrelated debt, and repairing it means
touching E6 release evidence). The remaining 18 gates were obtained with the
runner's committed `--keep-going` flag rather than by any local edit or
suppression.

### And a third: the health gate could never pass

With `--keep-going`, the second run reached all 46 gates and `qb_health_check`
reported **FAIL — candidate 368, baseline 368, NEW=1, GONE=1**. Equal counts,
different sets, which is exactly what set-comparison exists to catch.

The samples named the culprit:

```
new_sample:  ["Loading source: local ..."]
gone_sample: ["Loading source: ref (origin/main) ..."]
```

That is the checker's own **provenance banner** counted as a finding.
`_HEALTH_NOISE` in `run_oral_release.py` already stripped `source`,
`source_type`, `commit`, `files` and `eol` — but not `Loading source`. The
runner deliberately runs the two sides with different `--source` flags, so that
line differs **by construction on every run**: the gate was structurally
incapable of passing on any tree, clean or otherwise.

Proved before fixing: running the checker both ways and diffing the line sets
gave **14 differing lines, every one of them provenance** (`Loading source`,
`files 951 vs 837`, `source`, `source_type`) and **zero differing findings** —
152 findings on both sides, same commit.

Fixed with a one-line addition to the noise filter, and guarded both ways in
`test_oral_release_infra.py` section 6: provenance must be stripped **and** a
genuine finding difference must still be reported, so it can never be "fixed"
by filtering everything. Re-run bounded: **PASS, candidate 367 = baseline 367,
NEW=0, GONE=0.**

Why this one *was* repaired when the E6 debt was not: `run_oral_release.py` is
current infrastructure, already being modified this session to register F1's
gates, and the defect made a gate impossible to pass. The E6 debt lives in
historical release evidence, which is not this batch's to touch.

### A hardcoded total that expired

`test_oral_release_infra.py` asserted `len(manifests) == 11`. F1 turned that
control red **simply by existing** — the repo's own *"guards that expire"*
defect class, inverted. It is now an enumerated list
(`EXPECTED_BATCH_MANIFESTS`), matched both ways, following the same pattern
`POST_E6_GATES` already uses: adding a batch means editing one reviewable line,
and a hardcoded total can never expire out from under the control again.

`_batch_pair()` also gained an explicit `historical_39` parameter. F1 passes
`False`; the historical count stays exactly **39** and remains checkable forever.

---

## 5a. Full release result

Run 2, `--full --keep-going`, **46 of 46 gates executed**, 6709.6s.

| Status | Count | Which |
|---|---|---|
| PASS | 42 | includes `validate_batch_f1` (32 checks) and `batch_f1_mutate` (24 mutations) |
| PRE_EXISTING_BASELINE | 2 | `validate_batch_e6` (line-ending debt), `validate_audit` (`index_tier_literals_valid`) |
| UNAVAILABLE | 1 | `batch_e6_mutate` — pre-existing, §5 |
| FAIL | 1 | `qb_health_check` — harness provenance defect, diagnosed and fixed, re-run **PASS** |

* **Mutation aggregate: 17 suites, 282 mutations, 0 escapes, 0 no-ops, 0 crashes.**
* **Determinism: PASS** (155.5s).
* **Health: PASS** on re-run — candidate 367 = baseline 367, NEW=0, GONE=0.
* **Audit: `PRE_EXISTING_BASELINE`**, derived from `origin/main`, not declared —
  `failed 1` live and `baseline_failed 1`, so no new failure. Classified
  semantically; the tool exits **0** while reporting a failed check, which is
  why exit code is never the verdict here.
* **Generated artefacts restored by exact path** and verified:
  `PHASE2_VALIDATION_RESULTS.json` (gates 31, 36), `VALIDATION_RESULTS.json`
  (gate 37), `ORAL_NOTES_IMPACT.md` (gate 46). Final tree shows no diff under
  `examiner-audit/`.

Neither remaining non-green item is F1's: one is pre-existing E6 evidence debt,
the other its downstream consequence. **No new `FAIL_CURRENT`.**

## 6. Register status and immutability

The authoritative register is **byte-unchanged** — `git diff` against `HEAD` is
empty and `build_followup_register.py --check` still reports it byte-identical
to a fresh build. Implementation status lives **only** in
`batch_f1_manifest.json`, so there is exactly one status source and no competing
second one. `validate_followup_register.py` reports **32 checks, 0 FAIL** both
before and after F1.

Because status is external to the register, the repo can prove "35 authorised"
and "2 implemented by F1". A bare "33 remaining" is arithmetic, not a
repo-provable fact, and is reported here as *33 unimplemented, of which 8 are
blocked by the post-pin gap and 25 are clear*.

---

## 7. Next batch — F2 recommendation (NOT started)

All three `CONFIRMED` actions are now consumed, so F2 is necessarily
`REQUIRES_LIVE_ADJUDICATION`. Selection is by **evidence, not numeric FUP
order**, and adds two constraints F1 discovered:

**Recommended F2 — three actions, all unpinned, all strongly parent-aligned,
all low currentness exposure:**

| FUP | Parent | Ask | Why |
|---|---|---|---|
| FUP-007 | `QB1_C#q2` *Static vs dynamic stability* | Information obtained from GZ curve | direct mechanical continuation of the parent; no perishable content |
| FUP-021 | `QB4_B#q13` *STCW requirements for Junior Engineers* | STCW levels, competency at support level | parent is the same instrument and level structure |
| FUP-032 | `QB8_A#q4` *IMSBC Code groups A/B/C/MHB* | High-density cargo, precautions, Bulk Jupiter, IMSBC classification | parent is the exact code the ask names |

**Explicitly deferred, with reasons:**

* **All 8 colocated actions** (FUP-003, 006, 008, 009, 013, 017, 025, 034) —
  blocked by the post-pin gap in §2. Do not schedule until the supersession
  contract exists.
* **FUP-019 (`QB3_J#q1`) and FUP-029 (`QB6#q7`)** — both excellent topical fits
  (GHG/GWP/methane; UNFCCC/COP28 pledges), but GHG is the corpus's most
  perishable subject and the IMO net-zero framework is a live moving target.
  The register flags **neither** for currentness, which is the floor being
  under-inclusive again. Worth a dedicated environment batch with full
  currentness verification, not a mixed one.
* **FUP-028 (`QB5_E#q5`)** — F-P1 and HIGH confidence, but
  `METADATA_ONLY_CANDIDATE`. The ask reads *"IMO new SG- Arsenio Dominguez from
  Panama"*: a candidate's **fact note, not a question**, and a current
  office-holder claim. This is the trap the register warned about; it needs
  adjudication before it is allowed near a batch on priority alone.
* **FUP-010 and FUP-015** — visible score-chosen mis-targets ("Challenging
  ballast" parented on *India government contribution in shipping*; "SOLAS Ch
  XI-1" parented on *dry chemical powder firefighting*). Likely
  retarget candidates; adjudicate before producing.

---

## 8. Debt (max 5)

1. **The post-edit digest pin has no delegation path** — §2. Blocks 8 of 35
   follow-ups. The highest-value item on this list.
2. **`QB9_C#q5` leaks raw markdown to candidates.** The pre-existing P&I
   paragraph renders as `> P&I Clubs are mutual…settled. > >`. Candidate-visible,
   outside the F1 limb, deliberately not repaired here — a post-release content
   repair needs its own correction manifest.
3. **`QB9_C#q5` states that non-disclosure lets the underwriter void the
   contract from inception.** For UK business insurance the Insurance Act 2015
   replaced automatic avoidance with proportionate remedies. Pre-existing
   canonical text, outside the authorised limb; flagged, not rewritten.
4. **`batch_e6_mutate` is unrunnable, and it blocks the whole release.**
   `file_line_endings` in the E6 manifest remains unreproducible, so
   `validate_batch_e6` is non-green, so `mutate_batch_e6.py` hard-aborts
   (exit 2) and the runner reports `UNAVAILABLE` — release-critical. A default
   `--full` run therefore stops at gate 28 of 46 and never reaches health,
   audit, determinism or any F1 gate. This is **more severe than the amber
   validator it descends from** and should be fixed with, or before, the
   digest-supersession work. Not repaired here.
5. **`index_tier_literals_valid` still fails on a clean `origin/main`** (43
   invalid literals), carried since E1.
