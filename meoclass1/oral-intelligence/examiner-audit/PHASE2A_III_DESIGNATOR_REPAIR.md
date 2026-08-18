# Phase 2A-iii — mixed-case designator conflict repair

**Branch:** `research/oral-examiner-intelligence-v1-phase2a-iii`, from
`research/oral-examiner-intelligence-v1-phase2a-ii` @ `f9c5a12`
**Answers:** `PHASE2A_II_NOTES_COVERAGE.md` section G, the limitation that phase pinned
rather than hid, and which it required to be resolved before GAP-0409 is adjudicated.
**Scope:** the designator **conflict layer** only. The Phase 2A-i tokeniser is unchanged,
the 788 was not recomputed, no Release-A or P0 dataset was created, no reconciliation
baseline was rewritten, and no live product file was touched.

The governing rule of this phase, in three lines the code now enforces:

> A shared broad family must not erase a conflict between different specific members.
> ME-GI is not ME-GA. D-1 is not D-2. Form A is not Form B.
> But Annex VI **is** Annex 6, and naming only the family names no member at all.

---

## A. The defect, reproduced in full sentences before anything was edited

`designator_conflict` is exercised in production on mixed-case **sentences**. The Phase 2A-i
controls compared **bare** designators, where the string is wholly uppercase, the acronym
pass is skipped, and the conflict was correctly found. That is the gap the defect lived in:
it survived 181 controls, then 287, and 25 mutations.

Reproduced through the real `mtokens` to `designator_conflict` to `classify` path, at
`f9c5a12`, before the fix:

| Full-sentence pair | Expected | Observed |
|---|---|---|
| `Explain the working of the ME-GI engine.` vs `... ME-GA engine.` | conflict | **no conflict** |
| `Explain the working of the ME-GI engine.` vs `... ME-LGI engine.` | conflict | **no conflict** |
| Form A vs Form B · D-1 vs D-2 · G8 vs G9 · regulation III/1 vs III/2 | conflict | conflict |
| Annex VI vs Annex 6 | no conflict | no conflict |
| same-topic prose, no differing designator | no conflict | no conflict |

The tokens, at the point the conflict is computed:

```
A "...ME-GI engine."   dsg:me-gi  dsg:megi  dsg:me  dsg:gi
B "...ME-GA engine."   dsg:me-ga  dsg:mega  dsg:me  dsg:ga

A families  {me: [gi, me],  megi: [megi], gi: [gi]}
B families  {me: [ga, me],  mega: [mega], ga: [ga]}
                  ^^^^^^ the shared pseudo-value
```

**Final matcher consequence.** With coverage and similarity held at the top of the range —
which is exactly the case that matters, because the prose either side of the designator is
identical — `classify()` returned `EXACT_MATCH, "question text asks the same thing"` for an
ME-GI ask against an ME-GA question. The corpus holds 27 ME-GI, 46 ME-GA and 43 ME-LGI
mentions, so this is a live misallocation, not a theoretical one.

## B. Root cause

Not the tokeniser. Every designator token was emitted correctly, including `dsg:me-gi` and
`dsg:me-ga`, which carry the disagreement.

The fault is in `by_family`, inside `designator_conflict`. It read every designator token as
a family member. In mixed-case prose the acronym pass additionally emits the bare **family
head** — `ME-GI` yields `dsg:me` beside `dsg:me-gi` — and a separator-less token was assigned
its own body as its value, so `dsg:me` entered family `me` with the value `me`. Both sides
therefore held the pseudo-value `me`, the family intersection was non-empty, and the function
concluded the two sides had named the same member. The genuine `gi` / `ga` disagreement was
never reached.

The mechanism the Phase 2A-ii report predicted is the mechanism found. It is also more
general than ME-GI: bare `III/1` against `III/2` cancelled the same way through `dsg:iii`,
and was rescued only when a keyword slot such as "regulation III/1" happened to be present
to supply a second, uncontaminated family.

## C. The fix — conflict layer only

One rule, stated where the values are collected:

> A designator token names a **member** only when it carries a value distinct from its own
> family key. A token that merely names the family contributes no member.

A family named without a member can then neither create a conflict nor cancel one, which is
the same treatment already given to naming no designator at all: **silence is not conflict,
and naming the family is silence.**

Why the conflict layer and nothing else. The Phase 2A-i tokenisation is accepted work and
carries coverage and similarity as well as conflict; `dsg:me` and `dsg:megi` are load-bearing
*there* — `dsg:megi` is what lets an unhyphenated source spelling meet the MIW corpus spelling
`ME-GI`. Removing them from the tokeniser would have withdrawn real coverage in order to fix a
conflict bug. They are therefore still emitted, still matched, and merely no longer counted as
members. Controls assert the tokenisation is the behaviour Phase 2A-i left, designator by
designator.

