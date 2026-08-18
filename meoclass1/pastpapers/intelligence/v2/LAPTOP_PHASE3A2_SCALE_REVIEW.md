# Phase 3A.2 — independent Laptop scale-readiness review

**Verdict** `HOLD — QUESTION INTELLIGENCE V2 PHASE 3A.2 NEEDS ONE FINAL BOUNDED FIX`

**Reviewed** `research/question-intelligence-v2-phase3a` @ `b16cf18`
**Against** `review/question-intelligence-v2-phase3a1` @ `bea1d5d`
**Baseline** `origin/main` @ `3b55bfb` (clean, not merged into)
**Where** a worktree on `C:`, against a repository on `F:` — cross-drive by design
**Date** 2026-08-18

Both headline findings were re-tested from scratch, not read off the Desktop
summary. **R-1 passes completely.** **R-2 passes on everything it was asked to
do and fails on one thing nobody asked about**, in the same shape and the same
direction as the defect it was written to close.

---

## R-1 — required bank evidence fails closed · PASS

| Test | Result |
|---|---|
| Normal run, clean worktree | 202 checks · 0 skipped · 0 failures · exit 0 |
| Extract deleted | 177 checks · **0 skipped** · 7 failures · **exit 1** |
| Restored byte-exact | 202 · 0 · 0 · exit 0, `git status` clean |

Deletion names its own root cause — `C46 REQUIRED_SOURCE_MISSING` with the full
path — and the five downstream checks report **`unavailable`**, not `skipped`.
The distinction is the whole repair: a skip is a silence that counts as consent,
an `unavailable` is a failure with an explanation. Restoring the exact committed
bytes returns green, which proves the failure was caused by absence of required
evidence and not by damage to the test environment.

### Byte / hash integrity, independently established

`53,194` bytes · `185` items · sha256 `BA841F…BB9F8C` matching the manifest ·
**CR 0 / LF 190** · `.gitattributes` pins `*.json eol=lf`, so the LF form is what
checks out on Windows too.

### Attack matrix — mine, not the shipped fixture

| # | Attack | Result |
|---|---|---|
| A | one question text altered, **byte count preserved** (`foreign`→`distant`) | CAUGHT `C47` |
| B | one bank item removed (185→184) | CAUGHT `C34`,`C47` |
| C | declared sha256 changed, file untouched | CAUGHT `C47` |
| D | CRLF re-encode | CAUGHT `C47` |
| E | **fresh** — texts of items 1 and 2 swapped, ids and count preserved | CAUGHT `C47` |
| F | **fresh** — swap **plus** manifest sha re-declared | CAUGHT `C47` (byte count) |
| G | **fresh** — equal-length edit **plus** sha **plus** byte count all forged | see below |

Attack A matters most: it changes meaning while preserving length, so nothing
but a real hash can see it. It was caught.

**G — the honest limit.** Forging the file, its declared hash *and* its declared
byte count together defeats `C47`. What happens next depends on which item was
touched:

| Item corrupted | Result |
|---|---|
| **cited** ancestor (15, 39, 160 tested) | **CAUGHT** by `C32` + `C41` — semantically, with hash and byte count both forged |
| **uncited** item (176 of 185) | escapes |

So the semantic layer defends exactly the items that carry claims, independent
of any checksum — that is genuine defence-in-depth, and it grows automatically
as Phase 3B cites more ancestors. The residue needs a deliberate, simultaneous
two-file forgery visible in `git diff`. **Every accidental path** — drift,
re-extraction, truncation, CRLF, transfer error — is caught. Recorded as an
accepted limitation, not a blocker.

### Mutations

`48 / 0 escaped` (9 against the required source) — reproduced exactly.

---

## R-2 — marine technical magnitudes · PASS on scope, FAIL on one class

The taxonomy is real and dimensional, not decimal-detection. `FORCE`,
`VISCOSITY`, `TONNAGE`, `NAUTICAL_MILE` and `MICRON` — the five families the
3A.1 review found missing from `_UNIT_OF` — are all present and all proven
load-bearing by deletion.

Deliberate separations reviewed and endorsed: `MICRON` apart from `LENGTH_MM`;
`MASS_T` / `TONNAGE_DWT` / `GT` / `NT` kept as four measures, not one;
`SPEED_KNOT` apart from `SPEED_RPM`; `nm`, `KN` and bare `C` dropped as
ambiguous rather than guessed.

