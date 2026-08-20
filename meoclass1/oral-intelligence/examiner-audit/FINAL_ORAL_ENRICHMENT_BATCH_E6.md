# Final Oral Enrichment — Batch E6 (IMO instruments, maritime law and pollution response)

Six authorised existing-answer enrichment edits landing on **six** cards across **six**
pages. **No canonical card was created, removed, re-anchored or re-homed.** Corpus stays
at **721** questions / 86 question-bearing files.

Baseline commit `1b6c6c0`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

**This is the last enrichment batch. Enrichment workload 6 → 0.**

---

## 1. Repo truth

Working tree clean at session start. `origin/main` = `1b6c6c04c86e1883d3688dd1137aafec792205fb`,
matching the brief exactly, so no intervening commits needed inspection. Consolidation tip
`eb586ed`, matching. Branch cut: `prod/oral-enrichment-e6-final` from `origin/main`.

`prod/oral-enrichment-e5-stcw-mlc` sits *on* `1b6c6c0` — E5 was fast-forwarded, not merged.
E6 follows the same integration shape.

## 2. The action set — both representations agree

The brief named E6 as `ENRICH-A045`–`A050`. Verified, not assumed, on both independent
representations: the `batches[]` entry for E6 lists exactly those six ids, and the `batch`
field on each production action assigns exactly those six to E6. The two lists are equal
**in order**, the declared `action_count` is 6, and the batch's `source_family_ids` equal
the union of the per-action `family_ids`. No reconciliation needed.

## 3. Action matrix

| Action | Band | Verify class | Target | Family | Retargeted | Status |
|---|---|---|---|---|---|---|
| ENRICH-A045 | E-P2 | **CURRENT_REG** | `QB4_I.html#q4` | GAP-0144 | no | IMPLEMENTED |
| ENRICH-A046 | E-P2 | TECHNICAL_REASONING | `QB9_G.html#q3` | GAP-0165 | no | IMPLEMENTED |
| ENRICH-A047 | **E-P1** | **CURRENT_REG** | `QB1_A.html#q18` | GAP-0480 | no | IMPLEMENTED |
| ENRICH-A048 | E-P2 | **CURRENT_REG** | `QB3_J.html#q5` | GAP-0521 | no | **REDUCED SCOPE** |
| ENRICH-A049 | E-P3 | TECHNICAL_REASONING | `QB9_B.html#q2` | GAP-0382 | no | IMPLEMENTED |
| ENRICH-A050 | E-P3 | PRIMARY_AUTHORITY | `QB6_F.html#q4` | GAP-0553 | **YES** ← `QB2_A#q5` | IMPLEMENTED |

Priority mix **1 × E-P1, 3 × E-P2, 2 × E-P3** — the E-P1 is the last in the programme.
Verification mix **3 currentness, 2 reasoning-only, 1 primary** — **50% currentness
exposure**, twice E5's rate, exactly as E5's handoff projected.

**No shared target.** Six actions, six cards, six files, so actions == distinct cards ==
changed cards == 6 exactly. The validator asserts that absence rather than leaving it
implied.

**One retarget.** A050 was moved by the consolidation from `QB2_A#q5` to `QB6_F#q4`. The
brief did not mention it; it was derived from the consolidation. The retarget is sound and
consequential — see §5.

## 4. Current-live recheck

All six target cards were opened in full against the live 721-question corpus before any
edit — q-text, timed blocks, full answer body, CE relevance, examiner chain, traps,
reg-box and deep dives. Every candidate limb token was then checked **against the baseline
card**, because a token the baseline already carried would make the guard pass without the
limb being there at all.

That sweep rejected two tokens: **`protocol` and `by reference` for A046**, both already
present in that card's deep-dive. It is a real finding, not a formality — A046's limb was
**partly pre-covered**, and guarding on either token would have certified nothing.

**Zero actions were held. Zero were downgraded to already-covered. One was reduced in
scope** (A048), which is a different thing and is recorded as such.

## 5. A050's retarget, and the card it was moved away from

