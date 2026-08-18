# Phase 3A.3 repair register — four characters in an ordinary word

**Authority** Laptop independent scale-readiness review of Phase 3A.2,
`6a6b6a4` on `review/question-intelligence-v2-phase3a2`, artefact
`LAPTOP_PHASE3A2_SCALE_REVIEW.md`, verdict **HOLD — one final bounded fix**.
R-1 passed completely. R-2 passed on everything it was asked to do and failed
on one class nobody had asked about.

**Lineage** continued on `research/question-intelligence-v2-phase3a` from
`b16cf18`. Nothing merged, nothing published. Question Intelligence remains
research-only and is not integrated into the site.

---

## R-3A — the reference-suppression rule had no word boundary

### What was wrong

`_INSTRUMENT_NUM` suppresses the number that follows a document-reference
token, so that `SOLAS 74` and `regulation 13` are read as the names of
documents rather than as quantities an answer must match. Every alternative in
it was a bare substring:

```python
r'(solas|marpol|...|isps|ism|annex|chapter|regulation|reg|convention|'
r'protocol|amendment|no\.?)\s*[^.;]{0,24}$'
```

`no`, `reg` and `ism` therefore matched *inside ordinary words*. Reproduced at
`b16cf18` before any edit:

```
a filter is not coarser than 25 microns   -> []   (want MICRON 25)
the nozzle opens at 250 bar               -> []   (want PRESSURE_BAR 250)
the locking mechanism withstands 60 N     -> []   (want FORCE_N 60)
under regular testing at 440 V            -> []   (want VOLT_V 440)
normal running speed is 750 rpm           -> []   (want SPEED_RPM 750)
the regulating valve lifts at 7 bar       -> []   (want PRESSURE_BAR 7)
the registration survey covers 12 months  -> []   (want TIME_MONTH 12)
the isolating mechanism trips at 30 A     -> []   (want CURRENT_A 30)
sulphur content not above 0.50% mass      -> []   (want PERCENT 0.50)
not less than 4 pumps are fitted          -> []   (want COUNT 4)
```

Ten of twelve realistic marine stems lost their load-bearing magnitude
entirely.

### Why it was silent

The number is discarded **before its unit is ever read**, and
`number_conflict` compares only the dimensions the two sides *share*. An
emptied set is therefore silence, not disagreement — the classifier does not
report "these differ", it reports nothing at all, and the stems fall through to
the lexical layer identical. End to end:

```
"A filter is not coarser than 25 microns. Describe its maintenance."
"A filter is not coarser than 10 microns. Describe its maintenance."
  -> EXACT_REPEAT
```

This is precisely the class R-2 was written to close, reopened by a missing
`\b`. The failure is silent and **open**: it does not refuse, it agrees.

### Root cause

The expression was written as a list of words but compiled as a list of
substrings. Nothing in the suite tested a stem whose ordinary vocabulary
happened to contain one, so the gap was invisible to 48 validator mutations and
15 classifier mutations alike.

### The repair

```python
_INSTRUMENT_NUM = re.compile(
    r'(?:\b(?:solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|'
    r'annex|chapter|regulation|reg|convention|protocol|amendment)\b\.?'
    r'|\bno\.)\s*[^.;]{0,24}$',
    re.I)
```

Both boundaries, not one. Two points decided here rather than copied:

**A leading boundary alone is not enough.** The review proposed `\b(...)`, and
that closes `not`, `nozzle` and `mechanism` — but `regular`, `regulating` and
`registration` all *begin* with `reg`, so a leading boundary matches them
happily. Tested directly before adopting anything:

| expression | false triggers | genuine references missed |
|---|---|---|
| shipped at `b16cf18` | 13 | 1 |
| leading boundary only (as proposed) | 3 | 1 |
| **both boundaries (adopted)** | **0** | **0** |

The three survivors of the proposed form are `regular`, `regulating` and
`registration`. They are now a permanent mutation (`P33-2`), so the difference
cannot be lost again.

**`no` must carry its period.** Anchoring both ends still leaves `\bno\b`
matching the negation in *"no more than 25 microns"*. The designator is always
written `No. 4`, so `no` alone is required to be `no.` while the other tokens
take an optional period. That optional period also closes a pre-existing gap:
`Reg. 14` was **not** suppressed at `b16cf18`, because `[^.;]` could not cross
the period between the token and the number. It is suppressed now.

`Rule 21`, `section 5` and `paragraph 3` were never in the alternation and are
still not suppressed. Adding them would be a new feature and would move corpus
rows; it is recorded here, not done.

---

## R-3B — the boundary is now load-bearing

Fourteen classification controls (`P33-*`) and twenty parser assertions were
added. Every false-trigger token named in the review has a control, plus four
further realistic stems that carry the dangerous substrings naturally —
`normal`, `regulating`, `registration`, `isolating mechanism` — and two more
(`numbered`, `isometric`) at the parser.

**They run in pairs.** The `-1` case proves the magnitude survives
preprocessing and still separates the two questions; the `-2` case holds every
word constant and repeats the value, proving the separation came from the
quantity and not from the sentence around it. A one-sided test could be passed
by a parser that had simply stopped suppressing anything at all.