## D. Full-sentence results after the repair

| Pair | Result | |
|---|---|---|
| ME-GI vs ME-GA | conflict | `PARTIAL_COVERAGE`, was `EXACT_MATCH` |
| ME-GI vs ME-GI | no conflict | `EXACT_MATCH` preserved |
| ME-GI vs ME-LGI | conflict | distinct engines, distinct answer |
| Form A vs Form B | conflict | unchanged |
| D-1 vs D-2 | conflict | `PARTIAL_COVERAGE` |
| G8 vs G9 | conflict | unchanged |
| III/1 vs III/2, with a keyword slot | conflict | unchanged |
| III/1 vs III/2, **without** a keyword slot | conflict | **was cancelling** |
| Tier II vs Tier III · A-60 vs A-0 | conflict | unchanged |
| **Annex VI vs Annex 6** | **no conflict** | `EXACT_MATCH` preserved |
| broad family "the ME engine" vs "the ME-GI engine" | no conflict | naming a family is silence |
| same-topic prose, no differing designator | no conflict | no false conflict |

## E. Gates

| Gate | Phase 2A-ii | Now |
|---|---|---|
| `validate_phase2.py` | 66 PASS / 0 FAIL | **66 PASS / 0 FAIL** |
| `test_oral_controls.py` | 287 / 0 | **315 / 0** (+28) |
| `mutate_phase2.py` | 25 / 0 escapes | **26 / 0 escapes** (+M19) |
| `check_determinism.py` | 10 artefacts / 0 | **10 artefacts / 0** (seeds 0, 1, 524287) |

No Phase 2A-i or Phase 2A-ii check was removed, weakened or renamed. The single Phase 2A-ii
control that pinned the defect is **flipped, not deleted**, so the repair is recorded where
the limitation was recorded.

**M19 — the defect restored.** The mutation re-admits the bare family head as a member,
which is the pre-repair behaviour exactly. It fails **five** controls: the ME-GI/ME-GA
sentence, the ME-GI/ME-LGI sentence, the keyword-less III/1 vs III/2 sentence, the
`classify()` assertion that an ME-GI ask is not awarded an ME-GA question at `EXACT_MATCH`,
and the flipped Phase 2A-ii control. Not one bare-designator control notices — which is
precisely why the sentence controls now exist. The failure is semantic: the harness reports
`315 controls / 5 failures`, not an exception, an import error or a non-zero exit from a
broken harness.

An earlier draft of M19 removed one line too many and produced a `SyntaxError` instead. That
is a caught mutation which proves nothing, and it was rewritten until it failed for the right
reason. Recorded because the Phase 2A-ii session met the same class of harness defect.

## F. Baseline and product — explicitly untouched

`ORAL_788_RECONCILIATION.jsonl`, `ORAL_788_RECONCILIATION_SUMMARY.json`,
`ORAL_GAP_CANDIDATES.json`, `HUMAN_REVIEW_QUEUE.json`, `ORAL_NOTES_COVERAGE.jsonl` and
`ORAL_NOTES_UNITS.jsonl` were SHA-256'd before the first gate ran and verified byte-identical
after the last: **NOT REGENERATED, NOT MODIFIED.** No Release-A dataset and no P0 dataset was
created. `check_determinism.py` regenerates by design, so it was run in a **disposable
detached worktree**, never against the working branch; both trees were clean afterwards and
the worktree was removed. `.gitattributes` is unchanged and `git add --renormalize` was not
run.

No live product file was modified: no QB page, no Oral Note, no examiner index, no SQ index,
no homepage, no payments or commercial file, no Written QI file, no magazine file.

## G. Deliberately not done

788 not recomputed · Release A not built · P0 not recomputed and no answer written ·
**GAP-0409 not adjudicated** — the repair unblocks it, adjudication belongs to the recompute ·
examiner-index V2 not generated · no connection published · governance items left to the
Founder, unchanged.

## H. Next

**Phase 2A-iii final recompute** — with the Phase 2A-i matcher, the Phase 2A-ii Notes layer
and this designator repair all frozen, recompute all 788 source occurrences deterministically
and produce the final Release-A connection set, the final P0 production batch, the movement
report against Phase 2, and the Laptop review package. The movement this repair causes is
deliberately not estimated here, because estimating it would mean recomputing the thing this
phase was told not to recompute.