`QB2_A#q5` — A050's *original* target — is the corpus's dedicated **"Container lost at sea"**
card. That matters because **A047's limb is the container-loss reporting route**. The two
actions therefore touch the same subject from opposite ends, and the consolidation moved
A050 off that card.

Reading `QB2_A#q5` was not optional housekeeping: its reg-box cites *"Resolution
MSC.460(101) / Resolution MSC.517(105) regarding mandatory reporting systems for lost
containers."* Neither is the instrument that created the requirement. The mandatory regime
comes from **resolution MSC.550(108)**, adopted 23 May 2024, amending SOLAS regulations
V/31 and V/32, in force 1 January 2026. That is live cross-product inconsistency on a card
E6 is not authorised to edit — recorded as debt (§14, item 2), not repaired.

## 6. A047 — the E-P1, reviewed to the highest standard

Target and band both independently confirmed against the consolidation: `QB1_A#q18`,
E-P1, CURRENT_REG_VERIFY_REQUIRED. The limb has two parts and both survived.

**Part one was verifiable from the card alone.** The heading reads **"FAL Standardised
Forms (9 Forms)"** and the list beneath it contains **seven**. A live internal
contradiction, so the limb is genuinely missing rather than already covered.

**But the promised nine is itself superseded.** Under **FAL Standard 2.1 as amended by
resolution FAL.14(46)** (adopted 13 May 2022, in force **1 January 2024**), the declarations
public authorities may require run to **thirteen, (a) to (m)**: the seven FAL forms, postal
items under the Universal Postal Union, the Maritime Declaration of Health, the Ship
Sanitation Control Exemption/Control Certificate, security-related information under
**SOLAS XI-2/9.2.2**, advance electronic cargo information under the WCO SAFE Framework,
and the Advance Notification Form for Waste Delivery to Port Reception Facilities. Standard
2.1bis caps only items (a) to (g) at the Convention's appendix 1. The card now says so.

**Part two runs the currentness trap backwards.** The consolidation asked "which
declaration/form carries" a container-loss report. Checked against the amended Standard
2.1, **none of (a) to (m) does**. The report is a **danger message under SOLAS chapter V**:

* **V/31.2.1** — the master of a ship *involved in the loss* reports without delay to
  **ships in the vicinity, the nearest coastal State and the flag State**.
* **V/31.2.2** — if the ship is abandoned, or the report is incomplete or unobtainable,
  **the Company as defined in regulation IX/1.2** assumes the master's obligations.
* **V/31.2.3** — the **flag State** reports the loss to the Organization.
* **V/31.2.4** — a ship that merely *observes* containers drifting reports to ships in the
  vicinity and the nearest coastal State — **not** the flag State.
* **V/32.3** — the contents, including ship identity (IMO number, name, call sign, MMSI),
  position, number lost, dangerous goods yes/no with UN number, container description, and
  a later verified count marked **"final"**.
* **MARPOL Protocol I, Article V**, as amended by **MEPC.384(81)**, routes the
  harmful-substances report through those same SOLAS regulations.

Adopted 23 May 2024, deemed accepted 1 July 2025, **in force 1 January 2026** — so as at
this batch it **already binds**. The danger on this action is therefore the reverse of the
usual one: writing a rule that is in force as though it were still pending. Both directions
are guarded.

**A recall that was wrong, and why it matters.** Working from memory this would have been
written as a new *regulation V/31-1*. There is no such regulation. The IMO's own briefing
settles it: MSC.550(108) inserts new paragraphs into the existing regulations 31 and 32.
The correction came from primary text, not from a secondary summary.

## 7. A048 — reduced scope, honestly

