# Solved QP — learning-content quality triage

Internal. 2026-08-13, laptop team. Corpus at main `161c2b1`: 28 papers, 252
questions, 2,253 retrieval cards, 2,280 source entries.

Every number here is measured from the canonical specs, not estimated. The
purpose is to decide where enrichment actually pays, and — just as importantly
— to record which signals turned out to be worthless so nobody re-derives them.

---

## 1. Signals that turned out to be dead ends

Recording these first, because three of the five things one would naturally
triage on carry no information in this corpus.

| Candidate signal | Result | Verdict |
|---|---|---|
| Missing Understand | **252/252 present** | dead — the `fd0d9b4` pass closed it |
| Missing Study Guide | **252/252 present** | dead |
| Missing Answer Route | **252/252 present** | dead |
| Missing Recall cards | **0 questions have none** | dead |
| Answer over the 450–650 word band | **214/252 "fail"** | **useless as a defect signal** |

The word band deserves a sentence. It fires on 85% of the corpus, which means it
is not measuring a defect — it is measuring that the band was derived for a
different question shape than the one actually printed. It should be re-derived
per printed limb (already noted as an open item) and must not be used to select
questions for rewriting. An answer is not weak because it is long.

Two signals survive.

---

## 2. Signal A — retrieval-card overlength (the L-B3-3 item)

**Measured:** 79 of 2,253 cards exceed 90 words — **3.5%**. Corpus average card
length is **54 words**, which is healthy.

The problem is not corpus-wide. It is almost entirely two papers:

| Paper | Overlong | of cards | Avg card |
|---|---|---|---|
| **QP2408** | **46** | 72 | **100 w** |
| **QP2411** | **18** | 75 | 76 w |
| QP2511 | 6 | 86 | 55 w |
| QP2406 | 2 | 78 | 69 w |
| QP2412 | 2 | 110 | 56 w |
| *(9 others)* | 5 | — | — |

**64 of 79 overlong cards (81%) are in QP2408 and QP2411.** QP2408's average
card is 100 words against a corpus norm of 54 — it is not a corpus drift, it is
two papers authored to a different standard before §10.1 was written down.

### By card type

| Type | n | Avg | Over 90w |
|---|---|---|---|
| **procedure** | 275 | 62 w | **22 (8%)** |
| distinction | 337 | 58 w | 12 (4%) |
| regulation | 315 | 54 w | 14 (4%) |
| number | 214 | 53 w | 9 (4%) |
| definition | 306 | 53 w | 9 (3%) |
| trap | 541 | 52 w | 11 (2%) |
| structure | 265 | 48 w | 2 (1%) |

`procedure` is twice as likely to be overlong as any other type.

### Why they are long — three causes, only two of them defects

Read at source on QP2408-Q6, whose eight cards are the worst single cluster:

**Cause 1 — the route-recitation card (DEFECT).** `QP2408-Q6-C1`, 98 words,
prompt *"Give the route for the marine fuel standard, analysis and BDN
question."* The answer is fourteen numbered steps. This is not retrieval: no
candidate recalls fourteen items from one cue, and the content already exists as
`answer_route`, which has its own mode. A card that recites the route duplicates
a mode and teaches nothing. **These should not exist.** This is what makes
`procedure` the worst type.

**Cause 2 — two propositions in one card (DEFECT, splittable).**
`QP2408-Q6-C2`, 123 words, *"ISO 8217 or MARPOL — which one does what?"* carries
(i) the legal-status contrast — ISO 8217 is a commercial specification binding
only through the bunker contract, reg 18.3 is mandatory law — and (ii) the four
limbs of reg 18.3 quoted. Both are exam-critical; **deleting either loses
marks.** The fix is a split into two cards, not a trim.

**Cause 3 — a genuine list (NOT a defect — leave alone).** `QP2408-Q6-C3`, 133
words, *"What must a Bunker Delivery Note contain?"* is the ten mandatory items
of MARPOL Annex VI Appendix V. The examiner asks for the list; the candidate must
produce all ten. Ten limbs of one obligation are **one retrievable cluster**.
Splitting it destroys it and trimming it costs marks. Word count is simply the
wrong measure for this card.

This is precisely why the instruction was not to rewrite all 46 to a word target.
Roughly a third of the overlong cards are correct as they stand.

### The reusable rule

