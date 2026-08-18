# Phase 3A.2 repair register — the last two holes before scale

**Authority** Laptop independent review of Phase 3A.1, `bea1d5d` on
`review/question-intelligence-v2-phase3a1`, verdict **HOLD — one final bounded
repair**. Thirteen of fourteen Phase-3A.1 claims were independently confirmed;
this register closes the fourteenth and the recommendation beside it.

**Lineage** continued on `research/question-intelligence-v2-phase3a` from
`893912d`. Nothing merged. Question Intelligence remains research-only.

---

## R-1 — a required source must be required

### What was wrong

`load_extracted_bank()` returned a bare `None` for "absent", and six checks read
that as "this machine lacks the intake directory". That was true in Phase 3A,
when the extract lived outside the repository. Phase 3A.1 committed the
extract — and nobody revisited the function, so the meaning of absence
inverted without the code noticing. What used to say *this machine has no
intake* now said *someone removed the evidence*, and the validator answered
that with exit 0.

Reproduced here before any edit, exactly as the Laptop measured it:

```
extract     : ABSENT - two checks skipped
checks run  : 170        SKIPPED : 5        FAILURES : 0        EXITCODE=0
  ~ C32  ~ C33  ~ C40  ~ C41  ~ C42
```

C40–C42 are the Phase-3A.1 headline repair — the semantic wrong-but-valid-
ancestor guard built to close the Laptop's LC-3 finding. Deleting one tracked
file switched them off and reported success. The banner said "two checks
skipped" while five skipped, which is the tell that the branch was never
revisited after C40–C42 were added.

### What changed

`load_extracted_bank()` now returns `(items, problem)` and states *why* the
extract is unusable. **C46** is the root check and names the artefact:

```
C46 the required DGS bank extract is present and loadable:
    REQUIRED_SOURCE_MISSING: <path> - file does not exist
```

The six downstream checks report one shared reason —
`unavailable - C46 REQUIRED_SOURCE_MISSING` — rather than six rival
explanations of the same single fact. **Nothing skips.** There is no
`--allow-missing-extract` escape hatch: the Laptop offered one if a genuine use
case existed, and none does. A tracked file is either checked out or the
checkout is broken.

**C47** closes the gap sitting next to it, found in this pass: the manifest has
carried `extracted_json_sha256` and `extracted_json_bytes` since Phase 3A.1 and
**no tool ever read either**. The extract could be edited at will provided the
edit left 185 well-formed items. The hash is now verified against the bytes
actually checked out. That also holds the line on the CRLF trap — `.gitattributes`
pins `*.json` to LF, and if that pin were ever lost, C47 is what notices.

| | before | after |
|---|---|---|
| extract present | 200 checks, 0 skips, 0 failures, exit 0 | **202** checks, 0 skips, 0 failures, exit 0 |
| extract deleted | 170 checks, **5 skips**, 0 failures, **exit 0** | 177 checks, **0 skips**, 7 failures, **exit 1** |

### Proof

Nine required-source mutations, permanent in `--mutate`. They corrupt the
**file**, not the in-memory documents, because no in-memory mutation can reach
a defect in how a file's absence is interpreted. Each writes its variant to a
temporary directory and repoints the module at it, so a crash mid-table cannot
leave the repository holding a corrupted extract.

| mutation | caught by |
|---|---|
| delete the required bank extract | C46 |
| leave the extract unparseable as JSON | C46 |
| strip the `items` object out | C46 |
| blank the text of one item | C46 |
| remove one of the 185 items | C34 / C47 |
| alter the canonical text of one item | C32 / C47 |
| re-encode the extract with CRLF | C47 |
| change the declared sha256, touching nothing else | C47 |
| change the declared byte count, touching nothing else | C47 |

**9 of 9 caught, 0 escapes.** Total validator mutations 39 → **48**, escapes 0.

The extract is unchanged by all of this: 185 items, 53,194 bytes, sha256
`BA841F9A98C49FFBD15599481B2D62DD3B56B2CDC0A6DC43ECB83B6252BB9F8C`, zero CRLF.