| | |
|---|---|
| **Original limb** | The MS Act 2025 provision under which oil pollution prevention and spill reporting bite, **cited by section**, and the national reporting centre a ship actually calls on discovering a spill in Indian waters |
| **Implemented** | **Part VII of the Merchant Shipping Act, 2025 (Act 24 of 2025)** and the enabling block **sections 133 to 143**; and the reporting route — **nearest Indian Coast Guard MRCC**, without delay, on the Coast Guard's **Spill Notification Pro forma for Oil and HNS**, for a discharge **of any quantity** |
| **Omitted** | A single section number for the spill-reporting duty |
| **Reason** | **Could not be verified.** `indiacode.nic.in` is edge-blocked from this environment on both the PDF and the handle page, and the browser pane returned an Akamai error. Rather than guess, the Part and the enabling section block were established from the **Government of India's own 2026 draft rules**, three of which each recite "in exercise of the powers conferred by sections 133(2), 133(4), 133(5), 134(1), 134(2), 135(2), 136, [140,] 142(1), 143(1) and 143(2)(n) under Part VII of the Merchant Shipping Act, 2025 (24 of 2025)" |

**A wrong number that was nearly published.** A search result placed the pollution
provisions at *"Part XIA, sections 356A–356O"*. That is the **Merchant Shipping Act, 1958**
as amended. The 2025 Act is a consolidating statute of **sixteen Parts and 325 sections**,
so a section 356A cannot exist in it. The letter-suffixed 300s numbering is now a
**forbidden claim** in the validator, because it is the specific wrong answer the available
secondary sources will hand the next editor.

The card says plainly that there is no single "spill reporting" section to quote. That
sentence is a `REQUIRED_QUALIFIER`: a later tidy-up that deletes it invites exactly the
invention it exists to prevent.

## 8. A045 — a limb that had to clarify without contradicting

`QB4_I#q4`'s deep-dive already answers "who audits the Indian administration?" with *"The
IMO itself conducts these audits using an independent team of international maritime
auditors."* The authorised limb is **who actually performs an IMSAS audit** — and the
accurate answer is that the auditors are **nominated by Member States**, not IMO staff,
with the **IMO Secretariat** coordinating.

Written flatly, the limb would contradict its own card. It is therefore phrased as a
refinement — *"The scheme is run by IMO, but the auditors are not IMO staff"* — which
sharpens the existing sentence instead of denying it. This is the A043 lesson from E5:
an authorised limb written without regard to the card it lands on degrades the answer.

Current position, all verified: III Code (**A.1070(28)**) is the audit standard; mandatory
since **2016**; **seven-year** cycle; **India completed its audit on 4 March 2024** as flag,
port and coastal State; the **first mandatory cycle closed in 2026** with **168 Member
States** audited (~94% of the membership); the **second cycle begins July 2027** under the
revised Framework and Procedures adopted as **resolution A.1211(34)**.

**Adopted ≠ operating.** A.1211(34) is adopted; its risk-based continuous monitoring does
**not** begin until the second cycle opens. The card says so, that sentence is a required
qualifier, and asserting the second cycle is already under way is a forbidden claim.

## 9. A046 and A049 — reasoning-only, and what that does not excuse

**A046** supplies the instrument-type ladder the card's own question promises but never
defines — the word *protocol* appears in the q-text and nowhere in the answer. The rungs
are given with their binding force: conventions bind on consent; protocols must be
consented to in their own right; **MARPOL Annexes I and II are compulsory while III to VI
are optional**; regulations are the operative requirement; **codes have no binding force of
their own** and become mandatory only by reference from a convention chapter; guidelines
and circulars are recommendatory. No regulation number is asserted below chapter level.

**A049** places the drill on the strategic/tactical axis: the SOPEP and company response
policy are the strategic layer whose job is to be *correct and current*; the drill is the
tactical layer whose job is to be *honest*. The formulation the candidate can carry into
the room — *the plan proves the response is authorised and resourced; the drill proves it
is executable* — is the whole limb.

## 10. Notes

**None.** No action in this batch drew on the `oralnotes/` product. Every authority is
primary text, an official Administration instrument, or explicitly declared reasoning.

## 11. Additivity

**6 insert opcodes. 0 delete. 0 replace.** Proven twice and independently:

