# QP2302 — FEBRUARY 2023 — STAGING CHECKPOINT

**Branch:** `pastpapers/qp2302-founder-review`
**Branch baseline:** `124dfbec4db992f1abb3c46bdc65e04ea87b8e6c` (= `origin/main` at session start)
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db`
**Source SHA-256:** `5e16dca72cb492f70db244a61600f521d2d2fc4a997f6ba0d459da71752187a1`

> **This paper is NOT finished. 4 of 9 questions are authored.**
> Governed by `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §12. There is no valid half-authored state in a
> canonical spec, so **`specs/QP2302.json` has deliberately NOT been created.** The four completed
> question objects live here in staging. The next session resumes **on this same branch**.

---

## 1. STATE

| Artefact | State |
|---|---|
| `docs/QP2302_TEMPORAL_AND_DONOR_ANCHOR.md` | **COMPLETE** through §6. §7 (finalised-at-authoring) is a stub and is written last |
| `staging/QP2302/Q1.json` … `Q4.json` | **COMPLETE** — full MIW house depth, 41/41 house fields each, schema-identical to QP2303 |
| `staging/QP2302/Q5.json` … `Q9.json` | **NOT WRITTEN** |
| `specs/QP2302.json` | **NOT CREATED — deliberately.** Create only at 9/9, by guarded mechanical assembly |
| `QP2302.html` | **NOT BUILT** — deterministic from the solved spec, so it follows assembly |
| `verification/QP2302/Q1.md` … `Q9.md` | **NOT WRITTEN** — derived from the spec objects, written after assembly |

### Completed questions

| Q | Short title | Tier | Donor | Distance | Bytes |
|---|---|---|---|---|---|
| Q1 | Big Data Analytics — principles, regulatory pressure, commercial use | B | `QP2503-Q4` | +25 mo | 64 KB |
| Q2 | III Code — objectives, flag State strategy, KPIs, three State roles | A | `QP2510-Q7` | +32 mo | 62 KB |
| Q3 | EEXI design compliance, and the CII rating with AER and EEOI | A | `QP2410-Q8` | +20 mo | 75 KB |
| Q4 | Maritime against contractual salvage, liability for the award, LOF | C | `QP2408-Q7` | +18 mo | 67 KB |

### Remaining questions — donor adjudication already done, see anchor §3.1

| Q | Subject | Tier | Preferred donor | Distance | Note for the resuming session |
|---|---|---|---|---|---|
| Q5 | ISM "Effective communication" + Engine Resource Management + two near-miss examples | C | `QP2312-Q4` | +10 mo | **Prints a lone `a)` with no `b)`** — one limb, three instructions. **No casualty report is held**: the two examples must be constructed, clearly-labelled illustrative scenarios, and the answer must say so — see anchor §5.2 item 5 |
| Q6 | Bill of Lading — main function, why *to order*, when it becomes the contract | C | `QP2403-Q2` | +13 mo | Donor limbs differ (*define / distinguish types / obligations*). **No Hague-Visby article may be asserted by number** — anchor §5.2 item 4. Printed `(a) (b)` bracketed, unique on this paper |
| Q7 | High-efficiency propellers — ducted, Kappel, contra-rotating, azimuth | A | `QP2510-Q4` | +32 mo | Exact stem. `QP2403-Q4` is a tied second instance. Hydrodynamics is undated; **only the regulatory framing needs re-deriving** to EEXI/CII + Initial GHG Strategy 2018. Printed **`Cortra`** = contra-rotating |
| Q8 | MLC 2006 — flag/port State, complaint procedures, detainable deficiencies, Indian grievance redressal | C | `QP2407-Q6` | +17 mo | **No exact donor exists.** `QP2407-Q6` is two limbs only; `QP2406-Q6` is four *different* limbs. **Printed `Compliant` is a misprint for `Complaint`** — anchor §4 Q8. MLC 2022 amendments **adopted, NOT in force** (+22 mo). Limb (d) has **no donor and no held Indian source** — architecture only, no circular number |
| Q9 | CLC'92 against Bunker Convention 2001 — ships, oil, damages, limits, geography | B | **`QP2304-Q7`** | **+2 mo** | **The closest donor in the batch.** Reversed framing: donor asks *describe Bunkers, contrast CLC*; this asks *compare across four printed heads*. **NO SDR figure, tonnage band or currency conversion anywhere** — anchor §5.2 item 1. `QP2409-Q6` and `QP2402-Q2` are cross-checks only |