> **A retrieval card carries one prompt and one retrievable proposition — or one
> enumerated list that the examiner asks for as a list.**
>
> 1. If the answer contains two propositions that could be asked separately,
>    **split it**. Length is a symptom; the defect is the second proposition.
> 2. If the answer is a list the exam requires whole (Appendix V's ten BDN items,
>    the six elements of a framework), it is **one card however long**. Do not
>    trim it and do not split it.
> 3. **Never author a card that recites `answer_route`.** The route is a mode.
>    A `procedure` card tests one step or one decision, not the whole sequence.
> 4. Material that explains *why* belongs in Study Guide, not on the back of a
>    card. Move it rather than delete it.
> 5. Do not optimise to a word count. 90 words is a **review trigger**, not a
>    limit. The corpus norm of ~54 words is a consequence of rules 1–4, not a
>    target to hit.

### Work order (not done this session — see §5)

| Bucket | Est. cards | Action |
|---|---|---|
| Route-recitation `procedure` cards | ~22 | delete; route already exists as a mode |
| Two-proposition cards | ~35 | split into two |
| Genuine required lists | ~22 | **leave** |

The three buckets need reading card-by-card against the printed question. That is
authoring work with a verification gate, not a script.

---

## 3. Signal B — primary-source verification (feeds the True Source backlog)

**Measured from `sources[]` tier prefixes across all 252 questions:**

- 2,280 source entries recorded
- **57 questions (23%) carry at least one `P1_PRIMARY_VERIFIED` source**
- **195 questions (77%) carry none**

A question with zero P1 sources is not necessarily wrong — most rest on IMO
briefing material, class guidance or secondary summaries, which are often
adequate. It is a statement about *how much weight the answer can bear* if a
candidate is challenged, and about where a wrong gloss could survive unnoticed.

### Zero-P1 questions by topic — this IS the True Source demand map

| Primary category | Questions with no primary source |
|---|---|
| Statutory Framework & Class | **54** |
| Marine Insurance & Commercial Law | **40** |
| Human Element & Management | 38 |
| Alternative Fuels & Decarbonisation | 24 |
| Pollution Prevention & Response | 18 |
| Indian Maritime Legislation | 14 |
| Cargo & Bulk Carriage | 7 |

Human Element & Management is deliberately deprioritised in the backlog: much of
it is doctrine and good practice with no single instrument to cite, so a True
Source package would have little to capture. The first two rows are where a
compact package converts directly into defensible marks.

### Where both signals fire

Only four questions are both zero-P1 and carry three or more overlong cards:

| Question | Title | Overlong | Max card |
|---|---|---|---|
| QP2408-Q7 | Salvage Convention — award criteria | 7 | 132 w |
| QP2411-Q9 | Lubricating oil condition analysis | 5 | 107 w |
| QP2411-Q4 | SUA Convention — purpose, offences | 3 | 121 w |
| QP2411-Q5 | Salvage Convention 1989 — Articles | 3 | 131 w |

**Two of the four are Salvage.** That is the strongest single convergence in the
corpus and is why Salvage ranks first in the True Source backlog.

---

## 4. Mode-by-mode findings

- **Understand** — complete (252/252) and the standard is now written down. The
  `fd0d9b4` pass filled 13 and rewrote 6; those are now recorded in the
  candidate-facing ledger. No further systemic defect found.
- **Exam Plan / answer route** — present on all 252. The defect found is the
  reverse of a gap: the route is being *duplicated* onto retrieval cards.
- **Answer** — no reliable defect signal available. The word band is unusable
  (§1) and content defects have historically been found by targeted review
  against primary sources, not by metrics. This is the argument for the True
  Source backlog rather than for a metric-driven rewrite.
- **Study Guide** — present on all 252. It is also the correct destination for
  the explanatory material currently overloading recall cards.
- **Recall** — the one measurable defect, concentrated in two papers (§2).

---

## 5. What this session changed, and what it did not

**Changed:** nothing in the learning content. The four candidate-facing content
changes shipped this session were the *backfilled ledger entries* describing
corrections that had already shipped — not new edits to answers.

**Deliberately not changed:** the 79 overlong cards. Reading QP2408-Q6 showed
that a third of them are correct as authored, and that the two real defect
classes need different treatments. Rewriting 46 cards to a word target would
have destroyed the Appendix V list card and left the route-recitation cards in
place — worse content, better metric. The rule in §2 has to be applied
card-by-card against the printed question, with the same verification gate any
answer edit gets.

**Recommended next tranche:** QP2408 first (46 cards, avg 100 w, worst single
cluster), then QP2411 (18). Delete the route-recitation cards, split the
two-proposition cards, leave the required lists, and record the result as a
`learning_improvement` changelog entry per paper so candidates see it.
