# Final Oral gap decision — independent review record

Review of `research/oral-final-gap-adjudication-v1` at `d82daef`, from
`origin/main` at `66c919b`. No live product was touched.

The brief framed this as a laptop review of desktop work. It is not: the
adjudication branch was produced on this same clone, so this is a **second
adversarial pass over the same machine's output**, not machine-independent
corroboration. Everything below was re-derived from source artefacts and live
HTML rather than read off the adjudicated dataset.

## What reproduced exactly

| claim | method | result |
| --- | --- | --- |
| 688 canonical questions, 86 files | counted `q-card` anchors in both attribute orders across 124 `QB*.html` (38 are cheatsheets, 0 q-cards) | **reproduced**, 688 unique `file#anchor`, 0 duplicates |
| 311 governed − 9 P0 − 1 merged = 301 | set arithmetic on `FINAL_ORAL_GAP_CANDIDATES.json` and `FINAL_P0_PRODUCTION_BATCH.json` | **reproduced by identity**, not merely by count; zero strays either way |
| committed dataset is generated | re-ran the generator under three hash seeds | byte-identical, `git status` clean — not hand-edited |
| 26 validator checks, 0 failures | re-ran | reproduced |
| no live product touched | `git diff origin/main..HEAD` over QB HTML, index, examiner-index, SQ, xlsx, api, oralnotes | **empty** |

## Three findings that changed the inventory

### 1. A Notes promotion can create a card, and nothing recorded that

`decision_target` on a `NOTES_TO_QB_PROMOTION` row holds the **Notes source
anchor**, never a QB destination. The schema therefore had no way to say whether
a promotion enriches an existing card or creates a new one — so every
new-card promotion was invisible to the projected canonical count.

Reading all ten: nine have no QB home capable of absorbing them (COFR, the
Intervention Convention, free-fall lifeboat requirements, Bonjean curves, great
circle sailing, the galvanic series, caustic embrittlement, SID against CDC,
Incoterms). Each creates a card.

**The projected count of 710 was understated by nine.** The correct projection is
688 + 23 + 9 = **720**.

### 2. GAP-0065 was internally inconsistent with GAP-0689

`GAP-0065` ("BWTS USCG and IMO, AMS") was filed as a Notes promotion on the
stated ground that `QB3_J#q6` is "scoped to UV technology". It is not. Limb 3 of
that card is explicitly the IMO-against-USCG approval comparison; it names the
Alternate Management System, 46 CFR Part 162, VIDA, and the G8/G9 distinction.

The same dataset files `GAP-0689` — "USCG type approval not done, what is the
alternate provision?" — as `ALREADY_COVERED` **against that very card**. Two
near-identical asks, opposite dispositions, same target.

Resolved to `ALREADY_COVERED`. Notes promotions 10 → 9.

### 3. GAP-0595 is an enrichment, not coverage

Filed `ALREADY_COVERED` against `QB2_B#q7`. That card is the
Liner / NVOCC / VOCC operational model; the word *tramp* occurs in it exactly
once. The ask is the liner-against-tramp commercial contrast. The adjudicated
reason concedes "tramp is the residual limb only" — which is the definition of
an enrichment. Enrichment families 63 → 64 (68 after the medium conversions).

## The coverage column argues against the count, and it is wrong

`current_best_answer_coverage` on the proposed new cards is largely an
IDF-weighted false positive:

| family | ask | "best answer" | what that card actually is |
| --- | --- | --- | --- |
| GAP-0619 | medical evacuation and diversion | `QB9_B#q4` @ 0.51 | off-hire clause in a charter party |
| GAP-0442 | behaviour-based safety | `QB2_A#q10` @ 0.51 | IMSBC Code, Group A/B/C, TML |
| GAP-0128 | adaptive cylinder-oil control | `QB1_F#q9` @ 0.50 | how to reduce fuel consumption |
| GAP-0376 | stowaway handling | `QB9_C#q2` @ 0.45 | P&I — what the "I" stands for |
| GAP-0415 | autonomous ships | `QB2_A#q6` @ 0.40 | container vessel safety amendments |

Only `GAP-0465 → QB4_I#q2` is a real neighbour.

This cuts both ways, and the second direction is the dangerous one. The same
spurious-match mechanism can promote a genuine gap to ALREADY_COVERED. All 47
were therefore re-read: every one carries a **named target and a mention count**
rather than a score, which is the correct basis. One (GAP-0595) failed.

## The staleness narrative is partly mis-attributed

The record credits the movement in coverage to the frozen reconciliation being
stale. 40 frozen-zero families now score ≥ 0.30, but only **4** are explained by
a P0 anchor — the other 36 point at cards that existed before P0. The movement
is overwhelmingly finding #2 (title-matcher blindness) wearing a staleness
costume.

Consequently "median delta 0.0000 reproduces the governed matcher" is **not**
evidence of methodological equivalence: the median is dominated by the 179
families that did not move. Equivalence is established far more strongly by the
fact that `adjudicate_final_gaps.py` **imports** `reconcile_788.weighted_coverage`
and `oral_text.mtokens` rather than reimplementing them, so semantic drift is
impossible by construction. The stated proof is weaker than the actual proof.

## Reason-text corrections — disposition stands, justification was false

