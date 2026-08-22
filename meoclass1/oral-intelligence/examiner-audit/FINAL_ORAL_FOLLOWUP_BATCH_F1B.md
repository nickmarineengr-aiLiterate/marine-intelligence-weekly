# Oral follow-up production — batch F1b

**FUP-006 implemented. The first real historical-digest supersession chain on main.**

| | |
|---|---|
| Batch | `F1b` — single action, `FUP-006` |
| Target | `QB1_A#q9` — *General Average — Explain including act and procedure followed.* |
| Examiner | Nair |
| Ask | "Explain how GA was applicable for ship ever given stuck in suez." |
| Relationship | `FOLLOW_UP`, `QB1_A#q9 → EXAMINER_FOLLOW_UP → QB1_A#q9` |
| Register status | `AUTHORISED_NOT_STARTED` — **deliberately untouched** |
| Baseline | `e8173b2` |
| Manifest | `tools/oral/batch_f1b_manifest.json` |
| Validator | `tools/oral/validate_batch_f1b.py` — 38 checks, 0 FAIL |
| Mutations | `tools/oral/mutate_batch_f1b.py` — 26 mutations, 0 escapes |
| Full release | 48 of 48 executed — 46 PASS, 2 PRE_EXISTING_BASELINE, 0 FAIL, 0 UNAVAILABLE |

---

## 1. Why this batch exists

F1 authorised three actions, produced `FUP-018` and `FUP-033`, and **held**
`FUP-006` as `HELD_GOVERNANCE`. The blocker was structural, not editorial:
`QB1_A#q9` is pinned by `batch_e1_enrichment_manifest.json` through
`ENRICH-A003` (`post_edit_digest a1deaf3445bc1c88`), and `validate_batch_e1.py`
compares that pin to the **live** page. Anchor-level sibling delegation exempts
a card from `only_authorised_cards_changed` but never from
`manifest_digests_match`, which had no delegation path in any of the eleven
batch validators. Producing FUP-006 meant shipping a red historical guard or
rebaselining E1. Both are forbidden, so F1 held it and said so.

The infrastructure session that followed built `tools/oral/oral_supersession.py`.
**F1b is its first production use.**

---

## 2. What was implemented

### `FUP-006` — `QB1_A#q9`, `FOLLOW_UP`, examiner Nair

**Current-live adjudication: `PARTIALLY_COVERED`** — re-adjudicated against the
live card rather than accepted from F1's hold record. The card already defines
the general average act, lists the Rule A elements, sets out the procedure, and
carries a one-sentence Casualty Anchor naming Ever Given. It never worked the
Rule A elements through the Ever Given facts, never said which act was the
general average act, and never said what the Rules exclude.

Corroborated independently by E1's own record, which scoped the two limbs apart
before either was written: `ENRICH-A003` names GAP-0620 on this target as
*"Different limb — a worked casualty application — and NOT implemented here."*