1. **Exact reconstruction** — for each file, deleting the single contiguous inserted region
   recovers the `origin/main` blob byte for byte.
2. **Character-level opcodes** per card, LF-normalised: `ins=1 del=0 rep=0` on all six.

| File | Card | Opcodes | Chars added |
|---|---|---|---|
| QB4_I.html | q4 | ins=1 del=0 rep=0 | +1788 |
| QB9_G.html | q3 | ins=1 del=0 rep=0 | +2182 |
| QB1_A.html | q18 | ins=1 del=0 rep=0 | +3369 |
| QB3_J.html | q5 | ins=1 del=0 rep=0 | +1508 |
| QB9_B.html | q2 | ins=1 del=0 rep=0 | +1478 |
| QB6_F.html | q4 | ins=1 del=0 rep=0 | +1837 |

### The mixed-line-ending trap — new in E6

E6 is the **first enrichment batch with a mixed destination set**. `QB4_I.html` and
`QB9_G.html` are **100% CRLF**; the other four are **100% LF**. E5's nine files were
uniformly LF, and E5 recorded that a shell probe wrongly reported them all as CRLF. Here
the difference is real, so a single batch-wide convention would have left either two files
or four with mixed endings.

State was measured on **untranslated bytes**, the applier derives the convention **per
file**, and every digest in this batch is LF-normalised so it is independent of the on-disk
convention. `line_endings_homogeneous_per_file` now guards it.

**A refinement the commit itself supplied.** `.gitattributes` pins `*.html` to `eol=lf`,
so committing the two CRLF files produced a normalisation warning and stored **LF blobs** -
and the baseline blobs were LF too. The mixed state is therefore **working-copy-only**: the
object store is uniformly LF, and the CRLF exists solely on disk. Two consequences worth
carrying forward. First, the line-level diff is **52 insertions, 0 deletions** with no
re-normalisation churn, corroborating the character-level proof. Second, LF-normalised
digests were not merely convenient but **necessary**: had the manifest hashed raw bytes,
its recorded digests would have been correct on this machine and wrong for anyone who
checked the repo out fresh. E5's manifest note that 'disk and object store agree' is true
of E5's files and **not** of E6's - so the guard must keep measuring disk rather than
assuming the two match.

### Card-scoped insertion, again load-bearing

Insertion markers are not unique at file scope — `<div class="reg-box">` occurs 6, 7 and 9
times in the three files that use it, and 30 times in `QB1_A.html` for A047's marker. A
file-global replace would have landed three of six limbs on the wrong card while still
changing digests, so a naive "did it change?" check would have passed. Every insertion is
therefore card-scoped: the card is extracted by anchor, the marker is required to occur
**exactly once inside that card**, and the rewritten card must occur exactly once in the
file.

## 12. Timed-block delta — zero

All six cards: 15-second and 60-second blocks **byte-identical** to baseline. No timed block
was touched, so no word-count rebalancing was needed. `timed_blocks_unchanged` guards it in
both directions — the manifest may not even *claim* a timed change.

## 13. Follow-up overlap — one of six, not consumed

Re-derived from the current consolidation, not carried from the brief. E6 has exactly one
colocation, and it is the one the brief named — though the brief attributed it to A046
correctly while the action itself is not the one the brief's "A046 ↔ GAP-0481" shorthand
might suggest is at risk.

| Action | Target | Follow-up | Follow-up ask | Distinct? |
|---|---|---|---|---|
| A046 | `QB9_G#q3` | GAP-0481 | "FAL- Maritime single window in detail... came into force, Sagar Sethu" | **Yes** |

* **A046 enrichment limb** = the IMO instrument-type ladder (convention, protocol, annex,
  regulation, code, guideline/circular), which of them bind, and how a code becomes
  mandatory by reference.
* **GAP-0481 follow-up limb** = the FAL Maritime Single Window in detail, its entry into
  force, and Sagar Setu.