| family | claim | truth |
| --- | --- | --- |
| GAP-0120 | "Miller and Atkinson return zero hits corpus-wide" | Miller occurs 8× in `QB7_I`, always as *VVT/Miller cycling*, a methane-slip mitigation lever — never the cycle drawn or contrasted. Atkinson is genuinely zero. |
| GAP-0378 | "return three weak hits" | *steering gear* occurs **109×** across 10 cards. No card owns SOLAS II-1/29, so the card stands — but the pre-departure-test limb is already housed in `QB1_K` (SOLAS V/26, 12-hour test) and `QB4_C#q9` (drill frequency). Scope to II-1/29 and cross-link, or it becomes a third duplicate home. |
| GAP-0465 | BDN vocabulary "scattered, no owning card" | *bunker delivery note* 43 hits, *BDN* 61. `QB4_I#q2` genuinely holds BDN plus MARPOL sample tracking. The gap is ordering, disputes and the sample/retention regime. |

All other "zero hits" claims tested clean: FWA, behaviour-based safety, Type
B-60, ship broker, COSPAS-SARSAT/INDSAR, shale gas, flammability diagram,
wake-equalising duct, Bonjean, great circle, Incoterms, COFR, galvanic series,
caustic embrittlement.

## The 22, attacked individually

All 22 survive the last-resort test (existing coverage → enrichment → Notes
promotion → follow-up → merge → ambiguity). None is answerable from the current
live QB plus current Notes; each would cost a candidate the question.

Every one is single-examiner, single-occurrence. That is expected rather than
suspicious — the recurrent cross-examiner asks were the P0 batch — but it means
each was scrutinised for source-wording explicitness, and all 22 carry an
explicit ask rather than a topic label.

No merges are required among them. Two **co-location advisories** are recorded
instead: GAP-0159 / GAP-0558 share the capital-voyage-operating cost taxonomy,
and GAP-0225 / GAP-0218 are adjacent LSA arrangement asks.

## The seven medium candidates

| family | ask | decision |
| --- | --- | --- |
| GAP-0516 | drydock budgeting, job priority | **PROMOTE_TO_HIGH_NEW** — absorbs GAP-0517 and GAP-0519, so it carries three source families; a corpus sweep for budget / cost-estimation / job-list / tender vocabulary finds no owning card (the only dense *tender* hit is `QB1_C#q3`, the tender-against-stiff-ship stability card — a false match) |
| GAP-0239 | warranty against guarantee | CONVERT_ENRICH → `QB1_B#q19` |
| GAP-0443 | personality development onboard | CONVERT_ENRICH → `QB5_A#q6` |
| GAP-0553 | UN telecoms body (ITU) | CONVERT_ENRICH → `QB2_A#q5` |
| GAP-0672 | pre-repair checks, lifeboat davit | CONVERT_ENRICH → `QB10_B#q1` |
| GAP-0255 | shale gas | DEFER — examiner tangent, no syllabus anchor |
| GAP-0354 | VALEMAX | HOLD_AMBIGUOUS — referent clear, ask not |

## Ambiguous residue

The seven ambiguous families (STCW 7/8, FTIR, Navigational Equipments, Metos,
ICCT/ICT, IMO-ILO, Djibuti) are genuinely unformed asks; adjacent source context
does not resolve any of them into a scope. GAP-0354 joins them, making **8**.
Forcing any onto a target would cost a candidate a wrong answer to save a
review. None is a confirmed missing answer.

Of the 115-row human-review queue, the partition (42 resolved, 11 enrich, 62
still ambiguous) reproduces. The guard that matters is that 96 rows carry ≥ 0.90
coverage while 41 are one- or two-token prompts — **high coverage on a terse
prompt is not evidence**, because a short token set is trivially contained in a
long answer.

## Deferrals are safe

All 95 deferred families are single-occurrence, single-examiner and governed
P2. Nothing high-recurrence, multi-examiner or governed-P1 was deferred. This is
a set property, not a sample.

## Two gaps in the adjudicated validator

Its 26 checks are all referential integrity. Neither of the two controls that
mattered existed:

- **F** — no projected-count check at all, because the schema could not express
  a promotion that creates a card.
- **G** — nothing tests that two families sharing a target hold compatible
  dispositions. This is exactly how GAP-0065 / GAP-0689 escaped.

Both are implemented in `validate_production_authorization.py`.

**Residual weakness, stated honestly:** check G2 keys on QB-anchor targets. In the
adjudicated dataset GAP-0065's target was a *Notes* anchor, so G2 would not have
fired there either. It only becomes load-bearing once promotion targets are
normalised to QB destinations — which this authorisation does. The mutation
harness proves what G2 catches, not that it would have caught the original.

## Family count is not workload count

68 enrichment families collapse to **63** unique edits; 39 follow-up families to
**35** insertion groups. Together they touch **90** distinct existing cards, so
eight cards receive both an enrichment and a follow-up and should be visited
once.

## Verification

- 27 validator checks, 0 failures. Every check fails closed.
- 17 mutations, 17 caught, 0 escapes, 0 no-ops, 0 crashes. Each proves it was
  APPLIED by SHA-256 delta and RESTORED by digest, so a silently no-op mutation
  is an escape rather than a pass.
- Determinism: byte-identical JSON and Markdown under `PYTHONHASHSEED` 0, 1 and
  524287.
- Live product diff against `origin/main`: empty.

## Master workbook

**DEFERRED**, unchanged. `MEO_QB_master_v27.xlsx` and
`MIW_August2026_QuestionBank_SHARE.xlsx` need live anchors, and 32 brand-new
cards do not have anchors until production creates them.
