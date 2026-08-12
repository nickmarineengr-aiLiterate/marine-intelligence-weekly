# SOLVEDQP DERIVED LAYER — manifest, search, updates, health

**How the Solved QP delivery product is generated, and who owns each part.**
Created 2026-08-12.

One sentence: **the canonical specs are the only content, the manifest is the
only inventory, and everything a candidate sees is generated from those two.**

---

## 1. THE FLOW

```
  meoclass1/pastpapers/specs/*.json          CANONICAL. Authored. The only content.
            |
            |  build_solvedqp_manifest.py
            v
  solvedQP/solvedqp_content_index.json       GENERATED. The only inventory.
            |
            +--> solvedQP/index.html          home: counts, coverage, LATEST UPDATES
            +--> topic search                 in-page, over this file
            +--> solvedqp_health_check.py     daily, against main, emailed
            +--> solvedqp_search_test.py      search behaviour, in CI

  specs ----+--> solvedQP/QP####.html         the papers themselves (build_paper.py)
            +--> solvedQP/questions-YYYY.html year sheets (build_questions_year.py)
```

Nothing in the second column is hand-written. Nothing in the third column keeps
its own list of what exists.

---

## 2. OWNERSHIP — who changes what

| Artefact | Owned by | Changed how |
|---|---|---|
| `specs/<PAPER>.json` | the QP authoring session | authored and verified, one paper at a time |
| `specs/<PAPER>.json` → `changelog[]` | the session that makes a correction | appended, structured; see §5 |
| `solvedqp_content_index.json` | `build_solvedqp_manifest.py` | **never hand-edited** |
| `solvedQP/index.html` | `build_solvedqp_home.py` | **never hand-edited** |
| topic search inventory | the manifest | there is no second index |
| latest-updates strip | the manifest | nobody edits `index.html` when a paper lands |
| daily health report | `solvedqp_health_check.py` | GitHub Actions, daily |

**Nobody hand-maintains a search inventory. Nobody hand-edits the manifest.**
If a count is wrong, the spec is wrong or the generator is wrong; the manifest
is never the place to fix it.

---

## 3. WHY THERE ARE TWO MANIFESTS

They are different surfaces with different readers, and merging them would put
authoring metadata in front of paying candidates.

| | `meoclass1/pastpapers/pastpapers_content_index.json` | `solvedQP/solvedqp_content_index.json` |
|---|---|---|
| Surface | review / authoring (`/meoclass1/pastpapers/`) | delivery (`/solvedQP/`) |
| Reader | the production team | the candidate's browser |
| Carries | `reuse_tier`, `verification_status`, `answer_status`, dedup and red-team paths, **every** paper's questions | question stems, topic labels, sitting metadata — **solved sittings only** |
| Built by | `build_index.py` | `build_solvedqp_manifest.py` |

Both derive from the same specs. Neither is a copy of the other.

---

## 4. THE PAID-TEXT BOUNDARY

The manifest is served to a browser, so its contents are effectively published
to anyone entitled to the product. What may be in it:

**ALLOWED** — printed question stem, short title, topic/subject/intent tags,
search aliases, marks, sitting, recurrence status, anchor href.
These are discovery information; the year sheets already show them.

**NEVER** — `model_answer`, `study_notes`, `quick_revision`, `answer_route`,
`understand_first`, `memory_cue`, `retrieval_cards`, and every authoring field
including `recurrence_class`, `host_recurrence_hint`, `reuse_tier` and
`verification_status`.

This is **enforced, not documented**. `assert_no_paid_text()` fails the build on
(a) any banned key anywhere in the tree, and (b) any 60-character run of any
model answer appearing in the serialised manifest beyond what the published
stems legitimately contain. `--self-test` injects both and proves they fire.

> The subtraction in (b) matters. A model answer routinely opens by restating
> its own printed stem — QP2403-Q4's does, word for word — so a naive scan
> convicts the product of leaking its own question paper. The guard tests for
> answer prose *beyond* the published surface.

### 4.1 The exposure this does NOT fix

The MIW GitHub repository is **public**. `solvedQP/QP2601.html` — 389 KB of
paid worked answers — is readable with no authentication at
`raw.githubusercontent.com`. The Vercel middleware in `api/_lib/routes.js`
gates the *website*; it does not gate the *source*.