---

## 2. EXACT RESUME INSTRUCTIONS

```bash
git -c safe.directory=* fetch origin --prune
git -c safe.directory=* checkout pastpapers/qp2302-founder-review
git -c safe.directory=* status          # must be clean
git -c safe.directory=* log --oneline -1
```

1. **Read first, in this order:** `docs/QP2302_TEMPORAL_AND_DONOR_ANCHOR.md` (complete — do not
   re-derive the donor map or the temporal line), then this file, then `Q1.json` as the depth and
   register reference. **Do not re-run the donor recomputation**; §3 of the anchor is settled.
2. **Author `Q5.json` … `Q9.json`** into `staging/QP2302/`, one at a time, to the same house depth.
   Every question object carries all **41** house fields. Validate each against the QP2303 schema
   before moving on — the helper is reproduced at §4 below.
3. **Only when 9/9 exist**, assemble `specs/QP2302.json` by guarded mechanical assembly: the header
   block at §3 below, plus the nine staged objects **in order, unmodified**. The assembly step moves
   verified objects in; **it does not author**.
4. Build `QP2302.html` deterministically from the solved spec. Build **twice** and require byte
   identity.
5. Write `verification/QP2302/Q1.md` … `Q9.md` from the spec objects, in the QP2303 record format
   (see `origin/pastpapers/qp2303-founder-review:meoclass1/pastpapers/verification/QP2303/Q3.md`).
6. Complete **§7 of the anchor** — what changed at authoring.
7. Run the full governed QA suite (`QA_AND_HANDOVER_PROTOCOL.md`, playbook §14), including the
   HTTP UI review at 1280 and 375 with explicit server teardown.
8. **Retire staging only after the promoted objects prove byte-identical** to the staged ones.
9. Commit paper-owned files only, by explicit path. **Never `git add -A`.** Revert any regenerated
   global artefact before committing (playbook §13.2).

---

## 3. SPEC HEADER BLOCK — settled, use verbatim at assembly

```
schema_version   1.3
paper_id         QP2302
sr_no            QP-2302
month            February          year  2023        month_year  February 2023
function         Marine Engineering Management at Management Level
subject          Engineering Management
class            M.E.O. Class I
time_allowed     3 hours           total_marks  100
region_note      (India 2023)
source_copy_path meoclass1/pastpapers/docs/FEBRUARY 2023.pdf
printed_serial   2302 EM           pages  2
printed_authority                  EXAMINATION OF MARINE ENGINEER OFFICER
official_source_verified           false
carries_host_recurrence_annotation true
```

`instructions` — the four printed `NB:` items, verbatim:

1. `Answer SIX questions only.`
2. `All questions carry equal marks.`
3. `Neatness in handwriting and clarity in expression carries weightage`
4. `Blank pages if any, to be struck by (X) at the end of each question.`

**`marks_note` must record the stronger-than-QP2303 fact:** *no mark figure is printed anywhere on
this paper*, against any question or any limb. 16 per question is derived from the rubric — six
equal questions against a printed `Total Marks – 100`, giving 16.67, and every corpus question in
this format that does print a figure prints `(16)`. Six answered at 16 totals 96 against the printed
100; **that discrepancy is on the source copy and is reproduced, not corrected.**

