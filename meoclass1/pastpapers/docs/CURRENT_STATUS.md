# CURRENT STATUS — MEO Class I Written Questions / EM2607

**Canonical restart document for the Past Written Papers product.**
Last updated: 2026-08-08. Written at session closeout; read this first.

> Scope note: `AI_SESSION_HANDOVER.md` at the repository root is a *repository bootstrap*
> handover dated 2026-07-30 and is now stale (it describes a repo with no `tools/`
> directory). It was deliberately **not** edited. This file is the product-scoped status
> for Past Papers and is the one to trust for this work.

---

## 1. Repository

| | |
|---|---|
| Path | `F:\Marine-Intelligence-Weekly` |
| Remote | `https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git` |
| Branch at closeout | `pastpapers/em2607-founder-review` |
| Branched from | `main` @ `2bf6e49` (unchanged; nothing merged to main) |
| Checkpoint commit | `f8b39de` — *local only, NOT pushed* |
| Push status | **BLOCKED** — the sandbox permission classifier denied `git push`. Not a credential or network failure. See §17. |

All git commands in this repo should be run with `-c safe.directory=*`.

---

## 2. Product state

**EM2607 (July 2026, Engineering Management, MEO Class I) — all 9 questions built.**

Each question carries a Model Written Answer, a Study Guide and a Quick Revision block.
The paper page is interactive: live search, sticky side index, collapsible cards,
bookmarks, studied state, deep links, and a paper-level Rapid Revision table.

**Everything below is FOUNDER REVIEW state.** Not published, not gated, not indexable.

| Output | Path | Nature |
|---|---|---|
| Paper | `meoclass1/pastpapers/EM2607.html` | **generated** — never hand-edit |
| Written Questions index | `meoclass1/pastpapers/index.html` | **generated** |
| 2026 topic coverage | `meoclass1/pastpapers/topics-2026.html` | **generated** |
| Retrieval manifest | `meoclass1/pastpapers/pastpapers_content_index.json` | **generated** (manifest v2.0) |
| Canonical content | `meoclass1/pastpapers/specs/EM2607.json` | **SOURCE OF TRUTH** (schema 1.2, v0.3) |
| Known traps | `meoclass1/pastpapers/known_traps.md` | hand-maintained |
| Verification records | `meoclass1/pastpapers/verification/EM2607/*.md` | hand-maintained evidence |

Generated HTML **is** committed — that matches established MIW practice (QB and notes
pages are committed generated artifacts).

---

## 3. Architecture — settled, do not redesign

```
specs/EM2607.json          <-- ONE canonical question object per question
      |
      +-- build_paper.py   --> EM2607.html   (answer + study guide + quick revision + cheat sheet)
      |
      +-- build_index.py   --> pastpapers_content_index.json
                           --> index.html
                           --> topics-2026.html
```

**One question object → six outputs. No answer text exists twice anywhere.**

- **Tools stay at `tools/pastpapers/`.** Do **not** move them under
  `meoclass1/pastpapers/tools/`. Reason: this follows the `tools/notes/` generator-toolchain
  precedent and preserves the `miw_paths` import relationship. (`meoclass1/qb_health_check.py`
  is product-local, but it is a remote scanner + emailer — a different kind of thing.)
- **Known traps use `known_traps.md` with `GREP:` / `GREP: SKIP`**, matching
  `meoclass1/known_traps.md`. Not JSON. A `SCOPE: html` line limits a trap to generated
  pages, because specs and the manifest must record aggregator provenance verbatim.
- **No separate Study Guide HTML file.** Study Guide and Quick Revision live inside the
  same canonical question object and render into the card. A separate page would duplicate
  render logic for no user gain.
- **Search is driven by generated `data-search` attributes**, which is also the existing
  MIW pattern (`meoclass1/index.html:370`). Do **not** revert to QB10_A's `innerText`
  approach — see §4.
- **Bookmarks/progress**: `localStorage`, keys `miw:pastpapers:v1:bookmarks` and
  `miw:pastpapers:v1:progress`, keyed by stable `question_id` (`EM2607-Q5`), never by DOM
  order. No account system, no database, no framework.
