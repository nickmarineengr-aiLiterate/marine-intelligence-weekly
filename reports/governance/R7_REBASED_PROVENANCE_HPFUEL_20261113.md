# R-7: decision note on rebased-correction provenance (written before implementation)

| | |
|---|---|
| **Date** | 13 Nov 2026 |
| **Authority** | FOUNDER-DECISION-R7-R8-20261113, §2 (Option B, conditional). Local only; no push. |
| **Scope** | Exactly one record: `tools/oral/correction_corr_safety_hpfuel_pipe_20261022_manifest.json` (CORR-SAFETY-HPFUEL-PIPE-20261022) |

## 1. Verified facts

| Fact | Evidence |
|---|---|
| The original record is in `c2118cc7a18b37ddef3d852bb0c1f80bb7973c30`, committed 2026-10-23 01:46:49 +0530 (author date identical). The record blob is `d30bc748af5a7d5d324b299d39c9ad95ee428370`. | `git cat-file -p c2118cc` |
| The annotated tag `frozen/safety-hpfuel-pipe-qualified-candidate-20261022` is dated 2026-10-23 06:43 +0530. The October job root `MIW-QB-HPFUEL-CORR-20261022` sits outside the repository. | `for-each-ref`, reflog. Corroborating only. |
| **`c2118cc` is NOT in the release repository.** GitHub `main` = `ad7cd3d` has no HPFUEL tag, and `c2118cc` is not an ancestor of `ad7cd3d` or `3710538`. | `ls-remote`, `merge-base --is-ancestor` |
| The ancestry of `c2118cc` holds five unreleased RulesApp commits, among them `c145294..bf14420` and `446e726`, "PROPOSED close XP-RULESAPP-FALLS-01". | `git log ad7cd3d..c2118cc` |
| In the candidate, the record first appears in `8e7eff905eac95a2e641ef7c2fc8045831bbecca` (2026-11-12 14:08 +0530), which carries the trailer `(cherry picked from commit c2118cc7…)`. | `git log --diff-filter=A` |
| **It is logically the same correction.** Every field except `founder_authorisation`, `baseline_commit`, `governing_commits` and `note` is identical: `correction_id`, `date`, `title`, `cards`, `artefacts`, `propagation`, `invariants`, `review`, `status`, `kind`, `origin`, `candidate_*`, `authority`, `authorisation_source` and `known_traps_entries`. The four changed fields are the documented 12 Nov rebind, and `note` keeps the original SHAs. The four content commits have stable patch IDs identical to the originals: `840b7d1`→`2343230`, `9eba120`→`b3efed4`, `951e39c`→`a673bdc`, `ab10fe6`→`b8c293a`. | Structured diff, `git patch-id --stable` |

## 2. Rejected routes

| Route | Reason rejected |
|---|---|
| Change `date` | Forbidden by R-7. |
| Rewrite history | Forbidden. |
| Merge `c2118cc` into the candidate (even with `-s ours`) | It would publish the five unreleased RulesApp commits, including the proposed FALLS closure, into production history. That conflicts with the U-1 safeguards. |
| Push the frozen tag to GitHub | Same exposure, and it is a production-repository change. |
| A local tag alone | Not sufficient, by Founder instruction. |

**Dependency, reported as required:** the `c2118cc` Git object is not available in the release repository. The mechanism therefore carries the minimal objects needed to verify it inside the repository.

## 3. Mechanism (smallest form)

### 3.1 Code-pinned allow-list in `oral_monthly.py`

`REBASED_PROVENANCE` has exactly one entry, keyed by the record path:

```
correction_id      CORR-SAFETY-HPFUEL-PIPE-20261022
origin_commit      c2118cc7a18b37ddef3d852bb0c1f80bb7973c30
origin_record_blob d30bc748af5a7d5d324b299d39c9ad95ee428370
integration_commit 8e7eff905eac95a2e641ef7c2fc8045831bbecca
evidence           tools/oral/provenance/rebased_corr_safety_hpfuel_pipe_20261022.json
evidence_sha256    29d6a4f8ae8a93c2ee978de148328fce115d9000db5db4e7e16d1ffe8cdcbd55
decision_ref       FOUNDER-DECISION-R7-R8-20261113
```

