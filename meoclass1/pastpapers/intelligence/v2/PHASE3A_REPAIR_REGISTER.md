# Phase 3A — repair register

**RESEARCH ONLY.** `current_as_of: 2026-08-18`
Branch `research/question-intelligence-v2-phase3a`, from `origin/main` at `3b55bfb`.

---

## 0. A caveat the reviewer must read first

**The Laptop review document was not available to this session.** Branch
`review/question-intelligence-v2-phase2` was never pushed to origin, and commit
`7d8177b` is not a valid object in this clone. `git fetch --prune` was run; the
remote holds no review branch.

So `L-1` … `L-6` below are **reconstructed from the Founder's Phase-3A brief**,
which restates the findings, and from what the Phase-2 code turned out to be
doing when read. They are **not** quoted from the review. Where the code
disagreed with the brief, the code is recorded.

**Laptop must confirm this mapping before the register is treated as closed.**
If a seventh finding exists, or if any of these is narrower or wider than the
review meant, nothing downstream should be trusted until it is re-mapped.

---

## 1. The register

| | Finding | Severity | Artefact | Failure mechanism | Repair | Test | Status |
|---|---|---|---|---|---|---|---|
| **L-1** | Bank referential integrity incomplete | HIGH | `validate_families.py`, `OFFICIAL_BANK_ITEMS.json` | Only `C11` existed: an ancestor id had to appear in the curated file. Nothing checked the id against the item number, uniqueness, presence of text, or agreement with the 185-item extract. A wrong or edited ancestor passed. | Seven checks: `C29`–`C35`, `C39`. Curated text is compared byte-for-byte against the extract. | 6 bank mutations, all caught | **FIXED** |
| **L-2** | Extraction defect — item 182 scrambled | HIGH | `parse_dgs_question_bank.py` | Body lines sorted by `(page, -y)` only. Three fragments share baseline `y=145.5` on page 16 at `x0` 53.0 / 359.8 / 456.8; Python's stable sort left them in pdfminer container order, not left-to-right. | `x0` added to the sort key. | Whole-document scan: exactly one body row was mis-ordered. Re-extraction changes item 182 and nothing else; 184 byte-identical; 185/185 held. Corroborated by bank items 64 and 110. | **FIXED** |
| **L-3** | Prose metadata error — `(Oct-05)` on the wrong item | MEDIUM | `OFFICIAL_BANK_ITEMS.json`, `OFFICIAL_QUESTION_BANK.md`, `SOURCE_MANIFEST.json` | The extractor was correct; three write-ups said `BANK-4` where the annotation sits on `BANK-3`. A remembered fact with nothing deriving it. | Corrected in all three. | `C33` derives the carrier from the extract and asserts it is item 3 alone | **FIXED** |
| **L-4** | Similarity classifier deletes examiner command verbs | **CRITICAL** | `match_bank_to_corpus.py`, `negative_controls.py` | The stop-list held `give state explain list`, removed before comparison. There was no demand feature at all, so `describe` vs `criticise` differed by one token in a bag of thirty, and an actor inversion by none. | Five-feature stem model — demand, actor, polarity, numbers, lexis — in one shared classifier `qi_similarity.py`. Demand and actor can only demote. | 21 controls; 5 mutations, each breaking a control | **FIXED** |
| **L-5** | Short-stem protection not enforced at classifier level | HIGH | `match_bank_to_corpus.py` | The floor `len(set(tt)) < 4` lived in the sweep loop. Calling the classifier directly with `"Deviation"` returned `EXACT_OR_NEAR_VERBATIM`. Phase 2's NC-5 hid this by allowing four different outcomes. | Floor moved into `classify()`, returning `UNSCOREABLE_SHORT_STEM`. NC-5 now permits exactly one outcome. | NC-5 and AD-9; mutation "short-stem floor removed" breaks both | **FIXED** |
| **L-6** | Date confidence stored, not derived | **CRITICAL** | `validate_families.py` | `C21` compared `date_confidence` against `publication_status`. Editing both consistently promoted a family with no dated evidence. | `C36`–`C38` derive the date from evidence: a source of a date-bearing class, question banks excluded by construction, **and the current sitting excluded** — a paper is not evidence of an earlier one. | 5 date mutations that keep every field consistent and remove only the evidence; all caught | **FIXED** |

