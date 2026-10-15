# POST31 — LOHAN Source Series Admission (source classification only)

**Date:** 10 October 2026 · **Lane:** POST-PART31 · **Status:** LOCAL CANDIDATE — not pushed, not deployed.
**Authority:** LOHAN post-CA4W requalification accepted; this task authorises **source-series admission / classification only**. It does **not** authorise canonical subject IDs, `MERGE-*`, Uday↔LOHAN concept relationships, BWM/liability canonical integration, D-L4 publication, or any LOHAN push/deploy.

## 1. Base

`git fetch origin` on 10 Oct 2026 gave origin/main `d8b48e8116ba5285969eaa609f91a4aac71cb2f8` (POST31-CA4W), as required. No intervening commits, so no overlap classification was needed. Qualified LOHAN candidate: `43441b7e62cf8e2fdc79e574403fc34ebb38c7ac` (local only, never pushed).

## 2. Architecture decision

Use the existing CA2/CA3 Layer-1 architecture. `source_nodes.csv` already carries a `series` column and the identity rule "exact published `file#anchor`"; admission is therefore **data rows plus a narrowed validator, with no new file, column or schema**.

| Question | Decision | Why |
|---|---|---|
| Where do the 123 nodes live? | Appended to `source_nodes.csv` with `series = LOHAN` | Same identity rule, same columns; Uday rows stay byte-identical |
| Key | Full `meoclass1/oralnotes/lohan-notes-p<N>.html#topic-p<N>-<n>`; `N` in file and anchor must agree | 35 anchor strings collide with Uday, so only the file-qualified key is safe |
| Status value | `SOURCE_COMPLETE_UNPUBLISHED` (Uday stays `PUBLISHED_LIVE`) | Registers the source without claiming publication |
| `anchor_scheme` | `PART_LOCAL` | Matches how LOHAN anchors are generated |
| Inbound classification (request A-1) | No new column. A referrer's series is **derived from its path** (`lohan-notes-p<N>.html` pages, `tools/notes/specs/lohan/p<N>.json` specs); any other LOHAN-looking path fails | Keeps all 478 existing rows unchanged; deterministic; fail-closed |
| Timing (A-2/A-3) | Register now, before the pages exist in the tree | The registry rule is "register at creation"; admitting first means any later regeneration of the baseline no longer hits `LOHAN_ROW` |
| Pages not in the tree | Rows are checked structurally (key, series, part, ordinal-from-anchor, scheme, status, commit); the moment a page is present it is checked node-by-node against the rendered topic-blocks exactly as Uday pages are | Admission must not expose pages. Nothing in the manifest, index or Oral tooling is needed |

## 3. `FORBIDDEN_LOHAN_RE` — narrowed by file scope, not loosened

The regex is unchanged. Before, any data file naming a LOHAN page failed `LOHAN_ROW`. Now only `source_nodes.csv` and `inbound_baseline.csv` may name LOHAN pages, and only as well-formed rows of the admitted set (21 pages / 123 nodes, pinned in the validator, so changing it is a registry decision and not a data refresh). `display_aliases.csv` and `status/*.json` still fail `LOHAN_ROW`.

New and changed validator codes:

| Code | Fires when |
|---|---|
| `LOHAN_PAGE_UNREGISTERED` | a row, a mention in an admitting file, or a page in the tree is outside the admitted pages |
| `LOHAN_ADMISSION_COUNT` | LOHAN rows ≠ 123 or LOHAN pages ≠ the admitted 21 |
| `UNKNOWN_SERIES` / `BAD_SERIES` | series is not `UDAY`/`LOHAN`, or disagrees with the series of the key's file |
| `KEY_MALFORMED` / `KEY_WITHOUT_FILE` | anchor-only keys, or a LOHAN file with an anchor that is not `topic-p<N>-<n>` for the same `N` |
| `DUPLICATE_KEY`, `BAD_PUBLICATION_STATUS`, `PART_MISMATCH`, `ORDINAL_MISMATCH`, `SCHEME_MISMATCH`, `KEY_FIELD_MISMATCH`, `BAD_SOURCE_COMMIT` | existing checks, now series-aware |
| `CROSS_SERIES_REFERENCE` | a LOHAN node is an alias target, an inbound target, a status consumer or a teaching hub |
| `LOHAN_REFERRER_UNREGISTERED` | an inbound referrer (baseline or live) is LOHAN-looking but not an admitted LOHAN page/spec |
| `LOHAN_INBOUND_DRIFT` | when LOHAN referrers exist in the tree, the live LOHAN→Uday references differ from the baseline in either direction |
| `KEY_NOT_RENDERED`, `RENDERED_NOT_REGISTERED`, `TITLE_MISMATCH` | apply to LOHAN pages as soon as they are present |

`validate_status_consumers.py` now builds its node set from `series == UDAY` rows only, so a status core can never bind a LOHAN node.

## 4. Result

| Measure | Value |
|---|---|
| LOHAN source rows | **123** unique, 21 pages, all `LOHAN` / `SOURCE_COMPLETE_UNPUBLISHED` / `PART_LOCAL`, `source_commit` 43441b7 |
| Rows matching the rendered pages (simulated admitted tree) | 123/123 (anchor, title, ordinal, part) |
| Inbound baseline | **4,040 → 4,168** references; 478 → 604 rows |
| New LOHAN→Uday references | **128** in 126 rows (64 from pages, 64 from specs), 40 referrer files |
| Distinct Uday target anchors | **57** |
| Broken | **0** (baseline and live) |
| Uday source rows / aliases / inbound rows / status cores | unchanged (exact byte prefix; aliases and the three status cores byte-identical) |
| Canonical IDs, relationships, aliases for LOHAN | none |

`inbound_baseline.csv` is appended, not re-sorted, so the diff is purely additive; the validator does not require ordering.

## 5. Not done, by design

- No change to `notes_content_index.json`, `oralnotes/index.html`, `notes-master-index.html`, any learner page, or `tools/oral/**`.
- No LOHAN page or spec is added to the tree by this candidate.
- **Landing note for D-L4:** the pages are static files, so landing them on `main` publishes them even without a manifest entry (consistent with the earlier "landing = publication" finding). Admission is deliberately independent of that. When D-L4 is authorised its package must also (a) flip the LOHAN publication status in the validator and data to the published value, and (b) resolve the Oral `every notes page is classified` control, which the pages will trip.

## 6. Validation

`validate_canonical.py`, `test_validate_canonical.py`, `validate_status_consumers.py`, `test_validate_status_consumers.py` all pass in two checkouts: the candidate (LOHAN pages absent) and a scratch simulated admitted tree (main + the 43441b7 pages and specs, never committed). The mutation harness runs LOHAN cases in declared `absent` and `present` modes so each is meaningful in either checkout. One pre-existing case, M11 ("any LOHAN row fails"), asserted the rule being narrowed; it now asserts the new file-scoped rule (a LOHAN page named in the alias table still fails `LOHAN_ROW`), and 33 LOHAN cases cover the cases the task listed.