`REBIND_FIELDS = {founder_authorisation, baseline_commit, governing_commits, note}`.

### 3.2 Committed evidence file

The evidence file is `miw-rebased-provenance/1`. It holds the raw Git objects that prove the origin, base64-encoded:
- the `c2118cc` commit object;
- its root tree, `tools` tree and `tools/oral` tree;
- the record blob.

That is 5 objects, about 24 KB. The trees name no file that the candidate does not already contain. The commit's author line already appears throughout the published history.

### 3.3 Verification

The check runs from a fresh clone, using only HEAD's files and history. The record is accepted only if every condition holds.
1. The path and `correction_id` equal the entry.
2. The evidence file's SHA-256 equals `evidence_sha256`.
3. The evidence schema, path, `correction_id` and `origin_commit` equal the entry.
4. Every object's SHA-1, recomputed as `type len\0body`, equals its stated id. The object set is exactly {commit, 3 trees, blob}, with no extras and no duplicates.
5. The commit object's id is `origin_commit`. Its tree chain `tools` → `oral` → `<record filename>` resolves to `origin_record_blob`.
6. **The committer date and the author date of the origin commit both fall in the declared `date`'s month.** For HPFUEL: Oct 2026.
7. The origin blob's JSON has the same key set as the current record and is equal on every key outside `REBIND_FIELDS`. It also has the same `correction_id` and `date`.
8. In HEAD's history, the record's actual first-add commit is `integration_commit`. Its message carries `(cherry picked from commit <origin_commit>)`. The origin committer date precedes the integration committer date.
9. If the `origin_commit` object happens to be in the local object store, its bytes must equal the embedded commit object.

**Result.** The event date is the declared date (October). Its source is `declared+rebased-provenance`. Both dates are kept separately:
- **origin** = `c2118cc`, 2026-10-23;
- **integration** = `8e7eff9`, 2026-11-12.

**Every other record keeps the current rule unchanged.** A month mismatch on any path not on the allow-list still fails.

## 4. Failure conditions (each one is a test)

The check fails closed when any of these occurs:
- missing, unreadable or altered evidence;
- an object whose hash does not verify;
- a forged object, even with a correct hash, because the commit id is not the pinned one;
- an extra or missing object;
- a wrong path or tree chain;
- a different origin blob;
- the origin month differing from the declared month;
- the declared `date` changed;
- any non-rebind field changed, in the current record or in the origin record;
- a different first-add commit;
- a missing `-x` trailer;
- the origin date after the integration date;
- the entry copied onto another path or `correction_id`;
- a second allow-list entry appearing (asserted size = 1);
- any unlisted record with a month mismatch, i.e. a future backdated record.

## 5. Residual limit (disclosed)

Git dates are self-asserted. Nothing inside Git proves wall-clock time, and the existing first-commit rule trusts the same field.

Resistance to fabricated October history comes from three things:
- the exact `c2118cc` id and the evidence SHA-256 are pinned in reviewed code;
- the launcher pins that code's blob in `TRUSTED_BLOBS.txt`;
- independent October corroboration exists outside the repository (§1).

A forged October commit would need a new reviewed code change. This makes the gate no weaker than today, and strictly narrower than a general date bypass.

## 6. Effect on S1

The changed paths are:
- `oral_monthly.py`;
- the evidence file;
- one new test file;
- a gate registration plus the runner's test list;
- this note, kept in the repository under `reports/governance/`.

The S1 exception's `diff_pin` must therefore be regenerated. Its decision reference gains R-7, and the `KNOWN_EXCEPTIONS` pin and `TRUSTED_BLOBS` change with it. **That re-pin is deferred to final-candidate assembly**, because R-8 may change the baseline (see the release-order plan). Until then, landing gate L4 rejecting the candidate is the expected and correct result.