---

## R-2 — marine engineering does not stop counting at 20

### What was wrong

Phase 3A.1 typed magnitudes by dimension and fixed the 1–20 window for the
dimensions it knew. It did not know the marine ones. Where a dimension was
missing, the window was still open underneath it, in its original shape:

```
'25 microns' -> []                 '70 N'   -> []     '180 cSt' -> []
'10 microns' -> [('COUNT','10')]   '100 N'  -> []     '380 cSt' -> []
```

The conflict test requires both sides non-empty, so a filter changed from 25
microns to 10 read as an **exact repeat**. Recurrence is the product; a missed
numeric conflict is a false recurrence claim, and it was waiting for scale.

### What changed

A dimension is now a **quantity at a scale**, not a quantity. Newtons and
kilonewtons are separate keys, as are millimetres and kilometres.

This is the honest treatment of `70 N` against `0.07 kN`: they share no
dimension, so **neither a conflict nor an equality is asserted**. The layer does
no unit conversion and will not guess one — the Founder brief's own instruction
was, at minimum, not to classify them as conflicting without proving conversion
semantics. **This is a documented limitation, held as control `P32-F3`, not a
repair.** Equivalent *spellings* of one scale (`micron` / `um` / `µm` / `μm`) do
share a key, because that is normalisation, not conversion.

Casing is consulted before folding, so `NM` is a nautical mile while `nm` —
nanometre or nautical mile, with nothing to settle it — is dropped. Shouted `KN`
(kN or kn?) and bare `C` (Celsius or a category letter?) are dropped for the
same reason. Conservative refusal beats a clever guess.

Dimensions added: **FORCE** (N, kN, MN), **VISCOSITY** (cSt, mm²/s, mPa·s,
Pa·s), **TONNAGE** (dwt, gt/grt, nt/nrt) beside cargo **MASS** (kg, t), 
**NAUTICAL DISTANCE** (NM, nautical mile), **MICRON** (µm, μm, um, micron),
**CURRENT** (A, mA, kA), **ENERGY** (Wh, kWh, MWh, MJ), **PPB**, and
**TEMPERATURE_K**. Grouped thousands (`50,000 dwt`) are one number; joined forms
(`70N`, `25µm`, `0.50%`) are the same magnitude as their spaced forms; the digit
ceiling rose from 4 to 9.

### Two over-claims found here, which the review did not reach

Every case the Laptop raised was an **under**-claim — a conflict that should
have fired and did not. Auditing the table rather than the test values surfaced
two of the opposite sign, where Phase 3A.1 read two *different* quantities as
one magnitude because a key lumped several scales together:

- one `VOLT` key covering V and kV, so **440 V read as 440 kV**;
- one `SPEED` key covering knots and rpm, so **100 rpm read as 100 knots**.

Both are held as parser assertions.

### The bare-integer window

`COUNT` — a bare integer with nothing naming what it measures — is not a
technical magnitude, and its ceiling is a separate question from R-2. It rose
from 20 to 999. **No numeric range gates a unit-bearing quantity any more.**

### Mark allocation — unchanged and re-proven

The exclusion strips **parenthesised** digits only. `(4)` vs `(6)` and
`[4 marks]` vs `[6 marks]` on an otherwise identical stem remain `EXACT_REPEAT`
(`P31-M5`). A spelled technical quantity in the examiner's own words survives:
`minimum four pumps` vs `minimum six pumps` reaches `SAME_CORE_ASK` (`P32-X1`),
and `within 30 seconds` parses as `TIME_SECOND 30`.

The Laptop's **R-3** note is recorded and not acted on: `within (30) seconds`
extracts nothing, because the marks pattern cannot tell an annotation from a
parenthesised quantity. Real stems rarely parenthesise a quantity, and the
adjacent `No. (4) unit` is correctly suppressed twice over. Recorded as a known
edge, per the review.

### Proof

