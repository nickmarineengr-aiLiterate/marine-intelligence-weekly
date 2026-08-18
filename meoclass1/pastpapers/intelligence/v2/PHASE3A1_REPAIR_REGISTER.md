# Question Intelligence V2 — Phase 3A.1 repair register

**RESEARCH ONLY. Nothing here is candidate-facing.**
`current_as_of: 2026-08-18`

This register is built from the **actual Laptop review**, read in full from
`origin/review/question-intelligence-v2-phase3a` at commit `286c0c5`
(`review/LAPTOP_PHASE3A_INDEPENDENT_REVIEW.md`, 929 lines). It does **not**
reuse Desktop's earlier reconstructed L-numbering, which the review itself
showed to be shifted. Laptop's own ids are used throughout.

Every row was reproduced on this machine before it was repaired, and every row
is closed by an executable test rather than by assertion.

---

## 1. The register

| ID | Laptop finding | Affected code / data | Severity | Repair | Test | Status |
|---|---|---|---|---|---|---|
| **§O** | Four hardcoded `D:` paths. Two tools would not run at all on Laptop; the worst was `SPECS`, an absolute path to **committed repository content** two directories above the tool. | `validate_families.py`, `match_bank_to_corpus.py`, `parse_dgs_question_bank.py` | **BLOCKER** | One resolver, `tools/qi_paths.py`, derives every path from its own location. `parse_dgs_question_bank.py` takes `--pdf`. | Whole suite run from a clean worktree with the `D:` drive hard-blocked by an audit hook | **FIXED** |
| **§N** | The bank extract was outside git, so `C32`/`C33` skipped silently and one bank mutation escaped on the integration authority's machine. | `EXTRACTED_BANK` | **BLOCKER** | 185-item extract committed under `pastpapers/sources/official/dgshipping/`; sha256 and byte count recorded in the manifest. | Validator reports 200 checks, **0 skipped**, from the clean worktree | **FIXED** |
| **P3A-1** | `demand_compatibility` aggregates with `max()`. `{DESCRIBE, RESPONSIBILITY}` vs `{CRITICISE, RESPONSIBILITY}` → **1.00**. L-4 re-entering through a side door. | `qi_similarity.demand_compatibility` | **HIGH** | Primary command and secondary task type scored as separate dimensions, combined with `min()`. No verb pair named. | `P31-D1`…`P31-D6`; mutation *demand aggregated with max() again* | **FIXED** |
| **P3A-2** | Regime masking covered only `state of the art`, so `state of readiness` yielded a spurious `STATE`. | `qi_similarity._REGIME_PHRASES` | **MEDIUM** | Any `state of <something>` is masked. | `P31-D6`; mutation *regime masking removed* | **FIXED** |
| **P3A-3** | No negation / requirement polarity. `required` vs `not required` → `NEAR_VERBATIM`. | `qi_similarity` | **MEDIUM-HIGH** | `requirement_polarity()` reads REQUIREMENT / PERMISSION / APPROVAL / COMPLIANCE / FORCE from the raw text, anchored to rule words, with forward-looking modals. | `P31-N1`…`P31-N6`; mutation *negation removed* | **FIXED** |
| **P3A-4** | `numbers()` covered only integers 1–20 and mangled decimals. `0.50` vs `0.10` → `EXACT_REPEAT`. | `qi_similarity.numbers` | **MEDIUM** | Magnitudes typed by dimension (percent, ppm, volt, pressure, temperature, time period, decimal, year) and compared within a dimension. | `P31-M1`…`P31-M5`; mutation *numbers narrowed back to 1–20* | **FIXED** |
| **P3A-5 / LC-3** | The validator proves an ancestor *exists*; nothing proved it is the *right* one. Two families could swap ancestors with every id still real. | `validate_families.py` | **MEDIUM** | `C40` occurrence ancestors within the family declaration; `C41` representative fit ≥ `SAME_CORE_ASK`; `C42` no undeclared bank item fits better. | Mutations *swap the ancestors of two families*, *replace a correct ancestor with a different valid curated item* | **FIXED** |
| **P3A-6 / LC-5** | `raw_stem` unvalidated against the source spec, while actor is load-bearing in the classifier. | `validate_families.py` | **LOW-MEDIUM** | `C43` every `raw_stem` matches the text its own spec prints; `C43b` holds the unverifiable set to an explicit budget of 4. | Mutation *corrupt a preserved historical stem (invert the actor)* | **FIXED** |
| **§S** | `MERCHANT_SHIPPING_ACT_AUTHORITY.md` §5 and `PROTOTYPE_EVIDENCE_CLASSES.md` attach **EM-0009**'s casualty data to **EM-0008**. The Part XII gate was on the wrong family. | two write-ups | **MEDIUM** | Both corrected; gate re-attached to EM-0009. `C44` guards the prose. | Two document mutations restoring the exact live defect | **FIXED** |
| **§V** | The Coastal Shipping Act, 2025 is omitted from a document titled *primary authority* on what survives repeal. | `MERCHANT_SHIPPING_ACT_AUTHORITY.md` | **MEDIUM** | New §5A (both repeals) and §5B (Part XIV disambiguation). | n/a — documentary | **FIXED** |
| **L-3** | H1–H5 filenames assert `JUN2010`, `DEC2011`, `OCT2012`, `APR2010`, `MAR2010` — dates the model refuses to assert. Unrepaired since Phase 2. | `verification/` | **MEDIUM** | Renamed to their subject matter; headings state the date's status. | `C45`; mutation *re-date an evidence filename* | **FIXED** |
| **§L** | `SOURCE_MANIFEST.json` credits the Oct-05 derivation to `C29`; it is `C33`. | manifest, `OFFICIAL_QUESTION_BANK.md` | **LOW** | Corrected. | n/a | **FIXED** |
| **§Z** | `CANDIDATE_BLOCK_PROTOTYPES.md` still carries the superseded Phase-2 Prototype 3 with no cross-reference. | that file | **LOW** | Marked superseded in part, pointing at `PROTOTYPE_EVIDENCE_CLASSES.md`. | n/a | **FIXED** |
| **§W** | Two candidate-facing findings: W-1 Part XIV called "limited savings"; W-2 "Part XIV" carries two meanings across products. | `oralnotes/`, `QB*.html` | **MINOR / LOW** | Recorded in `CURRENT_ANSWER_CORRECTION_CANDIDATES.md`, re-verified against the live files. **Nothing edited.** | n/a — Laptop decides candidate repair | **RECORDED** |
| **§G** | `Company` is not in `ACTORS`, and Company/Master and Company/DPA are ISM-central. | `qi_similarity.ACTORS` | **LOW** | **NOT DONE** — see §4. | — | **OPEN, deliberate** |