Two further defects were found in Phase 3A's own work and are recorded because
they were caught by the delta review rather than by inspection:

- `"Port State Control"` matched the command verb `STATE`, giving every PSC
  question a spurious demand and making `describe`/`criticise` read as compatible
  at 1.00. Regime phrases are masked before demand detection.
- MIW's mark annotations `(4)`, `(6)` were read as question quantities, demoting
  two true repeats (`QP2310-Q4`, `QP2406-Q3`). The bank prints no marks, so every
  marked modern stem conflicted with its own ancestor.

**F — the Prototype D / date-leak claim.** Phase 2 claimed more than its validator
proved. That is now true by construction rather than by assertion: the date gate is
`C36`–`C38`, and §13's requirement is met because a bank ancestor can never satisfy
it — `OFFICIAL_QUESTION_BANK` is in `NEVER_DATE_BEARING`.

---

## 2. Results

| | Phase 2 | Phase 3A |
|---|---|---|
| Classifier copies | 3 (drifted) | 1 |
| Similarity controls | 6 | **21** |
| Similarity mutations | 0 | **5, 0 escapes** |
| Validator checks | 96 | **151** |
| Validator mutations | 21 | **33, 0 escapes** |
| Bank-vs-corpus exact/near | 45 | **45 — identical set** |
| Bank-vs-corpus "strong" headline | 63 | 45 |
| QP2608 Paper DNA verified | 48/144 = 33.3% | **48/144 = 33.3%** |
| QP2608 incl. same-core | 58/144 | **58/144** |

The sweep headline moved because Phase 2's "63 strong" counted 45 exact/near **plus
18 pairs its own model document said adjudicate to `SAME_CORE_ASK`**. The exact/near
set is unchanged, nothing was gained, and no threshold was tuned to protect a
number. The Paper DNA reproduces exactly once the model's own short-stem
inheritance rule is applied.

---

## 3. Canonical storage for the DGS bank — recommendation

The bank PDF currently lives only at
`D:\MIW-Historical-QP-Intake\dgshipping\dgs_meo_cl1_written_questions.pdf`, outside
git, on one machine. It is the single most valuable source either phase found and it
is not preserved anywhere the Laptop can reach.

**Recommended path:** `meoclass1/pastpapers/sources/official/dgshipping/` —
alongside the existing historical-paper intake convention, under `pastpapers`, which
`.vercelignore` already keeps out of the deploy.

**Recommendation: do not commit the 314 KB binary yet.** Three things should be
settled first, and they are Founder calls, not mine:

1. whether `.gitattributes` should route it through LFS, as the repo does for other
   binaries;
2. whether official third-party PDFs belong in the repo at all, or in the separate
   intake tree with only the sha256 committed — which is what `SOURCE_MANIFEST.json`
   currently assumes;
3. that `.vercelignore` excludes the path before anything lands.

What is safe and useful now, and costs nothing: the **extracted text** is small,
diffable, reviewable, and is what every tool actually consumes. Committing
`dgs_meo_cl1_bank_items.json` (53 KB) to the research branch would let the Laptop
reproduce `C32` without the raw intake tree, which it currently cannot — the
validator reports those checks as **skipped**, loudly, on any machine lacking `D:`.

---

## 4. Not done in Phase 3A

Stated plainly so the reviewer does not have to infer it:

- The **Laptop review document** was never read (§0). The register may be wrong.
  *(Closed in Phase 3A.1: the review is on origin at `286c0c5` and was read in
  full. See `PHASE3A1_REPAIR_REGISTER.md`.)*
- **Section-by-section mapping** of the 1958 Act's Part XII duties onto the 2025 Act
  is not done. `FAMILY-EM-0009` — the casualty family — must not advance toward
  candidate use until it is. *(Phase 3A attached this gate to `FAMILY-EM-0008` in
  error; corrected in Phase 3A.1.)*
- The **832 archived MEO URLs** were not classified or mined. Phase 3B.
- No **candidate-facing publication** of anything.
