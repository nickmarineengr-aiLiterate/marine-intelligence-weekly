# DESKTOP QP ALLOCATION BOARD

**The standing production board for the desktop team, across every batch.**
Created 2026-08-12, in the session that published QP2512.

Batch 1 was allocated on a 2024-only board,
[`DESKTOP_QP_ALLOCATION_2024.md`](DESKTOP_QP_ALLOCATION_2024.md). That file is
**kept unchanged as the Batch 1 record** — it holds the rationale, the dependency
warnings and the baseline hash for six papers that are already owned. It is not
superseded and it is not edited.

This board exists because **Batch 2 is not a 2024 batch.** Five of its six papers
are 2025 sittings, so a file named for a year could not hold it without lying in
its own title. Everything not restated here — branch model, artefact rules, the
stop gate — is inherited from Batch 1's board and from
[`DESKTOP_QP_PRODUCTION_PLAYBOOK.md`](DESKTOP_QP_PRODUCTION_PLAYBOOK.md), which
remains the method. Where this board and
[`PARALLEL_PRODUCTION_BOARD.md`](PARALLEL_PRODUCTION_BOARD.md) differ on branch
model or repository rules, **PARALLEL_PRODUCTION_BOARD wins.**

---

## 1. CORPUS TRUTH AT BATCH 2 ALLOCATION

Verified 2026-08-12, after QP2512 was completed and published:

| | |
|---|---|
| Corpus | **252 questions / 126 solved / 126 unsolved** — the halfway point |
| Papers | 28 — **14 solved**, 14 answerless intake |
| 2024 | 11 papers — 2 solved (QP2403, QP2404), 9 unsolved |
| 2025 | 11 papers — 6 solved, **5 unsolved** |
| 2026 | 6 papers — **all solved** |
| Reuse map | current: `build_reuse_map.py --check` reports "reuse map and source inventory are current" |

May is absent from the MIW source set in all three years. There is no `QP2405`,
`QP2505` or `QP2605`.

---

## 2. BATCH STATUS SUMMARY

| Batch | Papers | Owner | Status |
|---|---|---|---|
| **1** | QP2401 · QP2412 · QP2402 · QP2409 · QP2411 · QP2410 | DESKTOP | **IN FLIGHT** — five of six branches pushed to `origin`, none merged. See §6 |
| **2** | QP2501 · QP2502 · QP2503 · QP2504 · QP2507 · QP2406 | DESKTOP | **ALLOCATED — NOT STARTED** |
| **3** | QP2407 · QP2408 | *unallocated* | held back — see §5 |

Batch 3 is **two papers, not three.** That is a result of the Batch 2
selection, not a leftover.

---

## 3. BATCH 2 — THE SIX PAPERS

Branch for each: `pastpapers/qp####-founder-review`.

**Baseline for all six: the `main` commit that published QP2512** — recorded in
§7. Not `9c97359`, which was Batch 1's baseline and predates the QP2512 content,
the publish-state fix, the storefront trim and the whole SolvedQP manifest,
search and health system. A Batch 2 paper branched from `9c97359` would rebuild
product surfaces from a stale inventory.

| # | Paper | Sitting | Branch | Tier D *at its turn* | Family reach | Temporal flags | Dependency |
|---|---|---|---|---|---|---|---|
| **1** | **QP2501** | January 2025 | `pastpapers/qp2501-founder-review` | 0 / 9 | 3 | 2 — **0 HIGH** | **must precede #5** |
| **2** | **QP2502** | February 2025 | `pastpapers/qp2502-founder-review` | **3 / 9** | 4 | 2 (1 HIGH) | supplies #6's only donor |
| **3** | **QP2503** | March 2025 | `pastpapers/qp2503-founder-review` | 1 / 9 | 5 | 3 (2 HIGH) | **must precede #5** |
| **4** | **QP2504** | April 2025 | `pastpapers/qp2504-founder-review` | **5 / 9** | 3 | 4 (1 HIGH) | needs #1–#3; supplies #6 |
| **5** | **QP2507** | July 2025 | `pastpapers/qp2507-founder-review` | **8 / 9** | 8 | 2 (1 HIGH) | **HARD: never before #1 and #3** |
| **6** | **QP2406** | June 2024 | `pastpapers/qp2406-founder-review` | 1 / 9 | 2 | **0** | needs #2 and #4 |