- **Publication mode exists**: `--publish` switches noindex→index, adds canonical/OG/JSON-LD
  and *removes* the per-question production metadata block. Review mode is the default.

---

## 4. Proven improvements over QB10_A — do not reopen

`meoclass1/QB10_A.html` was the **UX reference, not code to copy**. It has a real defect:
its `applyFilters()` reads `card.innerText`, which excludes `display:none` subtrees — so
**searching QB10_A never matches answer content while a card is collapsed.** Its cards are
also `onclick` divs with no keyboard path and no ARIA.

The Written Questions implementation deliberately differs:

- real `<button>` toggles with `aria-expanded`, keyboard operable;
- bookmark and studied controls sit **outside** the toggle so they cannot open the card;
- generated `data-search` metadata, so search works on collapsed cards and matches
  aliases that are never displayed;
- `localStorage` persistence keyed by stable question id;
- deep links (`EM2607.html#q5` opens Q5 expanded);
- generated indexes rather than hand-maintained ones;
- skip link, `aria-live` result count, focus-visible styling, reduced-motion and print rules.

Do not undo any of these unless testing proves a defect.

---

## 5. Retrieval architecture

Every question is retrievable by any combination of: paper id, question id, year, month,
question number, exact wording, short title, subject tags, topic tags, intent tags,
search aliases (~22 per question), regulations/codes, recurrence, direct URL/anchor,
study-guide availability, verification state, and browser-level bookmark/study state.

`pastpapers_content_index.json` holds one record per paper **and one per question**, each
with a pre-built `search_blob`. That is what makes "search every question without knowing
which paper it is in" work, and it is what a future production agent will consume.

**Recurrence is classed honestly:** `new` / `topic_recurrence` / `near_recurrence` /
`exact_recurrence`. All three EM2607 repeats are `topic_recurrence` — a third-party
recurrence table alone can never support `near` or `exact`; that needs the prior paper's
wording actually compared. The rule is encoded in the manifest.

---

## 6. QA state at closeout

```
python tools/pastpapers/run_toolchain.py --self-test
```

```
SPEC          PASS  (4 warning(s))
PAPER BUILD   PASS
INDEX BUILD   PASS
UI BEHAVIOUR  PASS      34/34
KNOWN TRAPS   PASS      15 traps: 8 auto-scanned, 7 manual; all injected traps fire
HEALTH        PASS      all injected faults detected
AUDIT         PASS      13 checks
ALL STAGES PASS   4 warning(s)      exit 0
```

The health and trap checks are **positive-controlled** — `--self-test` injects real faults
and asserts they are caught. Keep it that way; a check that never fires is worse than none.

### The 4 warnings are accepted, not defects

| Warning | Decision |
|---|---|
| Q2 model answer ≈ **709** words (band 450–650) | **Accepted.** The excess is the corrected Bunkers Convention / CLC legal wording. Do not shorten. |
| Q6 model answer ≈ **695** words | **Accepted.** The excess is the "zero-carbon" qualification and the ICE-vs-fuel-cell contrast. Do not shorten. |
| 2 × re-verify notices | Informational — see §7. |

650 is guidance, not a gate. **Do not spend the next session trimming these.**

---

## 7. PUBLICATION STATUS: BLOCKED ON Q7 PRIMARY-SOURCE VERIFICATION

**Q7 — Merchant Shipping Act, 2025.** Two blockers, both real, neither disguised:

1. **Commencement scope not established.** `S.O. 1244(E)` dated 10 March 2026 brought the
   Act into force with effect from **15 March 2026**. Whether that notification commenced
   **every** provision or only some is **not confirmed** — the Act permits different dates
   for different provisions. The answer is worded to assert only what is evidenced.
2. **No section-level citations.** The full statutory text could not be retrieved
   (India Code PDF returned **HTTP 403**). **No section number of the 2025 Act is cited
   anywhere in the answer**, deliberately. Provision-level citations must be added only
   from the Gazette text.

The next session must re-ground Q7 from current primary Government of India / DG Shipping /
Gazette sources before any public release. Verified and safe to keep: Act No. 24 of 2025,
assent 18 August 2025, in force 15 March 2026 by S.O. 1244(E), repeals the MS Act 1958
(saving Part XIV, not s.411A) and the Coasting Vessels Act 1838.