**14 new controls** (P32-*) covering force, micron, viscosity, tonnage/mass,
nautical distance and the spelled-quantity guard; **21 parser assertions**
covering normalisation, conservative refusals, both over-claims and the
exclusions; **6 new dimension mutations** that delete one family of units at a
time, plus the existing 1–20 restoration extended to the new controls.

| mutation | must break | broke |
|---|---|---|
| force units unknown | P32-F1, P32-F2 | both |
| micron / particle size unknown | P32-P1 | yes |
| viscosity unknown | P32-V1 | yes |
| tonnage and mass unknown | P32-T1/T2/T3 | all three |
| nautical distance unknown | P32-N1, P32-N2 | both |
| decimals ignored | P32-F2, P31-M1 | both |
| numbers narrowed back to integers 1–20 | 8 controls | all eight |

**Controls 38 → 52, failures 0. Classifier mutations 9 → 15, escapes 0.
Parser assertions 21, failures 0.**

---

## Self-adversarial findings — beyond R-1 and R-2

**SA-1 — a portability claim nothing implemented.** `qi_paths.py` documented
that "`--repo-root` is accepted by the tools for the case of running against a
different checkout", and shipped a `for_root()` helper to serve it. **No tool
accepts the flag and nothing calls the function** — repo-wide, the only two
occurrences are the claim and the definition. A portability layer, reviewed
twice for portability, may not document an escape hatch that does not exist.
The claim and the dead helper are both removed, and the docstring now states
what is actually true: paths derive from the module, so pointing a tool at
another checkout means running that checkout's own copy.

**SA-2 — magnitude parsing asserted directly.** The class-level controls cannot
isolate a parser defect whose two stems differ lexically anyway, which is
exactly the shape of both over-claims above. `NUMERIC_PARSER_CASES` asserts
`(text → dimension → value)` with no classification in between, and a `None`
expectation asserts *silence* — that a conservative refusal really refuses.

---

## Recomputation — honest, and unmoved

No threshold was tuned. The sweep was recomputed against a worktree at the
pre-R-2 commit and diffed **row for row**, not compared on totals:

| | before | after |
|---|---|---|
| exact/near | 45 | **45** |
| same core ask | 37 | **37** |
| reportable matches | 82 | **82** |
| QP2608 Paper DNA | 48/144 = 33.3% | **unchanged** |
| including same-core | 58/144 = 40.3% | **unchanged** |

**Zero classification changes**, so there is no adjudication table to present.
That is the expected result and not a comfortable one to assume: the corpus is
40 modern specs against a bank whose stems rarely carry a marine magnitude at
all. The repair is for what ingestion is about to bring, which is precisely why
the Laptop flagged it before scale rather than after.

Untouched and re-verified green: the primary/secondary demand model, the
negation and polarity model, the actor model, containment, the short-stem
guard, bank semantic ancestor logic (C40–C42), date derivation (C36–C38),
EM-0008 = BANK-160 / EM-0009 = BANK-039 (C44), and dated filenames (C45).

## Recorded, not acted on

- **W-1** — `oralnotes/miw-notes-mgmt-p15.html:432` describes MS Act 1958
  Part XIV as "limited savings" when it is the substantive coasting-trade Part.
  Registered in `CURRENT_ANSWER_CORRECTION_CANDIDATES.md` with file, claim,
  problem, authority, severity and a bounded correction. **No candidate file was
  edited.**
- **W-2** — bare "Part XIV" is ambiguous between the 1958 and 2025 Acts.
  Registered likewise; a naming convention is adopted for this research layer
  only.
- Company / Administration actors — **deferred to Phase 3B**, per the review.
- EXPLAIN vs LIST calibration — **accepted as-is**.
- Coastal Shipping Act commencement — **COMMENCEMENT_UNVERIFIED**.
- 2010–2012 — unsupported. NTA — closed. Dieselship — not purchased.

## Status

Candidate-facing: **NOT PUBLISHED**. Website: **NOT INTEGRATED**. Bullet Exam
Plan, commercial/payment code and magazine: **untouched**. Phase 3B: **not
started**.
