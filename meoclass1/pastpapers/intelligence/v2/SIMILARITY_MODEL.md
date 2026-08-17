# Similarity model — QI-v2

**RESEARCH ONLY.** `current_as_of: 2026-08-17`
Class baseline locked by the Laptop review. Phase 2 changes the *measurement*, not
the classes.

---

## 1. The five classes (locked)

| Class | Definition | Candidate-facing? |
|---|---|---|
| `EXACT_REPEAT` | Identical stem but for the normalisation in §2 | yes, at HIGH |
| `NEAR_VERBATIM` | Same question; small wording or presentation changes | yes, at HIGH |
| `SAME_CORE_ASK` | Wording materially changed; substantially the same answer required | yes, at HIGH |
| `TOPIC_ONLY` | Same subject area, different examination task | **never as "repeated"** |
| `NO_MEANINGFUL_MATCH` | No defensible recurrence | n/a |

`TOPIC_ONLY` is not a repeat and must never be surfaced as one. It is the class that
inflates recurrence statistics if allowed to drift.

The classifier **proposes**. Human or Claude adjudication **confirms**. Semantic or
vector similarity may never publish a family on its own.

---

## 2. Normalisation — what may be discarded

The Laptop accepted `QP2608-Q8(b)` as `EXACT_REPEAT` despite *on board* / *onboard*
and punctuation differences, so the rule is now stated explicitly rather than left
to judgement.

**Safe to normalise away** — presentation only:

- case
- runs of whitespace
- punctuation variance, including a trailing `?` on a non-question
- hyphenation and spacing variance where semantic identity is obvious
  (`lay-up` / `layup`, `on board` / `onboard`, `co-operation` / `cooperation`)
- curly versus straight quotes
- regular plurals

**Never normalise away** — these are the question changing:

- a different command verb — `differentiate` → `write short notes` is a real change
- a different legal qualifier
- a different scenario condition, **including one that is merely added**
- different numbers
- different marks
- an added or removed substantive limb

The second list is why `QP2608-Q4(b)` is `SAME_CORE_ASK` and not `EXACT_REPEAT`
(the command weakened from *differentiate … with an example* at 8 marks to
*write short notes* at 4), and why `QP2608-Q8(a)` is `SAME_CORE_ASK` even though
its ancestor sits inside it whole.

---

## 3. What Phase 2 changed — measure containment in **both** directions

Phase 1 measured how much of the modern question appears in the historical one.
That is one-directional, and it **missed real ancestors**.

For a candidate pair, over content tokens after normalisation:

```
fwd = |modern ∩ historical| / |modern|        how much of the modern text is old
rev = |modern ∩ historical| / |historical|    how much of the old text survives
```

| `fwd` | `rev` | Proposed class |
|---|---|---|
| ≥ 0.85 | ≥ 0.85 | `EXACT_REPEAT` / `NEAR_VERBATIM` |
| < 0.85 | ≥ 0.85 | **`ANCESTOR_ABSORBED_AND_EXTENDED`** → adjudicates to `SAME_CORE_ASK` |
| ≥ 0.85 | < 0.85 | **`ANCESTOR_NARROWED`** → adjudicates to `SAME_CORE_ASK` |
| max ≥ 0.65 | | `SAME_CORE_ASK` candidate |
| max ≥ 0.45 | | `TOPIC_ONLY` candidate |
| otherwise | | `NO_MEANINGFUL_MATCH` |

The two named middle cases are the Phase-2 addition, and they are not cosmetic:

> **`QP2608-Q8(a)` scores `fwd 0.48`** — a one-directional test discards it —
> **and `rev 0.96`.** Its ancestor `BANK-105` sits inside it almost entirely;
> August 2026 then wraps it in a PSC-failure scenario, an initial-meeting setting
> and a demand for examples. Phase 1 recorded this limb as having no ancestor.
> It has one, and it is 10 of the paper's 144 marks.

`ANCESTOR_NARROWED` is the mirror case: the modern question asks a strict subset of
the older one.

Both middle cases adjudicate to `SAME_CORE_ASK`, never to `EXACT_REPEAT` — because
in both, something substantive was added or removed, and §2 forbids discarding that.

---

## 4. The short-stem guard