---

## 2. What was found here that the review did not name

**A near-miss worth recording, because the next reviewer will hit it too.**
The first draft of the ancestor-fit check (P3A-5) reported `FAMILY-EM-0004` as
misattached: four of its five occurrences have nothing to do with its declared
`BANK-072`, and two reproduce `BANK-085` verbatim. That reading was **wrong**.
The family already declares `secondary_bank_ancestor: BANK-085`, and the
two-ancestor model is deliberate and documented — the warranties limb recurs
against BANK-085 in 2021 and 2022, while its *current* recurrence is limb (b)
of QP2608-Q4, whose parent is BANK-072. The check now reads the declared set,
and **no family data was changed**. A check that had not read the secondary
field would have manufactured a defect and "repaired" correct data.

**A portability defect the review could not have seen.** The extract was first
committed with CRLF while the repository's own `.gitattributes` pins `*.json`
to `eol=lf`. The sha256 recorded in the manifest therefore described bytes no
checkout would ever produce, and Laptop would have verified the provenance hash
against a 53,194-byte LF file and been told the official source had been
tampered with. Hash and byte count now describe the LF form every platform
checks out, and this is verified from the clean worktree.

---

## 3. Numbers, before and after

| | Phase 3A on Laptop | Phase 3A on Desktop | **Phase 3A.1, clean worktree, `D:` blocked** |
|---|---|---|---|
| Validator checks | 166 | 169 | **200** |
| Skipped | **2** | 0 | **0** |
| Failures | 0 | 0 | **0** |
| Validator mutations | 33 | 33 | **39** |
| Mutation escapes | **1** | 0 | **0** |
| Similarity controls | 21 | 21 | **38** |
| Control failures | 0 | 0 | **0** |
| Classifier mutations | 5 | 5 | **9** |
| Classifier escapes | 0 | 0 | **0** |
| `D:` paths in tools | 4 | 4 | **0** |

### The measurement sets did not move

| | Before | After |
|---|---|---|
| Sweep rows | 96 | 96 |
| exact / near | **45** | **45** |
| same core ask | **37** | **37** |
| reportable | 82 | 82 |
| Class changes | — | **0** |
| QP2608 exact/near | 48 / 144 = 33.3% | **48 / 144 = 33.3%** |
| QP2608 inclusive | 58 / 144 = 40.3% | **58 / 144 = 40.3%** |

**Not one of the 96 sweep rows changed class** across all four classifier
repairs. That is the honest result and it is worth stating plainly: the holes
closed were real, demonstrably real — every one reproduces on demand as a
mutation — but none of them was occupied by the verified corpus. The 45 was not
protected; it was recomputed and it did not move.

---

## 4. Not done in Phase 3A.1, and why

- **`Company` and `Administration` actors (§G).** Adding actors changes the
  classifier's behaviour on a corpus nobody has adjudicated yet, and §43 of the
  brief forbids adding features in a hardening pass. `Administration` is
  arguably already covered by `FLAG_STATE`. Recorded as open.
- **`EXPLAIN` vs `LIST` adjudicates to `TOPIC_ONLY`** (control `P31-D2`,
  demand 0.40). This is pre-existing taxonomy calibration, not a Phase-3A.1
  change, and the review did not flag it. It is demote-only and therefore safe.
  Flagged here rather than tuned to taste.
- **Coastal Shipping Act commencement.** No notification located. §5A therefore
  does **not** claim Part XIV is already gone.
- **The 1958 Part XII → 2025 Act section mapping.** Phase 3B. The gate stays,
  now on `FAMILY-EM-0009`.
- **Candidate-facing repair of W-1 and W-2.** Laptop's call, not Desktop's.
- **Phase 3B ingestion.** Not started. No historical paper was ingested.