**`transcription_verified`** — text extracted with PyMuPDF from the born-digital text layer and
carried into `text_verbatim` without retyping, whitespace normalised to single spaces and nothing
else altered; **both pages additionally rendered at 200 dpi and read in full**, and reconciled
against the text layer character by character. They agree. Host furniture — header, footer,
watermark, two advertisement blocks and the red recurrence table under every question — excluded,
and the twenty recurrence cells retained per question in `host_recurrence_hint` as intake evidence
only.

**The printed numbering is `Q1 Q2 Q3 4. 5. Q6 Q7 Q8 Q9` and is NOT normalised.** Fifteen printed
anomalies are catalogued at anchor §1.4 and every one is preserved in `text_verbatim`.

---

## 4. VALIDATION HELPER

```bash
python - <<'EOF'
import json,glob,os
ref=set(json.load(open('/path/to/QP2303.json',encoding='utf-8'))['questions'][0].keys())
for p in sorted(glob.glob('meoclass1/pastpapers/staging/QP2302/Q*.json')):
    d=json.load(open(p,encoding='utf-8'))
    print(os.path.basename(p), len(json.dumps(d,ensure_ascii=False)),
          'missing=',sorted(ref-set(d)), 'extra=',sorted(set(d)-ref))
EOF
```

A reference copy of a solved spec can be obtained without switching branches:

```bash
git show origin/pastpapers/qp2303-founder-review:meoclass1/pastpapers/specs/QP2303.json > /tmp/QP2303.json
```

---

## 5. FINDINGS THE RESUMING SESSION MUST NOT LOSE

1. **`MEPC.328(76)` entered into force 1 November 2022**, on the resolution's own operative
   paragraph 3, read at source from the text held in the corpus. The corpus amendment register's
   `2023-11-01` is **wrong**. This is the open correction request **`TSCR-3`**, which is **carried,
   not re-raised**, and **the corpus was not modified**. QP2302 is the **first MIW paper whose answer
   depends on the correction** rather than merely referencing it — Q3 is unanswerable without it.
2. **`A.1157(32)`, not `A.1187(33)`.** The 33rd Assembly adopted on 6 December 2023, ten months after
   this sitting. All three exact Q2 donors cite the later instrument, which revokes the one operative
   here. Reversed in Q2 and recorded at anchor §2.4 and §4.
3. **No ship held a CII rating at this sitting.** The first rating year began six weeks earlier and
   regulation 28 determines the rating after the calendar year ends. Q3 limb b) is written
   forward-looking throughout. **This also constrains Q1**, already authored.
4. **MLC 2022 amendments are adopted but NOT in force** — 23 December 2024, twenty-two months future.
   Binding on **Q8**.
5. **No SDR figure, tonnage band or currency conversion may appear in Q9**, although the stem prints
   "limits of liability" as a required head. Answer the *structure* of limitation: CLC carries its
   own tonnage-banded limit and a compulsory-insurance certificate; **Bunkers sets no limit of its own
   and refers out** to the applicable regime, in practice LLMC. Neither treaty text is held.
6. **Q5's two examples must be constructed and labelled as such.** No casualty report is held, so no
   named real casualty may be cited, and the answer must say plainly that the scenarios are
   illustrative.
7. **Building this paper creates the first same-year donors for `QP2308-Q9` and `QP2307-Q4`** —
   anchor §3.3. Record it in the handover; it is the production reason QP2302 was kept next.

---

## 6. WHAT HAS DELIBERATELY NOT BEEN DONE

- `specs/QP2302.json` not created — playbook §12 forbids a partly-solved canonical spec.
- No HTML built — it is deterministic from the solved spec and would misreport coverage.
- No verification records written — they are derived from the finished spec objects.
- **No global derived artefact touched.** No reuse map, manifest, index, year sheet, topic sheet or
  `solvedQP/` page has been regenerated or committed. `CURRENT_STATUS.md` and
  `history/SESSION_HISTORY.md` are untouched.
- **No source PDF committed.** The repository is public.
- **No corpus file modified.** `RulesApp-Local-Input` was consumed read-only at `319524c`.
</content>