**DISTINCT.** An instrument-hierarchy taxonomy does not answer a Single Window
implementation question. **GAP-0481 is NOT consumed. Follow-up workload remains 35 groups.**
The manifest records the distinctness reason, and a mutation proves the guard fires if the
manifest ever claims consumption.

## 13a. E6 validator

`tools/oral/validate_batch_e6.py` — **31 checks, 0 FAIL.**

Beyond the properties inherited from E1 and E5, four are new:

* `no_shared_target` — asserts the *absence* of a shared target, so the arithmetic
  actions == distinct cards == changed cards == 6 is exact. E1 and E5 both needed extra
  guards to stop a shared pair collapsing; E6 asserts it never had one.
* `line_endings_homogeneous_per_file` — measures untranslated bytes and requires each
  destination to be wholly one convention **and** to match the manifest. New because E6 is
  the first batch whose destinations are not uniform.
* `examiner_index_expectation_stable` — the inline `examiner-tag` count proves *delta*
  only; the absolute 960/7 lives in the generated `EXAMINER_INDEX_SNAPSHOT.json`, so the
  manifest's declared expectations are checked against that artefact rather than against a
  number typed into the validator.
* `authorisation_batch_key_matches_batch_id` — added *after* the first mutation run; see
  §13c.

**The validator caught a real defect during development, in itself rather than the card.**
`unsubstantiated_claims_absent` failed A048 for the phrase "reportable threshold" — which
the card uses to *deny* a threshold ("assuming a reportable threshold is the single most
common error"). The card was right and the guard was wrong. The pattern is now anchored on
an actual quantity (`reportable (threshold|quantity)[^.]{0,25}\d`), and it was unit-tested
to reject the card's correct denial while still catching four assertive forms. This is the
same shape as E5, where a guard written against "Rule 37" failed a card that correctly said
"Rules 35 to 37".

## 13b. Validator performance — a fix that was not cosmetic

The first working validator took **91 seconds** per run because it called `git show` once
per file, 172 times. The mutation harness runs the validator 35 times, so that was a
50-minute suite. Streaming the whole `meoclass1` tree out of the object store with a single
`git archive` took the run to **39 seconds**.

This is worth recording because a slow guard is a guard that gets run less often, and a
mutation suite is precisely the thing a tired reviewer is tempted to skip.

## 13c. E6 mutations — and the first run, which was not green

**First standalone run: 32 mutations, 30 caught, 1 ESCAPE, 1 NO-OP, 0 crashes.** Both
failures were in the harness, not the product, and both are recorded rather than smoothed
over.

**The escape — mutation L.** Pointing `authorisation_batch_key` at `batches.E5` left the
validator green. The cause: the validator **hardcoded `"E6"`** when selecting the batch from
the consolidation and never read the key at all. The field looked like provenance and
supplied none.

*Repair:* the batch is now selected **through** the manifest's own key, so a corrupted key
selects the wrong batch and the action-set comparison fails, with a dedicated
`authorisation_batch_key_matches_batch_id` check naming the fault directly. **A field a
validator does not read is decoration, and decoration in an authorisation record is worse
than nothing — it looks like provenance while guaranteeing none.**

**The no-op — mutation H.** The pattern read `resolution <strong>MSC.550(108)</strong>`;
the card reads `<strong>resolution MSC.550(108)</strong>`. The opening tag sits *before*
the word. The pattern matched nothing, the write changed no bytes, and the mutation
exercised nothing — while still reporting a "caught" result had the harness counted
unapplied mutations as passes. It does not, which is the whole reason the distinction
exists. This is E5's mutation-C incident in a new form: **an anchor that looks right in the
prose you wrote and is wrong in the markup you wrote it into.**

*Repair:* pattern corrected; H now applies at −21 bytes.

**A cheap check that should have come first.** After repairing both, every mutation was
**dry-run in memory** — applied to the file text without writing — and its byte delta
printed before the suite was launched. All 33 applied; zero predicted no-ops. That dry run
costs seconds and would have caught the H no-op before a 22-minute run. It is the right
default for any future batch.

Two mutations were also added while repairing:

* **P2** injects the 1958-Act section numbering while *leaving* the correct section block in
  place, so only `unsubstantiated_claims_absent` can catch it. P alone removed the limb
  token too, so it could have been carried by the limb check; P2 proves the forbidden-claim
  guard fires on the real card.
* **L2, Z2, Z3, Z4** guard disposition, follow-up consumption, currentness recording and
  line-ending truth respectively.

## 14. Verification

| Property | Result |
|---|---|
| Canonical total | **721 -> 721** (equality vs baseline `1b6c6c0`) |
| Question-bearing files | **86**, unchanged |
| Cards added / removed | **0 / 0**, corpus-wide |
| Cards changed corpus-wide | **exactly 6**, all authorised, 0 unauthorised |
| Edits purely additive | **yes** - 6 insert opcodes, 0 delete, 0 replace, LF-normalised |
| q-text / anchors | unchanged on every card, corpus-wide (124 files compared) |
| DOM | balanced on all six, ids unique, all under `#q-feed`, no nested lists, no inline styles, no fixed pixel widths, longest added token 18 chars |
| Candidate-visible hygiene | clean on all added text |
| `build_qb_content_index --check` | **CURRENT - no regeneration** (86 files / 721 questions) |
| `build_examiner_index --check` | **960 relationships / 7 examiners - zero delta**, 4/4 artefacts current |
| Public corpus count | **721**, unchanged. Pricing untouched |
| Determinism | **26 artefacts / 0 non-reproducible** under `PYTHONHASHSEED` 0 / 1 / 524287 |

### Full release suite - 39 gates, every one executed

39 gate records, **39 unique, 0 duplicates, 0 skipped**. Total wall time 8,677s.
**All 39 exited 0 on the first attempt.**

The Node invocation lesson from E5 held: `node --test` was given **explicit test files**
(globbed in the runner) rather than a directory, and passed first time -
**611 tests, 610 pass, 0 fail, 1 skipped, exit 0**.

### Mutations - 266 across 15 suites, 0 escapes, 0 no-ops, 0 crashes

`content_index` 26 - `batch_a` 8 - `batch_b` 10 - `batch_c` 10 - `batch_d` 12 -
`gap0609` 8 - `batch_e4` 12 - `batch_e3` 16 - `batch_e2` 18 - `batch_e1` 25 -
`batch_e5` 25 - **`batch_e6` 33** - `examiner` 13 - `ce_tip` 17 - `phase2` 33.
Every suite ended byte-identical.

**The parser caveat, met again - and this time the documented fix was re-learned the hard
way.** A first aggregation reported **8 escapes and 4 crashes**. Every one was a parsing
artefact:

* `gap0609` prints `mutations=8 escapes=0`, and a pattern of the form `(\d+)\s*escape`
  reads the **8** as the escape count. **E5's handoff documents this exact failure and its
  fix** - key on the `escapes=N` form BEFORE the bare-number form - and this session wrote
  the fallback order backwards and reproduced it.
* The four "crashes" came from `(\d+)\s*crash` matching body text of the form
  `fails=2 crash=False` - a count from a neighbouring field, not a crash.
* Two summaries were unparseable because each harness prints its own dialect:
  `26 run, 0 escape(s)`, `13 mutations, 0 escapes`, `33 mutations / 0 escapes`.

**A single regex spanning fifteen harnesses is itself a defect.** The corrected parser
selects the *last line* carrying both a mutation and an escape figure and reads key=value
forms first; it was validated against all fifteen live logs before its aggregate was
believed. **Reading a lesson is not the same as encoding it - the ordering constraint
belongs in shared code, not in prose each session must remember.**

### Audit validator - semantic result, not exit code

`validate_audit` reports **`passed 12 / failed 1 / unavailable 0`** while exiting **0**.

Run against a clean `origin/main` tree at `1b6c6c0`, the result is **identical**: same
counters, same failing check (`index_tier_literals_valid`), same detail (`43 invalid
literals`).

**PRE-EXISTING AUDIT BASELINE - ZERO E6 AUDIT DELTA.** Reported rather than counted as
green, because reading the exit code alone would call it a pass. Carried debt from E1-E5.

### Health check - the baseline comparison is VACUOUS, and that is a finding

`qb_health_check` returns **369 findings on both the E6 branch and a clean `origin/main`
tree**, compared as multisets after normalising the transport - **0 new, 0 gone**.

**That comparison proves nothing about E6, and it never could have.**
`meoclass1/qb_health_check.py` hardcodes `GITHUB_BRANCH = "main"` and downloads a tarball
from `codeload.github.com`. Its own line 33 says so: *"This checker scans the GitHub tree
rather than local disk."* It never reads the working tree.

This was **proved, not inferred**: five `q-card` tags were corrupted in the clean tree and
re-run produced a byte-identical finding set. A local regression is invisible to it.

The consequence reaches backwards. E5's handoff records *"370 findings on both the E5
branch and a clean origin/main worktree - 0 new, 0 gone"* as release evidence. Both runs
were reading the same remote `main`. **The health-check multiset baseline has been reported
as pre-merge evidence in several handoffs while being structurally incapable of detecting
the change under test.**

The check becomes meaningful only **after** push, when remote `main` carries the batch.
That post-push run is recorded in section 18.

### Gate-generated artefacts

Dirtied by the suite and by the determinism run, all reverted by **exact path**, never a
blanket restore:

* `VALIDATION_RESULTS.json` and `PHASE2_VALIDATION_RESULTS.json` - attributed to
  `validate_audit.py` / `validate_phase2.py` and their mutators. The diff is entirely the
  known stale-counter debt (`live_questions` 688 -> 721, `headings=954` -> `960`).
* `ORAL_NOTES_IMPACT.md` - attributed to `report_notes_impact.py` in the determinism
  generator chain.

All six E6 card digests were re-verified intact after every revert.

## 15. Render

**NOT BROWSER VERIFIED.** One genuine attempt was made: the preview pane serves files
outside the project folder as static snapshots that execute no JS and expose neither DOM
nor page text; `get_page_text` returned "No site is open in this tab." No browser claim is
made. This reproduces E1's and E5's findings exactly.

Substituted and clean on all six cards: div, `<p>`, `<li>`, list and `<strong>` balance;
id uniqueness; `#q-feed` parentage; q-text stability; candidate-hygiene regex over the
**added text only**; and nested-list, inline-style, fixed-width and long-token scans - all
zero. The single 80-character token on `QB9_B#q2` is the pre-existing `=====` rule inside
its stray `<pre>` block (debt item 4), not added text.

### A static-check trap worth recording

A corpus-wide comparison first reported **721 questions added**. It was an artefact:
Windows `glob` returns paths with backslash separators, so `git show origin/main:meoclass1\QB1_A.html`
failed for every file, every baseline came back empty, and every live card looked new.
Re-run with the separator normalised: **0 added, 0 removed, 0 q-text changes** across 124
files. **A comparison whose baseline silently fails to load reports the entire corpus as
new - and reads as catastrophic rather than as broken.**

### Backslashes through two layers of quoting - a third form

E1 lost a `\b` to a backspace byte and E5 lost a `\1` to a SOH byte. This session lost
backslashes three times to shell heredocs, which silently halved `'C:\'` and turned
`replace('\','/')` into a syntax error. No control byte reached any **product or tooling** artefact - all E6 Python, JSON and QB
HTML scan clean of every C0 byte except TAB, LF and CR.

**But this document did.** The paragraph you are reading was first written through a
heredoc, and the sentence naming E1's `\b` and E5's `\1` arrived on disk carrying a real
**0x08 at offset 26981 and a real 0x01 at offset 27019** - the two exact bytes it describes.
It was caught by the pre-commit control-byte scan and repaired before the commit.

The class is now confirmed across three sessions and in three distinct forms, and the
conclusion is no longer advisory: **author anything containing a backslash with a file
writer, never through a shell heredoc** - and **scan prose artefacts for control bytes too,
not only executable ones**. A handoff is release evidence; a handoff with hidden control
bytes is corrupted evidence.

## 16. New debt (5)

1. **`QB1_A#q18` cites the wrong resolution for the Maritime Single Window.** The card says
   *"FAL Amendment 2018 (Res. FAL.13(42))"*. The MSW mandate comes from **FAL.14(46)**,
   adopted 13 May 2022, in force 1 January 2024 — which introduced Standard 1.3quin. The
   **date on the card is right; the instrument and year are wrong.** Outside E6's limb (the
   addition neither touches nor restates that paragraph), so recorded rather than repaired.
   Scoped follow-up.