**Seven claims across the paper carry `reverify_before_publication` flags** (Q1 ×2, Q4 ×1,
Q6 ×2, Q7 ×2). `validate_spec.py` prints them on every run.

---

## 8. Q9 / QB9_C — known cross-link issue, repair deliberately deferred

EM2607 Q9 correctly treats the **Indian Marine Insurance Act, 1963** as the operative
statute (s.19 utmost good faith, s.20 disclosure incl. the four s.20(3) exceptions).

`meoclass1/QB9_C.html` attributes the principles of marine insurance to the **UK Marine
Insurance Act 1906**, which is the wrong statute for an Indian examination. EM2607 Q9
currently carries an **explicit caution** on that cross-link rather than silently inheriting
it. `meoclass1/QB9_E.html` handles it correctly (names both Acts).

A broad Question Bank repair was **deliberately deferred** and spawned as a separate task.
Do not undertake it inside the Past Papers work. Once QB9_C is fixed, soften the caution in
`specs/EM2607.json` (Q9 `cross_links`) and regenerate. Recorded as trap 8 in
`known_traps.md`.

---

## 9. Review / publication state — do not change without Founder approval

- EM2607, the Written Questions index and the 2026 Topics index are **all `noindex`**.
- **No production gate** is enabled (`miw_auth` count is 0 on all three pages).
- **Nothing deployed. Nothing published. No publication approval given.**
- `meoclass1/index.html` has one added nav link to `/meoclass1/pastpapers/`. This is a
  local link to an unpublished section — harmless until deployment, but it is the one
  thing that becomes visible if the site is deployed as-is.

---

## 10. Important files

**Read these to restart:**

| File | Why |
|---|---|
| `meoclass1/pastpapers/docs/CURRENT_STATUS.md` | this file |
| `meoclass1/pastpapers/specs/EM2607.json` | canonical content; everything else is generated from it |
| `meoclass1/pastpapers/verification/EM2607/PILOT_RED_TEAM_REVIEW.md` | 15 findings, 2 Critical — why the answers read as they do |
| `meoclass1/pastpapers/verification/EM2607/DEDUP_AND_SOURCE_PLAN.md` | reuse tiers, production order, corpus findings |
| `meoclass1/pastpapers/verification/EM2607/Q7.md` | the publication blocker in detail |
| `meoclass1/pastpapers/known_traps.md` | 15 traps already paid for |
| `meoclass1/pastpapers/docs/miw-pastpapers-production_SKILL_DRAFT.md` | §A–G annotations incl. 18 AGENT_LESSONS |
| `tools/pastpapers/run_toolchain.py` | the one command |

**Not in the checkpoint, still on disk:** `meoclass1/pastpapers/docs/*.pdf` — six
aggregator-hosted (Dieselship-branded) source papers. See §13.

---

## 11. Standing content rules

- **`Notes-for-written-answers/` is never a verification source.** 45 HATC coaching PDFs;
  all 325 machine-readable pages carry the publisher's own line that *"certain
  statements/figures have been intentionally made wrong"*. Discovery and question-scope
  evidence only. Never authority, never reproduced. (One exception in that folder:
  `DOC-20251125-WA0009.pdf` is genuinely IRS Guidelines on Ballast Water Management 2018.)
- **MIW holds no licensed IMSBC Code.** Q1's Group C classification is recorded at
  `P2_AUTHORITATIVE_SECONDARY`, not P1. Acquiring the 2023 (07-23) and 2025 (08-25)
  editions is the highest-value unblock for every future cargo question.
- **The source papers are aggregator copies, not official.** `official_source_verified` is
  `false` by design and is stated on the page. Do not upgrade that claim without actually
  comparing an authoritative DG Shipping / MMD copy.
- **Three-layer answer test:** model answer = what scores + only the reasoning needed to
  make it correct; study guide = the rest. Research depth that does not earn marks belongs
  in the study guide.

---

## 12. Outstanding work — priority order

1. **Fresh-session re-grounding.** Run the restart commands in §14; confirm the toolchain
   still passes before touching anything.