**Owner (all six):** `DESKTOP CORPUS/QP TEAM`
**Status (all six):** `ALLOCATED — NOT STARTED`
**Corpus dependency:** none blocking.

`Tier D at its turn` is the count **as it will stand when that paper is
reached**, having solved everything before it in this order. It is not today's
count, and for QP2504 and QP2507 the difference is most of the paper.

---

## 4. WHY THESE SIX, AND IN THIS ORDER

Recomputed from `specs/*.json` through `recurrence_model.py` — the same
derivation `build_reuse_map.py` uses — under a **simulated built set that
assumes Batch 1 is complete** (180 answers, not today's 126). The stale
allocation note recommending QP2502 at "tier D 2/9, family reach 5" was not
carried forward; QP2502 is now **3/9**, because Batch 1's QP2402 creates a Q1
donor that did not exist when that note was written.

### 4.1 Taking all five 2025 papers closes a year

After Batch 2, **2025 is complete: 11 of 11.** 2026 is already complete. The
Founder's stated priority is to finish 2024 and 2025 quickly, and a whole
finished year is worth more to the product than six scattered papers — the year
sheet stops being partial and the coverage grid loses a column of dashes.

### 4.2 QP2507 is the largest readiness conversion in the corpus

QP2507 has **zero** verified donors today and the **highest family reach
anywhere at 8** — the combination that Batch 1's board correctly refused to
start from. What the recomputation adds is *where that reach points*:

```
QP2507-Q1 -> QP2501-Q1     QP2507-Q5 -> QP2503-Q5
QP2507-Q2 -> QP2501-Q7     QP2507-Q6 -> QP2503-Q3
QP2507-Q4 -> QP2501-Q9     QP2507-Q7 -> QP2503-Q2
                            QP2507-Q8 -> QP2503-Q1
                            QP2507-Q9 -> QP2503-Q9
```

**All eight edges land inside QP2501 and QP2503.** Solve those two and QP2507
goes from 0/9 to **8/9**. That is why it is in this batch and why its position
is a hard constraint rather than a preference: taken before them it is the
worst paper in the corpus; taken after them it is the best.

### 4.3 The order is provably optimal, and it is the calendar

Eighteen of the batch's fifty-four questions arrive with a verified donor in
this order. Exhaustive evaluation of all **720** orderings shows 18 is the
**maximum**. Started cold — no ordering benefit at all — it would be 6.

This is the first batch where calendar order happens to *be* the optimal order.
That is a coincidence of this particular donor graph and must not be read as a
rule; Batch 1's optimum was emphatically not chronological.

### 4.4 QP2406 is the sixth, and the choice was close

Only three 2024 papers remain, and all three finish at **1/9 with reach 0**
whichever is taken — their donors come from 2025 and 2026, never from each
other, so there is no mid-2024 block to keep intact. The tie is broken on
temporal risk:

| | Tier D | Reach | Flags |
|---|---|---|---|
| **QP2406** June 2024 | 1/9 | 2 | **0** |
| QP2407 July 2024 | 1/9 | 1 | 1 (HIGH) |
| QP2408 August 2024 | 1/9 | 0 | 2 (1 HIGH) |

QP2406 is **the only paper left in the entire corpus with zero temporal
flags**, and its single donor is created inside this batch by QP2502 and
QP2504 — research transferred while it is still warm, the same reasoning that
put QP2412 second in Batch 1.

### 4.5 What was deliberately not optimised for

Calendar contiguity was **broken on purpose** at position 6. Batch 1's main
finding was that contiguous sittings share a regulatory line and should be
researched together. That still holds — positions 1 to 4 are a contiguous
January–April 2025 block for exactly that reason — but it does not apply to
QP2406, because the mid-2024 papers no longer form a block in any sense that
pays: they share no donors, and June 2024's regulatory line is not established
by anything else in this batch.

---

## 5. HELD BACK — BATCH 3

| Paper | Sitting | After Batch 2 | Why held |
|---|---|---|---|
| **QP2407** | July 2024 | 1/9, reach **0**, 1 HIGH flag | Same donor count as QP2406 and strictly worse temporally. Its reach is fully consumed by QP2502 |
| **QP2408** | August 2024 | 1/9, reach **0**, 2 flags (1 HIGH) | Weakest paper in the corpus. Reach 0 in every scenario tested; it neither receives from nor gives to anything in Batch 2 |

Deliberately **not** held back: **QP2507**, despite 0/9 donors today. Deferring
it past this batch would force the January and March 2025 regulatory line to be
established twice, months apart — the precise cost the contiguous-block rule
exists to avoid.

---

## 6. BATCH 1 — CURRENT STATE (2026-08-12)

Read from `origin`, not from the Batch 1 board's expectations.

| Paper | Branch on `origin` | Head | Merged to main |
|---|---|---|---|
| QP2401 | present | `37af6d4` | no |
| QP2402 | present | `af5a8d9` | no |
| QP2409 | present | `6ca65d9` | no |
| QP2411 | present | `2cc73be` | no |
| QP2412 | present | `48badc3` | no |
| QP2410 | **not yet pushed** | — | no |

Five of six branches exist and none has been integrated. **The six-paper stop
gate has not been reached**, so Batch 2 must not begin before Batch 1 is
complete and handed back. Batch 2 is allocated, not open.

The laptop has **not** reviewed or integrated any Batch 1 branch. That work,
and all global regeneration, remains laptop-owned and one paper at a time.

---

## 7. BASELINE AND ARTEFACT RULES

| | |
|---|---|
| **Batch 2 baseline** | `main` at **`333e814`** — the QP2512 publication commit |
| Baseline contents | QP2512 live · 14 papers / 126 questions · publish-state fix · storefront trim · SolvedQP manifest, search and daily health |
| MIW remote | `github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly` — **PUBLIC** |
| Corpus remote | `github.com/nickmarineengr-aiLiterate/RulesApp-Local-Input` — **PRIVATE** |

### 7.1 How the baseline hash was recorded

The baseline is the commit that published QP2512 and built the derived layer. A commit cannot
contain its own hash, so `333e814` is written in by a small follow-up metadata commit whose
**parent is the baseline** — the same self-verifying pattern Batch 1 used:

```bash
git -c safe.directory=* cat-file -p HEAD^{commit} | head -2   # on the metadata commit
# its 'parent' line must read 333e814...
```

Branch every Batch 2 paper from `333e814` — not from the metadata commit, and not from the
branch head, which moves as the laptop integrates Batch 1.

A paper branch **owns** its spec, its verification records, its anchor and
checkpoint evidence, and its review HTML.

A paper branch must **NOT** commit any global derived artefact. That list has
grown since Batch 1 and now includes the delivery manifest:

> the reuse map · the reverse-hint queue · recurrence indexes ·
> `pastpapers_content_index.json` · **`solvedQP/solvedqp_content_index.json`** ·
> `questions-YYYY.html` · `topics-YYYY.html` · `solvedQP/*` · any other paper's
> HTML · `CURRENT_STATUS.md` · `history/SESSION_HISTORY.md` · sample and
> product counts

The toolchain **will** regenerate several of these during QA. Validate with
them, then **revert them before committing.**

---

## 8. STANDING TEMPORAL ANCHORS FOR BATCH 2

Every Batch 2 sitting predates **15 March 2026**, when the Merchant Shipping
Act, 2025 commenced and repealed the 1958 Act by s.324(1). The 1958 Act governs
throughout, and every donor pulled back from a 2026 answer must have its
statute reference reversed, not inherited.

- **QP2406 (June 2024)** falls after the **33rd IMO Assembly**, whose
  resolutions were adopted **6 December 2023**. The `A.11xx(33)` editions are
  operative for it.
- **All five 2025 papers** fall *before* the **34th IMO Assembly**, adopted
  **3 December 2025**. `A.1206(34)` and every other `A.1xxx(34)` is **after**
  every Batch 2 sitting and must not appear as operative in any of them. For
  port State control that means `A.1185(33)` is the operative edition — which
  is *wrong as current law and right for these papers*, and is exactly why the
  daily health check does not apply current-law trap rules to historical
  sittings.

An Assembly boundary is the **adoption date**, not the meeting month.

---

## 9. THE STOP GATE, RESTATED

When all six Batch 2 papers are complete and pushed:

> # STOP DESKTOP PRODUCTION.

Do not select a seventh. Do not merge to `main` or any integration branch. The
six pushed Founder-review branches are handed back to the laptop team.

**Do not start any Batch 2 paper while Batch 1 is open.**