The manifest adds no new class of exposure — it contains strictly less than the
pages already committed beside it — but it must not be cited as evidence that
the boundary is sound. **It is not.** That finding is separate, pre-existing and
recorded in `WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`.

---

## 5. RECENTLY UPDATED — where change history comes from

Two sources, in precedence order:

1. **`changelog[]` on the paper's own spec.** The only place a correction is
   recorded. Structured, owned by the paper it describes, reviewed with it:

   ```json
   "changelog": [
     {"date": "2026-08-20", "kind": "correction",
      "questions": ["QP2508-Q5"],
      "summary": "Regulatory citation corrected and the Study Guide updated."}
   ]
   ```

2. **A synthesised `added` record** from the spec's `updated` date, for any
   AVAILABLE paper with no explicit `added` entry. Every solved paper therefore
   appears once without anyone remembering to write the ordinary case down.

`SESSION_HISTORY.md` is **not** scraped. It is free-form narrative written for
engineers, and building a customer-facing surface out of it would couple the
product to prose nobody edits with a customer in mind.

Records are candidate-facing: no branch, no commit, no build state. The health
check warns if a summary uses internal process language.

---

## 6. THE HEALTH CHECK, AND THE ONE RULE THAT MAKES IT DIFFERENT

`tools/pastpapers/solvedqp_health_check.py` runs daily from
`.github/workflows/solvedqp-health-check.yml` (03:30 UTC / 09:00 IST), fetches
`main` as a tarball, checks what is actually published, and emails through
Brevo. `workflow_dispatch` allows a manual run.

Coverage: inventory consistency · status/file agreement · paper structure and
anchors · every link and every search target · search integrity · the paid-text
boundary · product leakage · written known traps · **temporal contamination** ·
update-record honesty · manifest freshness.

### 6.1 Current law is not the law of the paper

> `A.1185(33)` is **wrong** as current 2026 law and **right** for QP2512, sat in
> December 2025.
> `Merchant Shipping Act, 1958` is **wrong** as current law and **right** for
> all twenty-two 2024 and 2025 sittings.

`meoclass1/known_traps.md` — the **Oral** ledger — greps for both. Pointing this
checker at it would produce roughly a hundred findings on correct content every
morning, and a report that is wrong every day is a report nobody opens.

So the Oral ledger is **not used here**, and the exemption is written into the
checker as a named constant rather than left as an omission. The **Written**
ledger at `meoclass1/pastpapers/known_traps.md` is used, and it already handles
time-sensitivity properly by marking such entries `GREP: SKIP`.

### 6.2 What IS checked, deterministically

Forward contamination only, in one direction: **an instrument may not be
asserted as operative in a paper sat before that instrument existed.** That needs
no judgement — only the sitting date and the instrument's own date.

Three refinements, each of which came from a false positive on the first run:

- **Answer panes only.** The Study Guide is *required* to tell the candidate the
  law has since changed. Scanning the whole page raised seven errors on correct
  content.
- **Negation-aware.** "the 2025 Act had assent but had **not commenced** at this
  sitting" is the model sentence, not a defect.
- **Same month is REVIEW, never ERROR.** A December 2025 sitting and a
  3 December 2025 adoption cannot be ordered from a month. A checker that
  guesses is manufacturing a verdict.

No AI judgement runs in CI. Every check is deterministic.

---

## 7. RUNNING IT

```bash
python tools/pastpapers/run_toolchain.py              # builds and checks everything
python tools/pastpapers/run_toolchain.py --self-test  # + every injected-defect suite
```

Individually:

```bash
python tools/pastpapers/build_solvedqp_manifest.py            # regenerate
python tools/pastpapers/build_solvedqp_manifest.py --check    # fail if stale
python tools/pastpapers/build_solvedqp_manifest.py --self-test
python tools/pastpapers/solvedqp_search_test.py
python tools/pastpapers/solvedqp_health_check.py --local --no-email
python tools/pastpapers/solvedqp_health_check.py --self-test
```

The toolchain builds the manifest **before** the home page and runs the search
and health checks **after** it. That ordering is what makes the manifest
authoritative rather than merely present.