Controls run through the full `classify()`, not `numbers()` alone, so what is
proven is the product consequence — `SAME_CORE_ASK` where the values differ,
`EXACT_REPEAT` where they do not — and not merely a parser return value.

Genuine suppression is asserted in the same table: `regulation 13`, `Reg. 14`,
`reg 14`, `No. 4`, `ISM 9`, `chapter 9` and `MARPOL Annex VI regulation 14` all
still yield no quantity.

### Regex mutations

The boundary is not a classifier option, so it cannot be switched off through
`Options`. A third mutation table substitutes weaker expressions directly and
requires each to break something:

| mutation | result |
|---|---|
| `P33-1` the 3A.2 defect restored, unanchored | broke 16 |
| `P33-2` leading boundary only | broke 5 |
| `P33-3` period dropped from `no.` | broke 2 |

`3 mutations, 0 escaped`. If any weaker expression had passed the whole suite,
the boundary would have been decoration.

---

## R-3C — the control harness now runs on a stock Windows console

Review finding S-1. `adversarial_controls.py` printed `µ` — a real datum, since
`25 um` and `25 µm` must stay distinct in the corpus — and a default cp1252
console cannot encode it, so the suite raised `UnicodeEncodeError` halfway down
the table and exited 1 without a verdict.

It failed **closed**, so it could never manufacture a false green. But a
control suite that is red on an unconfigured machine is not portable, and
requiring `PYTHONIOENCODING=utf-8` to be set by hand is exactly the environment
dependence the rest of the model was cleaned of.

`_make_stdout_printable()` reconfigures this tool's own stdout and stderr to
UTF-8 with `backslashreplace`, falling back to a `TextIOWrapper` where
`reconfigure` is unavailable. It is **display only**: no test datum is altered,
the classifier still compares the unmodified source strings, and the semantic
result is identical under both consoles. The change is confined to the test
harness; no production runtime encoding is touched.

---

## Accepted limitation — coordinated forgery of an uncited item

Carried forward from the review's attack matrix (attack G), **accepted by the
Founder before Phase 3B**.

An attacker who simultaneously changes an **uncited** bank item, forges the
manifest's declared sha256, *and* forges its declared byte count defeats `C47`
and escapes. The residue is bounded and understood:

- Every **cited** ancestor is additionally verified semantically by `C32` and
  `C41`, which catch the attack with hash and byte count both forged. 15, 39
  and 160 were tested by the reviewer.
- 176 of 185 items are presently uncited; the exposure shrinks automatically as
  Phase 3B cites more ancestors, because semantic coverage follows citation.
- Every **accidental** path — drift, re-extraction, truncation, CRLF
  re-encoding, transfer error — is still caught.
- The attack requires a deliberate, simultaneous two-file edit that is plainly
  visible in `git diff`.

No semantic verification of all 185 items was built, and no signature
infrastructure was invented. Both were considered and declined as
disproportionate to a residue that git already exposes.

---

## What did not move

The repair changes what the parser does with words it previously mis-read, so
the corpus was checked rather than assumed. The full sweep was run at `b16cf18`
in a separate worktree and again after the repair, and the two outputs are
**byte-identical**:

```
reportable 82 · strong (exact/near) 45 · same core ask 37     both runs
```

Zero rows moved, matching the review's measured incidence of the defect —
0 of 185 bank items and 0 of the corpus stems. That is why 48 validator
mutations and 15 classifier mutations never caught it, and why the defect was
latent today and live for Phase 3B, whose whole purpose is ingesting 2013–2015
wording this parser has never seen.

QP2608 Paper DNA recomputed from the live sweep rows, unchanged:
**48/144 = 33.3%** verified, **58/144 = 40.3%** including same-core, with
double counting suppressed — `Q1` and `Q8` contribute their limbs, not their
`__WHOLE__` rows.

---

## Test profile

| Suite | Result |
|---|---|
| `validate_families.py` | 202 checks · 0 skipped · 0 failures |
| `validate_families.py --mutate` | 48 mutations · 0 escaped |
| classification controls | 66 · 0 failures |
| magnitude parser assertions | 41 · 0 failures |
| classifier mutations | 15 · 0 escaped |
| regex mutations | 3 · 0 escaped |
| stock Windows console, no `PYTHONIOENCODING` | exit 0 |
| extract deleted | 177 checks · 0 skipped · 7 failures · exit 1 |
| extract restored byte-exact | 202 · 0 · 0 · exit 0 |

Extract integrity independently re-established: 53,194 bytes · 185 items ·
sha256 `BA841F…BB9F8C` · CR 0 / LF 190.

---

## Still open, unchanged

**W-1** `miw-notes-mgmt-p15.html` Part XIV "limited savings".
**W-2** bare Part XIV ambiguity across the 1958 and 2025 Acts.

Both remain **record-only** candidate-content maintenance. No candidate file
was edited in this repair.

**S-2** documentation drift noted by the reviewer — the README Status line and
`OFFICIAL_BANK_ITEMS.json`'s `why_only_a_subset_is_stored` — is pre-existing,
outside this bounded scope, and left for separate maintenance.