**Fresh cases, all passing** (§9–§17): 60 vs 120 N · 3.5 vs 7.0 kN · 200 vs
250 kN · 20 vs 40 microns · 25 vs 50 µm · `10 um` ≡ `10 microns` · 150 vs
500 cSt · 180 vs 380 cSt · 5 vs 15 NM · 6 vs 12 nautical miles · 500 vs 750 kg ·
5000 vs 12000 tonnes · 20000 vs 40000 dwt · dwt ≠ gt · 15 vs 30 ppm · 440 vs
690 V · 60 vs 50 Hz · 5 vs 10 bar · 30 vs 90 s · 70 vs 85 °C · 30 vs 60 A ·
500 vs 900 kW · 0.25 vs 0.50 % · 2.5 vs 4.0 bar · 1.5 vs 3.0 kN.

**1–20 window: closed.** `9, 19, 20, 21, 25, 70, 100, 1000 N` all read
`FORCE_N`; `10, 25, 100 microns` all read `MICRON`. No value becomes `COUNT`
for being either side of 20.

**Mark exclusion: correct and not overbroad.** `(4)` vs `(6)` and
`[4 marks]` vs `[6 marks]` raise no conflict; `four pumps` vs `six pumps` does.

**Unit conversion: correctly absent.** `70 N` vs `0.07 kN` yields no conflict.
Declining to equate them is the right conservative reading. No engine wanted.

### R-2-A — the blocker

`_INSTRUMENT_NUM` (`qi_similarity.py:522`) has **no leading word boundary**, so
its alternatives `no`, `reg` and `ism` match *inside ordinary words*:

```
'not less than '             -> matched 'no'    (inside "not")
'the nozzle opens at '       -> matched 'no'    (inside "nozzle")
'the governor mechanism at ' -> matched 'no'    (inside "mechanism")
'under regular survey at '   -> matched 'reg'   (inside "regular")
```

The match makes the following number a document designator, so it is dropped
**before the unit is ever read**. Thirteen of thirteen realistic marine stems
lost their load-bearing magnitude entirely:

```
not less than 4 pumps are fitted        -> []   (want COUNT 4)
the nozzle opens at 250 bar             -> []   (want PRESSURE_BAR 250)
the locking mechanism withstands 60 N   -> []   (want FORCE_N 60)
filter is not coarser than 25 microns   -> []   (want MICRON 25)
sulphur content not above 0.50% mass    -> []   (want PERCENT 0.50)
```

`number_conflict` compares only shared dimensions, so an empty set is silence,
not disagreement. The failure is therefore **silent and open** — end to end:

```
"A filter is not coarser than 25 microns. Describe its maintenance."
"A filter is not coarser than 10 microns. Describe its maintenance."
  -> EXACT_REPEAT

"A filter rated at 25 microns. Describe its maintenance."     (control)
"A filter rated at 10 microns. Describe its maintenance."
  -> SAME_CORE_ASK
```

Identical questions; the only difference is the words *is not coarser than*.
This is precisely the class R-2 was written to close — "a filter changed from
25 microns to 10 read as an exact repeat" — reopened by a missing `\b`.

**Incidence today: zero.** 0 of 185 bank items and 0 of 260 corpus stems lose a
magnitude (harness validated against known-positive and known-negative cases).
That is why no sweep row moved and why the 48 mutations did not catch it. The
defect is **latent in the present corpus and live for Phase 3B**, whose entire
purpose is ingesting 2013–2015 wording this parser has never seen. A guard that
is correct only on the text already checked is not a guard that can be scaled.

**Bounded fix** — anchor the alternation and require the period on `no.`:

```python
_INSTRUMENT_NUM = re.compile(
    r'\b(solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|annex|'
    r'chapter|regulation|reg|convention|protocol|amendment|no\.)\s*[^.;]{0,24}$',
    re.I)
```

Verified against all four genuine instrument-number controls — `SOLAS 74`,
`Annex I`, `regulation 13`, `MARPOL Annex VI regulation 14` — which stay
suppressed, while all thirteen marine stems recover their magnitude. Add a
control per false-trigger token (`not`, `nozzle`, `mechanism`, `regular`) so the
boundary itself becomes load-bearing.

### Classifier mutations