2. **Founder visual review** of the three product pages. *(Not yet done — see §15.)*
3. **Q7 primary-source resolution** (§7). This is the publication blocker.
4. **Correct any defects found during Founder review.** Edit the **spec**, never the HTML.
5. **Re-run the full toolchain** and confirm deterministic rebuild.
6. **Founder approval.**
7. **Only then** decide gating / publication / indexability (`--publish`, `--gated`).
8. **Only after EM2607 is stable**, decide whether to build a second paper to test whether
   the workflow generalises.
9. **Only after that additional proof**, mature `miw-pastpapers-production_SKILL_DRAFT.md`
   into a final skill and consider the Claude production agent. **Do not build the agent
   yet.**

---

## 13. Deliberate exclusions from the checkpoint

**Six source PDFs under `meoclass1/pastpapers/docs/` were NOT committed** (~1.4 MB,
Dieselship-branded, watermarked third-party material). They remain on disk and nothing was
deleted. Reasons: pushing them to a remote is redistribution of third-party copyrighted
material and is hard to reverse; repository visibility could not be confirmed in-session
(`gh` unavailable); and the toolchain has **no runtime dependency** on them, so excluding
them breaks nothing.

**`FOUNDER DECISION REQUIRED`** — whether the source PDFs should be committed as provenance.
If yes, the next session can add `meoclass1/pastpapers/docs/*.pdf` in a separate commit.

Also untracked and deliberately left alone (pre-existing, unrelated to this work):
`Claude skill/`, `ENGINEERING_PRINCIPLES_*.md`, `REPOSITORY_STATUS.md`,
`Notes-for-written-answers/` (268 MB of third-party HATC material — must never be
committed), `docs/MIW-master-Question-bank/`, `docs/agent-build/`, `docs/miw-notes-mgmt*`,
and `tools/notes/_*.txt` scratch files.

---

## 14. Exact restart commands

```bash
cd /d F:\Marine-Intelligence-Weekly
git -c safe.directory=* status --short --branch
git -c safe.directory=* log -3 --oneline --decorate
python tools/pastpapers/run_toolchain.py --self-test
```

Then open the three pages for review:

```bash
start meoclass1\pastpapers\index.html
start meoclass1\pastpapers\EM2607.html
start meoclass1\pastpapers\topics-2026.html
```

Deep-link check: `EM2607.html#q5` must open Q5 already expanded.

To rebuild after a spec edit (never edit the HTML):

```bash
python tools/pastpapers/run_toolchain.py --self-test
```

---

## 15. Stop conditions — require Founder decision

- **Publication, gating or removing `noindex`.** Blocked on Q7 (§7) regardless.
- **Committing the source PDFs** (§13).
- **Merging this branch into `main`.** The checkpoint branch is deliberately not merged.
- **Starting a second paper.** Not until EM2607 is approved.
- **Building the autonomous production agent.** Not until the workflow is proven on more
  than one paper.
- **Any change to the settled architecture in §3–§4** without test evidence of a defect.

---

## 17. Push status — checkpoint is LOCAL ONLY

The checkpoint commit `f8b39de` exists **only on this machine**, on branch
`pastpapers/em2607-founder-review`. The `git push -u origin
pastpapers/em2607-founder-review` was **denied by the session's permission classifier**,
not by git, GitHub, credentials or the network. No authentication configuration was
changed, and no retry or workaround was attempted.

**There is currently no off-machine backup of this work.** The first thing the next
session should do, once it has permission to push, is:

```bash
cd /d F:\Marine-Intelligence-Weekly
git -c safe.directory=* push -u origin pastpapers/em2607-founder-review
```

Do **not** force push. Do **not** merge into `main`. Do **not** open a pull request unless
the Founder asks.

---

## 16. Known environment quirk

A repo hook, `validate_antipatterns.py`, is misconfigured — its plugin path does not exist
on disk, so it errors on every file write. It blocks nothing, but it is currently a no-op
safety net and every Write/Edit reports a hook failure. Not caused by this work; worth
fixing or removing.

`package.json` sets `"type": "module"`, so any Node test file must use the `.cjs`
extension — hence `tools/pastpapers/ui_behaviour_test.cjs`.