A stem of one or two words scores `fwd = 1.00` against almost anything that mentions
it. `QP2608-Q4(b)` is the single word **“Warranties”**.

**Rule.** A stem with fewer than **three distinct content tokens** after
normalisation is classed `UNSCOREABLE_SHORT_STEM`. It may not carry a similarity
class of its own. It **inherits** its parent question's class, and the inheritance
is recorded on the occurrence.

Without this guard the four one-word limbs of `QP2608-Q4` would each have reported
containment 1.00 and manufactured four spurious exact repeats.

---

## 5. Confidence — three fields, never one

Phase 1 carried a single `confidence`. It conflated three independent things and has
been split. A family may now correctly read **HIGH / NONE / HIGH**.

| Field | Answers |
|---|---|
| `text_similarity_confidence` | how sure are we the two stems are the same question? |
| `date_confidence` | how sure are we *when* the earlier one was set? |
| `source_confidence` | how good is the source the earlier text came from? |

`FAMILY-EM-0001` is the worked example: `HIGH` text (containment 1.00/1.00 against
an official bank item), `NONE` date (the bank is undated and no sitting is proven),
`HIGH` source (the Directorate's own publication). All three at once, and none of
them contradicting the others.

| Label | Requires |
|---|---|
| `HIGH` | both stems read as text, from sources of known identity |
| `MEDIUM` | stems compared but one side's authority is soft |
| `LOW` | assertion only — a recurrence table, a recollection, a topic argument |
| `NONE` | no evidence of this kind at all |
| `UNSCOREABLE_SHORT_STEM` | §4 applies; the class is inherited |

---

## 6. Provenance tier — kept separate from confidence

| Tier | Meaning |
|---|---|
| `OFFICIAL_BANK_ANCESTOR` | the wording is fixed by the Directorate's own published question bank |
| `MIW_TEXT_VERIFIED_OCCURRENCE` | both stems read from MIW's own verified holdings |
| `EXTERNAL_TEXT_VERIFIED_RECURRENCE` | one stem read from a third-party text source |
| `DIESELSHIP_ASSERTED_OCCURRENCE` | provider metadata asserts a sitting; no text was seen |

`OFFICIAL_BANK_ANCESTOR` is new in Phase 2 and is the highest tier. It is also the
tier that most needs its date column read: it is the strongest evidence of
*ancestry* in the whole layer and it carries **no date at all**.

---

## 7. Negative controls

`tools/negative_controls.py` — **6 of 6 hold**:

| Control | Pair | Required | Result |
|---|---|---|---|
| NC-1 | motivation family, true positive | `EXACT_OR_NEAR_VERBATIM` | 0.94 / 0.94 — pass |
| NC-2 | cargo abandonment vs abandonment of ship / wreck | `NO_MEANINGFUL_MATCH` | 0.00 / 0.00 — pass |
| NC-3 | motivation-as-a-topic vs the motivation family | not a match | 0.35 / 0.23 — pass |
| NC-4 | dry dock coordination vs dry dock project planning | not a match | 0.12 / 0.15 — pass |
| NC-5 | one-word “Warranties” vs the differentiate form | narrowed, not exact | 1.00 / 0.08 — pass |
| NC-6 | lay-up reactivation vs lay-up preservation (inverse ask) | not a match | 0.13 / 0.27 — pass |

NC-2 is the standing semantic false positive the Laptop required be kept.
**NC-3, NC-4 and NC-6 are new in Phase 2**, and each guards a trap the official bank
introduced by bringing near-neighbours of our families into the same corpus:
`BANK-061` discusses *attitude and motivation development* but is not the motivation
family; `BANK-164` is about dry-docking but is not the coordination question.

NC-5 shows the model reporting an honest `ANCESTOR_NARROWED` on a stem that the
short-stem guard then refuses to let stand alone.

---

## 8. Limits

- Containment is **lexical**. It will miss a genuine recurrence that has been fully
  reworded, and it has no notion of meaning. It proposes; it does not decide.
- The stop-list and the crude singulariser are tuned to this corpus and are not
  general.
- A high score against the official bank says the *question* recurs. It says
  nothing about whether the *answer* still holds — that is
  `TEMPORAL_DELTA_SCHEMA.json`, and it is a separate question by design.