`15 / 0 escaped` reproduced. Two fresh mutations of my own, both load-bearing:

| Fresh mutation | Broke |
|---|---|
| every dimension collapsed into generic `COUNT` | `P32-F3` + 13 parser cases |
| all newly-added marine families removed at once | 6 controls + 9 parser cases |

---

## Reproduced without change

| Measure | Desktop | Laptop |
|---|---|---|
| Validator | 202 / 0 / 0 | **202 / 0 / 0** |
| Validator mutations | 48 / 0 | **48 / 0** |
| Classification controls | 52 / 0 | **52 / 0** |
| Magnitude parser assertions | 21 / 0 | **21 / 0** |
| Classifier mutations | 15 / 0 | **15 / 0** |
| Sweep exact/near | 45 | **45** |
| Sweep same-core | 37 | **37** |
| Sweep reportable | 82 | **82** |
| QP2608 DNA verified | 48/144 = 33.3% | **48/144 = 33.3%** |
| QP2608 incl. same-core | 58/144 = 40.3% | **58/144 = 40.3%** |

Paper DNA re-derived from the sweep rows, not copied: Q1(a) 10 + Q2 16 + Q4 16 +
Q8(b) 6 = 48; plus Q8(a) 10 = 58. **Double counting is suppressed** — no
`__WHOLE__` row exists for Q1 or Q8 alongside their limbs.

Previous hardening holds: describe-vs-criticise separates (`AD-1`, `P31-D1` →
`TOPIC_ONLY`), and the required/not-required, short-noun-stem,
wrong-but-valid-ancestor, duplicate-occurrence-id and fake-dated-occurrence
guards all pass inside the 52 + 202.

---

## Secondary findings

**S-1 · `adversarial_controls.py` cannot run on a stock Windows console.**
Printing `µ` raises `UnicodeEncodeError` under cp1252 and the suite exits **1**
mid-table. It fails *closed*, so it cannot manufacture a false green, but the
control suite is red on an unconfigured Laptop and needs
`PYTHONIOENCODING=utf-8`. Fix: reconfigure stdout inside the tool rather than
requiring the environment to be right.

**S-2 · documentation drift, both pre-existing.** README's Status section says
"Nothing is even `DATE_VERIFIED`" — two families are (present at `893912d`, so
not introduced here). `OFFICIAL_BANK_ITEMS.json`'s
`why_only_a_subset_is_stored` still says the 185-item extract "lives in the raw
intake directory outside git"; Phase 3A.1 committed it, and `SOURCE_MANIFEST`
says so.

**S-3 · cross-drive worktrees need `safe.directory`.** Not a code defect; noted
so the next reviewer does not read it as repository damage.

---

## Founder decisions reviewed

1. **No `--allow-missing-extract` hatch** — endorsed. The delete test only means
   something because there is no way to ask for the old behaviour.
2. **Bare `COUNT` ceiling 20 → 999** — endorsed, no unintended risk found. It
   applies only to bare integers; every unit-bearing value is parsed at any
   magnitude, and no corpus classification moved. Values above 999 still read as
   designators.
3. **`for_root()` deletion** — endorsed. No consumer exists. `qi_paths.py`
   derives every path from `__file__`, names no drive letter, and now documents
   only what it actually does. Removing a promised-but-unbuilt escape hatch is
   better than building one nobody asked for.

## Standing constraints — all confirmed

Scope contained to six files under `intelligence/v2/`. Specs, solvedQP,
oralnotes, SQ, payments, refunds, entitlements, homepage, magazine and the
Bullet Exam Plan are all **untouched**. Zero `CANDIDATE_PUBLISHED`; families sit
at `TEXT_VERIFIED` / `DATE_VERIFIED` / `RESEARCH_HYPOTHESIS`. Question
Intelligence remains **not integrated** and **research-only**. W-1 and W-2
remain recorded in the register as candidate-content maintenance items; no live
candidate file was edited.

---

## What Phase 3B needs first

One bounded repair: anchor `_INSTRUMENT_NUM`, add the four false-trigger
controls, re-run both suites and the sweep, and confirm no corpus row moves
(expected — incidence is zero today).

Phase 3B may then begin as scoped: the dated 2013–2015 DGS MEO Class-I papers
only, no blind crawl of the 832 URLs, provenance preserved per paper, output
research-only.