**Placement.** A new `<h4>` block inserted after `Who the Average Adjuster Is`
(E1's addition) and before `CE Role — Evidence Preservation`, so the reading
order runs elements → examples → procedure → adjuster → **worked application** →
CE role. The directed follow-up edge was appended to the existing CE Oral Tip,
which is the tier that already carries this card's Nair/Simon relationships — so
**examiner relationships stayed at 960 / 7**. A new examiner-bearing block would
have moved that count.

**Content.** The worked application maps each Rule A element onto the facts, and
carries the points a candidate most often misses:

* the **grounding is not the general average act** — the act is the owner's
  deliberate decision to engage dredgers, tugs and salvors;
* **peril is the element to argue, not assert** — nothing was on fire and no
  container was jettisoned, and Rule A carries the argument because peril need
  not be immediate or inevitable, only more than fanciful;
* salvage expenditure is allowed by **Rule VI(a)** subject to (b)–(d), and
  **Rule VI(d)** excludes Article 14 special compensation and SCOPIC;
* **Rule C** bars demurrage, loss of market and delay outright, so the
  casualty's largest economic consequence — the several hundred ships queued at
  both ends of the canal — contributed nothing to the GA;
* **Rule D** keeps contribution alive irrespective of fault, which is why the
  adjustment proceeded while the cause of the grounding was still contested.

**Verification class: `PRIMARY_AUTHORITY_REQUIRED`**, discharged against the CMI
text itself — the York-Antwerp Rules 2016, read from the CMI tabular comparison
of the 1994 / 2004 / 2016 editions. Rules A.1, VI(a), VI(d), C.1, C.3 and D were
each checked verbatim rather than recalled.

**Currentness: `VERIFIED_CURRENT`**, even though the register's floor said not
required — `currentness_required` is a floor, not a ceiling, and section 6
requires independent inspection. Two present-tense assertions were found and
both checked: that YAR 2016 is still the current edition (the 2016 Rules were
approved at the CMI Conference in New York in May 2016 and no later edition has
been adopted), and that the Suez Canal Authority settlement terms remain
undisclosed.

**Deliberately not asserted**, because the evidence does not support it: the
settlement figure, who ultimately bore what proportion, the cause of the
grounding, any allocation of legal liability, the exact date of the GA
declaration (sources place it between 1 and 5 April 2021, so the card says
"shortly afterwards"), and which YAR edition the Evergreen bills of lading
incorporated — the analysis is written so it holds either way, Rule A being
word-for-word identical in all three editions. `validate_batch_f1b.py` guards
the first and the last of those with `no_unsupported_claim_reintroduced`.

**Diff.** One card, one file.

| Level | Insert | Delete | Replace |
|---|---|---|---|
| Character (`SequenceMatcher` opcodes) | 2 ops, 4,007 chars | 0 | 0 |
| Line (`git diff --numstat`) | 14 | 1 | — |

The single line-level deletion is the CE Oral Tip line being rewritten with text
appended to it; at character level it is an insertion, which is why
`edits_purely_additive` is green.

---

## 3. The supersession chain

```
batch_e1_enrichment_manifest.json / ENRICH-A003   a1deaf3445bc1c88   (H1)
        |
        v
batch_f1b_manifest.json / FUP-006                 46defd301a1f56a3   (H2, live)
```

* `F1b.pre_edit_digest` **==** `E1.post_edit_digest` — continuity proved at
  source: the applier read `a1deaf3445bc1c88` off the untouched live card before
  writing a byte.
* `F1b.post_edit_digest` **==** the live card after the edit.
* E1 was **not** rebaselined, **not** relaxed, and stayed at **25 checks / 0
  FAIL** throughout. Its claim is now strictly stronger: not "my state is live"
  but "my state is the ancestor of what is live".
* `python tools/oral/oral_supersession.py` →
  `PASS QB1_A.html#q9  2 state(s)  ENRICH-A003 -> FUP-006`; 1 chain, 0 FAIL.
* The chain stays in E1's `sha256(card_text_lf)[:16]` convention throughout.

**No one-off exception exists.** The generic resolver handles it. There is no
`if FUP == 006`, no `if QB1_A#q9`, no skipped digest, and no accepted "any later
digest". Proved by mutation, not by inspection: with F1b removed from the
authorisation surface, `validate_batch_e1.py` goes red on
`manifest_digests_match` exactly as it did before the contract existed.

---

## 4. F1's history is intact

F1 still declares `FUP-006` as `HELD_GOVERNANCE` with `work_still_owed: true`,
and its `cards[]` still contains only FUP-018 and FUP-033. That is a truthful
record of what F1 did, and F1b does not rewrite it.

The discharge is recorded in **F1b**, through a new `discharges_hold` field
(`LOAD_BEARING`, asserted by `oral_manifest.audit_manifest`):

| Assertion | Prevents |
|---|---|
| `discharged_holds_well_formed` | a discharge with no id, holder or reason |
| `discharged_holds_are_actually_produced` | claiming a discharge the batch never implemented |
| `discharged_holds_name_a_real_hold` | naming a manifest that never held it, or whose hold has since been deleted |

The register is likewise untouched: it is an **authorisation** record, not a
status board. `register = authorised work; production manifests = implementation
history.` Mutations O, P, Q, R and S attack exactly this — claiming F1 produced
the action, deleting the hold, marking the work no longer owed, dropping the
discharge, and editing the register to say `PRODUCED`. All five are caught.

---

## 5. Guards

### Two guards expired — in opposite directions

Both were caused by a legitimate change, and neither was fixed with a special
case.

**Started failing.** `validate_batch_f1.py`'s `held_action_target_untouched`
asserted the held card was byte-unchanged — correct while held, wrong the
instant the hold was discharged. It now changes **subject** rather than standing
down: with no discharge declared, the card must be unchanged (original
semantics); with one declared, it must be exactly the state the discharging
record pinned. Non-vacuous under both regimes — F1's mutation C still trips the
same named check — and F1's check count did not move (32).

**Kept passing while meaning nothing.** `test_oral_supersession.py` asserted
*"no supersession is declared on main today"* — true the day the mechanism
landed, stale the first time it was used. It now asserts that **every declared
chain resolves**: silent when there are none, stronger when there are. This is
the more dangerous shape of expiry, because nothing goes red; the guard simply
stops describing the repository.

### A live fixture must derive its predecessor

`test_oral_supersession.py` hardcoded `ENRICH-A003 / a1deaf3445bc1c88` as the
state its scratch successor descended from. F1b legitimately appended a state,
so the scratch became a second successor to one predecessor — `CHAIN_FORK`,
which reads as a broken contract when the only stale thing is the fixture.
`terminal_state_for()` now asks the resolver where the chain currently ends, so
the scratch extends it. The suite went **48 checks → 55**, because the FUP-006
case stopped returning early and now proves the contract **at depth three**.

A related trap: a resolver failure **changes shape** once a chain exists. The
same probe that reported `PIN_MISMATCH` reports `TERMINAL_NOT_LIVE` once a
successor is declared, and a parser reading only the first shape silently
returns `None` — which is what made the case abort rather than fail loudly.

### Two process incidents worth recording

* **A killed mutating control leaves product bytes.** `test_oral_supersession.py`
  restores in a `finally:`, which does not run when the process is killed by a
  timeout. Run bare and killed at two minutes, it left `QB1_A.html` mutated on
  disk and `validate_batch_e1.py` red — a "failure" that was purely the
  leftover. The release runner owns a byte snapshot and an exact-path restore;
  that protection only applies to runner-owned invocation.
* **Never run two gates concurrently.** A validator run while that background
  control was live read a transiently-probed `QB3_I.html` and reported a card as
  changed that was byte-identical to `HEAD`. The runner enforces serial
  ownership for this reason.

Both are now in the SKILL traps table.

---

## 6. Full release

`python tools/oral/run_oral_release.py --full` — one definitive run, no
`--keep-going`.

```
  PASS                   46
  PRE_EXISTING_BASELINE   2
  executed               48 of 48 planned
  wall time              7705.6s
  mutations              19 suites, 341 mutations, 0 escapes, 0 no-ops, 0 crashes
  release                all gates green
```

* **0 FAIL, 0 UNAVAILABLE.** Both `PRE_EXISTING_BASELINE` results are the known
  carried debt: `validate_batch_e6` (`line_endings_homogeneous_per_file`) and
  `validate_audit`. Each was derived from `origin/main`, never hardcoded, and
  neither was repaired or absorbed.
* **Gate count 46 → 48.** F1b added exactly two, `validate_batch_f1b` (45) and
  `batch_f1b_mutate` (46), both `historical_39=False`. The historical 39 are
  intact and still counted as 39.
* **Mutations 315 → 341** across **18 → 19** suites: exactly F1b's 26.
* **Health:** `candidate(local)=367  baseline(origin/main)=367  NEW=0  GONE=0`,
  compared as sets with the corrected noise normaliser. No source-banner false
  positive.
* **Determinism:** PASS.
* **Product guard:** clean. No QB bytes left behind by any gate. The one
  `WARNING: generated artefacts still differ after restore` at `validate_phase2`
  was followed by the runner's exact-path restore of
  `PHASE2_VALIDATION_RESULTS.json`, and `git status` confirms no examiner-audit
  artefact is dirty.

**Canonical invariants:** 721 questions · 86 question-bearing files ·
960 / 7 examiner relationships · content index CURRENT
(`build_qb_content_index.py --check`: *outputs on disk already match the live
derivation*). No new canonical card; q-text and anchor unchanged.

---

## 7. Follow-up accounting — derived from the repository, not by arithmetic

Computed by scanning `cards[]`, `held_actions` and `discharges_hold` across
every `batch_*_manifest.json`:

| | |
|---|---|
| Register total | **35** |
| Implemented | **3** — `FUP-006` (F1b), `FUP-018` (F1), `FUP-033` (F1) |
| Holds declared | 1 — `FUP-006`, by F1 |
| Holds discharged | 1 — `FUP-006`, by F1b |
| **Open holds** | **none** |
| Unstarted | **32** |
| Retarget required | 2 — `FUP-009`, `FUP-031` |
| Metadata-only candidate | 1 — `FUP-028` |

---

## 8. Next batch — F2 recommendation (planning only, NOT started)

**The hand-adjudicated tranche is now exhausted.** This is the most important
planning fact to come out of F1b, and it changes what F2 is.

All three implemented actions were `target_review_status: CONFIRMED`, `HIGH`
confidence, with a strong relationship class (`FOLLOW_UP` / `EXPECTED_DETAIL`).
Of the 32 that remain:

* **32 of 32 are `REQUIRES_LIVE_ADJUDICATION`** — none is `CONFIRMED`;
* **31 of 32 are `TOPIC_INFERENCE_ONLY`**, the weakest relationship class;
* the only remaining `HIGH`-confidence, strong-relationship action is
  **`FUP-028`**, which is also `METADATA_ONLY_CANDIDATE` (the source says it is
  *not an answer* — likely a trap) and `currentness_required: true`, because it
  names a serving office-holder. **Do not take it into F2.**

So from F2 onward, target adjudication stops being a formality. Every action's
parent was chosen by an IDF coverage score, not by a person.

**Recommended: authorise F2 as "up to three", not three.**

| Action | Priority | Target | Topic | Why |
|---|---|---|---|---|
| `FUP-007` | F-P2 | `REQUIRES_LIVE_ADJUDICATION` | Safety / Stability — *information obtained from GZ curve* | unpinned, no colocation, `currentness_required: false` |
| `FUP-021` | F-P2 | `REQUIRES_LIVE_ADJUDICATION` | STCW & Certification — *STCW levels, competency at support level* | as above |
| `FUP-032` | F-P2 | `REQUIRES_LIVE_ADJUDICATION` | Cargo — *high-density cargo carriage, precautions* | as above |

The historical proposal survives re-evaluation on the mechanical criteria — all
three are `F-P2`, `MEDIUM`, no currentness exposure, no colocated enrichment, and
pinned by no earlier record, so none needs a supersession chain. The subject
spread (stability / certification / cargo) is coherent without overlapping.

**But all three are `TOPIC_INFERENCE_ONLY`.** F2's first task is live target
adjudication against the current answer bodies, and any of the three may
legitimately be dropped, retargeted or found `ALREADY_COVERED`. Authorising a
fixed count would create pressure to produce against a parent that adjudication
rejects — which is the exact failure `RETARGET_REQUIRED` exists to name.

**Explicitly not in F2:** `FUP-009` and `FUP-031` (`RETARGET_REQUIRED` — they
need re-homing first, which is an adjudication task, not production) and
`FUP-028` (above).

**Now unblocked but not prioritised:** the five colocated actions on pinned cards
— `FUP-003`, `FUP-008`, `FUP-013`, `FUP-017`, `FUP-025` — are no longer blocked
now that supersession is proven in production. They are `LOW`/`MEDIUM`
confidence, so there is no reason to bring them forward, but the governance
reason for holding them is gone.

---

## 9. Debt (max 5)

1. **`file_line_endings` in the E6 manifest is still not reproducible.**
   Unchanged, carried, reported as `PRE_EXISTING_BASELINE`. Repairing it would
   mean rewriting what E6 certified.
2. **`index_tier_literals_valid`** still fails in `validate_audit.py` on a clean
   `origin/main` (43 invalid literals). Pre-existing, carried since E1.
3. **Stale counters** in `VALIDATION_RESULTS.json` /
   `PHASE2_VALIDATION_RESULTS.json` (`live_questions` 688 vs 721, `headings`
   954 vs 960).
4. **`authorisation_source` is still unread by every batch validator.** It now
   resolves, so it is not decoration, but no validator selects through it.
5. **F1b's limb is the largest single follow-up insert so far** — 4,031 bytes
   against F1's 2,034 and 2,896. Justified by a P1 action on a flagship card
   that had to carry a five-element mapping plus the Rule VI / C / D exclusions,
   but the trend is worth watching: QB2408's flashcards reached twice corpus
   length before anyone measured. A future batch should not read 4 KB as the new
   normal.