2. **`QB2_A#q5` cites MSC.460(101)/MSC.517(105) for mandatory lost-container reporting.**
   The instrument is **MSC.550(108)**. Different card, outside the limb. Now also a
   cross-product inconsistency with the corrected A047 text. Scoped follow-up.
3. **`QB3_J#q5` leaks internal status language to candidates** — its reg-box reads
   *"(Part-level citation; section mapping pending verification)"*. Same defect class E5
   found on `QB9_H#q4`, and now partly obsolete because A048 supplies the Part and the
   section block. Repairing it is a delete/replace outside the limb, so it stays.
4. **`QB9_B#q2` carries internal production text in candidate view** — a `<pre>` block
   duplicating the reg-box, a literal `CORRECTION FOOTER: QB8 · Q11 · v1.0` line naming the
   **wrong card id**, and repeated `---` markdown leakage. Pre-existing, outside the limb.
5. **`QB4_I#q4`'s footer reads `v1.0 · Finalised — pending Nixon final sign-off before
   gating`**, its correction mailto subject is the malformed `QQ14 Correction Required`, and
   its `data-tags` opens with a literal `**`. All candidate-visible, all pre-existing,
   all outside the limb.

Carried, unfixed, from earlier batches: `validate_audit` exits 0 while reporting `failed: 1`
(`index_tier_literals_valid`); the committed gate-result artefacts are stale and re-dirty on
every run; `qb_health_check` output order is hash-seed dependent.

## 17. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Examiner index: **960 relationships / 7 examiners**, delta zero.
- Enrichment workload: **6 → 0. ENRICHMENT IS CLOSED.**
- Follow-up workload: **35 groups**, unchanged.
- Master XLSX: **deferred**.

## 18. Post-push verification — the health check that means something

Published at `4800837` (`1b6c6c0..4800837`, fast-forward). Vercel deployment
`dpl_HKUuCAsGoptF1MbcGo4zjGysRi22` is **READY**, target production, on commit SHA
`480083728369f141c57f33678d689d8648fd34a8` — the exact pushed SHA.

Public invariants verified on the live site: **"Oral QB + Notes — ₹1,499 for one year.
721 solved oral Q&As, the examiner index and 200 pages of notes."** Count and pricing both
unchanged.

**The real health comparison.** With remote `main` now carrying E6, `qb_health_check`
returns **369 findings / 202 distinct** — against the pre-push baseline of **369 / 202**.
**0 new, 0 gone.** This is the first form of that comparison capable of detecting anything
at all (§14), and E6 introduces no new health finding.

Eight findings name an E6 destination file; all eight are in the pre-push multiset and are
therefore pre-existing. The one that reads alarmingly — *"SQ copy size differs from
meoclass1/QB1_A.html by >15% — likely diverged/stale duplicate"* — is expected: `SQ/QB1_A.html`
is the free-sample teaser, 164 KB against the paid page's 299 KB, and its `q18` is a locked
`qb-lock` card with no answer body. A047's limb lands only on the paid card, and no SQ
change was required or made.

**Recommended for the next tooling session:** give `qb_health_check.py` an opt-in local
mode (or a `--ref` argument) so the pre-merge comparison stops being vacuous. Until then,
the honest statement is that a health baseline taken before push proves nothing, and only
the post-push run is evidence.
