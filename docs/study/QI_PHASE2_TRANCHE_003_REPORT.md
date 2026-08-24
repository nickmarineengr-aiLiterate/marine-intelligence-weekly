# QI Phase-2 tranche 003 — the library at production scale

**Status: COMPLETE.** Eight families processed, zero holds.
Baseline `dbe680e`. Store: `tools/study/qi_phase2_adjudications.json`.
Contracts: `docs/study/PHASE2_PRESENT_DAY_LAYER.md`,
`docs/study/CURRENT_ANSWER_LIBRARY.md`, `tools/study/SKILL.md` §"Phase 2".

---

## The question this tranche was built to answer

Tranche 002 weighted itself six-of-twelve toward `NEW_MODERN_ANSWER_REQUIRED`
in order to **price** the creation of a present-day answer, and answered its own
question in the negative: **one of six resolved.** The other five could not be
resolved at any price, because a present-day answer had nowhere to live.

The container now exists. This tranche was weighted **five-of-eight** to test
the opposite proposition — that the library scales.

**It does. All five new-answer families resolved.** But the more useful finding
is the one nobody asked for:

> **THREE of the five needed a library answer. The reuse order disposed of the
> other two, and it did so by finding answers MIW already owned and could not
> see.**

Reading candidate owners in full — not sweeping titles — turned `QIF-EM-0064`
into a successor pointer at a solved sixteen-mark answer already in the corpus,
and cut `QIF-EM-0025` from two new answers to one. **Five library entries were
created where a naive reading would have created eight.**

---

## Selection — and it was not the easy eight

| | |
|---|---|
| Actionable pool at selection | **85** (of 107 actionable; 22 already adjudicated) |
| `NEW_MODERN_ANSWER_REQUIRED` available | **31** |
| Declared new-answer minimum | **5**, checked by `R-P2-NEW-ANSWER-BIAS` against the action **pinned at selection** |

The three verify families are the **three highest-ranked actionable families in
the corpus**. The five new-answer families are the **five highest-ranked of
their class**. No `READY_TO_STUDY_NOW` family was taken and nothing was
substituted for convenience.

| Family | Rank | Action at selection | 3Y/5Y/10Y/Full | Currentness | Final state |
|---|---|---|---|---|---|
| `QIF-EM-0185` | 36 | VERIFY | 3/3/3/3 | `CURRENT_WITH_AMENDMENT` | `CURRENT_AND_VERIFIED` |
| `QIF-EM-0251` | 39 | VERIFY | 2/2/2/2 | `CURRENTNESS_REVIEW_REQUIRED` | `UPDATED_AND_VERIFIED` |
| `QIF-EM-0253` | 40 | VERIFY | 2/2/2/2 | `CURRENTNESS_REVIEW_REQUIRED` | `CURRENT_AND_VERIFIED` |
| `QIF-EM-0080` | 102 | NEW | 0/1/2/6 | `UNKNOWN` | `NEW_CURRENT_ANSWER_CREATED` |
| `QIF-EM-0064` | 103 | NEW | 0/1/6/7 | `UNKNOWN` | `SUPERSEDED_WITH_SUCCESSOR` |
| `QIF-EM-0025` | 105 | NEW | 0/0/2/11 | `UNKNOWN` | `NEW_CURRENT_ANSWER_CREATED` |
| `QIF-EM-0043` | 115 | NEW | 0/0/6/9 | `UNKNOWN` | `NEW_CURRENT_ANSWER_CREATED` |
| `QIF-EM-0061` | 120 | NEW | 0/2/3/7 | `CURRENT_FRAMEWORK_CHANGED` | `NEW_CURRENT_ANSWER_CREATED` |

**`QIF-EM-0185` was included**, and it is still what tranche 002 said it was:
the highest-ranked unresolved actionable family, displaced by `QIF-EM-0267` and
recorded in the tranche-002 note as "the first family for tranche 003".

**`QIF-EM-0058` was NOT taken.** Its hold rests on a repealed-statute and
current-question problem, not on the missing container the library now supplies,
and its canonical rank does not place it in this tranche. It stays held with its
existing reason.

---

## What the reuse order actually did

Rule 9 — *read the answer, not the label* — changed the output on three of eight
families.

| Family | Naive plan | What reading the candidates produced |
|---|---|---|
| `QIF-EM-0064` | one library answer | **`QP2311-Q8`**, a solved 16-mark answer to this exact task. No new answer. |
| `QIF-EM-0025` | two library answers | limb A → solved **`QP2603-Q7`**; only limb B authored. |
| `QIF-EM-0061` | one library answer | two limbs, because the governed join `QIJ-0005` proves the second limb is *itself* a recurrence family. |

### Rejected owners, and why

| Family | Rejected | Reason |
|---|---|---|
| `QIF-EM-0080` | `QP2301-Q3` | types of policy, exclusions and Indian agencies — not claims |
| | `QP2411-Q6` | P&I against H&M — not claims |
| | `QP2306-Q3` | running down clause, GA expenses, unrepaired damage — a slice |
| | `QP2606-Q3` | types of loss, GA, warranties — a slice |
| `QIF-EM-0043` | `QP2512-Q4` | Maslow's motivation theory, not coping with stress-affected personnel |
| `QIF-EM-0253` | `QP2401-Q7` | **describes VIQ7 as operative** — true at its January 2024 sitting, false since 2 September 2024 |
| `QIF-EM-0185` | `QP2511-Q4`, `QP2512-Q2` | both sat **before** the 1 January 2026 IGF Code amendments |

The last two rows are the substance of the two verify families. In both cases a
framework boundary falls **inside** the family, and a family-level grant would
have blessed a pre-boundary answer. That is the `QIF-EM-0017` failure from
tranche 001, and it was avoided by naming one question rather than a family.

### The contestable decision, recorded rather than buried

`QP2311-Q8` **carries no canonical QI family** — verified in
`safe_qi_projection.json`, where its `canonical_family_ids` is empty. That was
the *second* reason tranche 002 rejected `QP2308-Q7` as an owner, so the
objection had to be answered, not ignored.

It does not defeat this owner, for two independent reasons.

1. `QP2308-Q7`'s primary disqualifier was **scope**. Here scope is not in
   doubt: `QP2311-Q8`'s own hand-written `recurrence_adjudication` **names**
   `QP2204-Q3` — the modern member of `QIF-EM-0064` — quotes its stem, and
   records it as "substantially this examiner task nineteen months earlier,
   sharing the distinctive printed phrase *hassle free slow steaming*". A hand
   adjudication at question level is **stronger** evidence than a
   similarity-derived family join.
2. The objection's substance — *the readiness layer knows nothing about it* — is
   exactly what this record cures. `QP2311-Q8`'s currentness is established
   here, in a governed Phase-2 record, for the first time.

The known imprecision from `QIF-EM-0011` carries over unchanged and is
deliberately not "fixed": because `QP2311-Q8` belongs to no family,
`project_question` will not badge it *Current answer verified*. The **routing**
is verified; the successor's own page gains nothing.

---

## The correction — `QP2606-Q4`, June 2026

Found by discharging that question's **own** `reverify_before_publication`
note, which said in terms that the approval status of the alternative-fuel
training guidelines had not been established from a primary source.

| | |
|---|---|
| The answer said | HTW 12, February 2026, **agreed draft** interim training guidelines for methyl/ethyl alcohol and for ammonia |
| Established | **MSC 111 (13–22 May 2026) APPROVED both** — one month before the sitting. **MSC 110 (18–27 June 2025)** had approved the **generic** interim guidelines they are built on — a year before it, and unmentioned |
| Class | **`CORRECTION`**, not modernisation |

Both approving sessions sat **before** June 2026, so the edit **restores**
sitting-anchoring rather than breaching it, and every session named in the
replacement text pre-dates the sitting. `R-P2-MODERNISATION-NOEDIT` is not
engaged.

**The answer's argument survives and improves.** Its discriminating point is
that the *mandatory* framework stops at the IGF Code — and approved,
non-mandatory guidelines are better evidence for that than unapproved drafts
were. The replacement text says *"None of it is mandatory"* in terms.

**Sibling checked.** `QP2312-Q4` sat in December 2023, when none of these
instruments existed, and its regulation list is correctly anchored to that date.
No correction, and it is **not** the named owner, so it keeps its own verdict.

**Restraint recorded.** The `STCW.7/Circ.` designations widely reported for
these three sets of guidelines were **not** established at source. They appear
nowhere — not in the answer, not in its sources, not in the Phase-2 record. The
approvals are cited from IMO's own session records instead.

---

## The defect production scale exposed — and it was a real one

`validate_study_qi.R-READY-SAFE` **failed on `QIF-EM-0061`** with its research
complete, its authority established, its review passed and its answers
published.

`_phase2_earned()` read only `canonical_current_answer`. A family owned **limb
by limb** has no such field, so it looked as though it answered nothing and lost
a readiness grant it had fully earned.

This is the same failure `validate_phase2_tranche` was hardened against when
limb ownership was introduced — arriving from the other side. That validator was
fixed; **this rule was not**, and the gap stayed latent for one reason worth
recording:

> The only limb-owned family before this tranche was `QIF-EM-0052`, whose
> Phase-1 triage is `UNKNOWN`. `UNKNOWN` is not in `UNSAFE_CURRENTNESS`, so the
> guard never reached it. **`QIF-EM-0061` is the first limb-owned family whose
> triage flagged a real currentness risk.**

A guard whose coverage depends on which families the corpus happens to contain
is a wasting asset. Fixed, and the fix is a **hardening**: an owner must still
exist, a limb list with no `owner_id` counts for nothing, and the other three
legs are untouched, so a hollow record still buys no `READY`.

**Mutation added: `6b limb-owned family ready with no owner`** — a limb-owned
family with a currentness risk left reading `READY` with no `owner_id` in any
slot must still be refused. The condition is **constructed** onto whichever
family carries a Phase-2 resolution rather than harvested from whichever family
happens to be limb-owned today, so it cannot expire on the next tranche. The
positive control is the baseline itself, which now contains a genuinely
limb-owned family with an unsafe triage and passes.

---

## Authority — what was checked, and what was refused

### Repo truth beat the web, and it mattered

`CA-EM-0005` was **drafted wrong and corrected before publication.** The draft
said MIW had not established the commencement of the Carriage of Goods by Sea
Act 2025 and relied on "the Hague-Visby content common to both" regimes. MIW's
own corpus had already read both 2025 Indian Acts **in the Gazette of India**
during the verification of `QP2510-Q2`:

- both the **Bills of Lading Act 2025 (Act 18 of 2025)** and the **Carriage of
  Goods by Sea Act 2025 (Act 19 of 2025)** came into force on **10 September
  2025**, vide S.O. 4083(E) and S.O. 4082(E) of 8 September 2025;
- the Schedule to Act 19 enacts the Hague Rules as amended **with
  modifications**, departing from Hague-Visby in four respects — **"goods"
  INCLUDES live animals and deck cargo**, the one-year time bar is extendable by
  three months by the court, Article IV bis is absent, and the limitation is
  666.67 units of account per package or unit or 2 per kilogramme, whichever is
  higher.

The second error was the dangerous one: a generic Hague-Visby answer teaches
that deck cargo and live animals are *outside* the rules, and under Indian law
they are *inside* it.

> **The lesson is the reuse rule applied to AUTHORITY rather than to answers.
> Before declaring a fact unestablished, check whether the corpus has already
> established it.**

### Dated findings this tranche relies on

| Fact | Date | Bearing |
|---|---|---|
| IGF Code amendments `MSC.524(106)` + `MSC.551(108)` | in force **1 Jan 2026** | boundary inside `QIF-EM-0185`; selects `QP2603-Q5` |
| `ISO 20519:2021` current, replacing 2017 | — | the bunkering procedure itself |
| SIRE 2.0 sole OCIMF tanker regime, VIQ7 withdrawn | **2 Sep 2024** | boundary inside `QIF-EM-0253`; selects `QP2504-Q7` |
| TMSA remains at **third** edition | — | "TMSA 4" would be wrong |
| MSC 110 approved generic alt-fuel training guidelines | **18–27 Jun 2025** | half the `QP2606-Q4` correction |
| MSC 111 approved methanol + ammonia training guidelines | **13–22 May 2026** | the other half |
| `MSC.396(95)` → STCW V/3 and A-V/3 | in force **1 Jan 2017** | the edge of the *mandatory* framework |
| `MSC.1/Circ.1687` ammonia safety interim guidelines | **26 Feb 2025** | safety side is also interim |
| MLC 2006 **2022 amendments** | in force **23 Dec 2024** | expands `QIF-EM-0043` beyond any sitting in it |
| `MSC.1/Circ.1598` IMO fatigue guidelines | **24 Jan 2019** | current; supersedes the 2001 guidance |
| Manila amendments adopted / in force / transitional end | **25 Jun 2010 / 1 Jan 2012 / 1 Jan 2017** | `QIF-EM-0061`, and why its printed framing is dead |
| `MEPC.395(82)` 2024 SEEMP Guidelines | adopted **4 Oct 2024**, in force **1 Jan 2026** | the one superseded citation in `QP2311-Q8` |
| Indian 2025 carriage Acts in force | **10 Sep 2025** | `CA-EM-0005` |

### What was refused

- **No `STCW.7/Circ.` numbers.** Widely reported, not read at source.
- **No resumed-session date for the IMO Net-Zero Framework.** IMO's own record
  gives no calendar date and secondary sources disagree between mid/late
  November 2026 and 4 December 2026. **MIW asserts none.** A previous MIW
  session shipped a wrong date on this very event; a declared unknown is the
  correct treatment.
- **No resolution number** for the IGF Code amendments expected in force
  1 January 2028.
- **No section numbers** from the Marine Insurance Act 1963.
- **No STCW Code table, paragraph or column-content quotations**, no qualifying
  period in months, no revalidation interval in years.
- **No convention limitation amounts**, and no rupee conversion of any unit of
  account.
- **No class figures** — permissible crack depth, grinding limit, taper contact
  percentage, survey interval — because they differ between societies.

### One vocabulary addition, documentary only

`INDUSTRY_SCHEME_PUBLICATION` was added to `authority_classes` in the Phase-2
store so that OCIMF's SIRE 2.0 and TMSA can be cited **for what they are** — a
voluntary commercial scheme with no instrument, no amendment register and no
entry into force. It is **not** added to
`validate_phase2_tranche.ACCEPTED_AUTHORITY` or
`ca_model.ACCEPTED_AUTHORITY`, so it can never satisfy an authority gate;
`QIF-EM-0253` is carried by the ISM Code and `A.1185(33)` instead. Labelling an
industry scheme *primary* would have concealed the most important fact about the
subject.

---

## Ownership, typed

| Family | Owner | Type |
|---|---|---|
| `QIF-EM-0185` | `QP2603-Q5` | `SOLVED_PAPER` |
| `QIF-EM-0251` | `QP2606-Q4` | `SOLVED_PAPER` |
| `QIF-EM-0253` | `QP2504-Q7` | `SOLVED_PAPER` |
| `QIF-EM-0064` | `QP2311-Q8` | `SOLVED_PAPER` (successor, out of family) |
| `QIF-EM-0025` L-A | `QP2603-Q7` | `SOLVED_PAPER_LIMB` |
| `QIF-EM-0025` L-B | `CA-EM-0004` | `CURRENT_LIBRARY_LIMB` |
| `QIF-EM-0080` | `CA-EM-0005` | `CURRENT_LIBRARY` |
| `QIF-EM-0043` | `CA-EM-0006` | `CURRENT_LIBRARY` |
| `QIF-EM-0061` L-A | `CA-EM-0007` | `CURRENT_LIBRARY_LIMB` |
| `QIF-EM-0061` L-B | `CA-EM-0008` | `CURRENT_LIBRARY_LIMB` |

`QIF-EM-0025` reproduces the proven `QIF-EM-0052` **mixed-ownership** pattern:
one limb on a solved paper, one in the library.

### New library entries

| Id | Title | Scope |
|---|---|---|
| `CA-EM-0004` | Surface Cracks on the Tail-End Shaft Keyway | `LIMB` |
| `CA-EM-0005` | Why a Ship Needs Marine Insurance, and How Hull and Cargo Claims Are Made | `WHOLE_QUESTION` |
| `CA-EM-0006` | Coping with Stress-Affected Personnel, and Implementing It for Better Teamwork | `WHOLE_QUESTION` |
| `CA-EM-0007` | What the Manila Amendments Changed for the Engine Department | `LIMB` |
| `CA-EM-0008` | Onboard Training and the Standard of Competence under STCW Chapter III | `LIMB` |

Library: **3 → 8 entries**, all `CURRENT_ANSWER_VERIFIED`, all `GATED`.

### Two whole-vs-limb decisions, and both were tested the other way

- **`QIF-EM-0043` is owned WHOLE.** Its second limb asks how "these elements"
  are implemented — a referent that points back into the first limb. Split, the
  second limb would dangle.
- **`QIF-EM-0061` is owned LIMB BY LIMB**, and the warrant is external: the
  governed join `QIJ-0005` records `QIF-EM-0068` as a `WHOLE_VS_LIMB_RELATION`
  at **0.9667** containment — the second limb's stem is, on its own, another
  recurrence family in the corpus. That is the strongest evidence for a limb
  split anywhere in this tranche, and it is not a bracket split.

### One historically framed stem reframed

`QIF-EM-0061`'s printed wording invites a comparison between "the existing
chapter III of the STCW 95" and "the amended chapter III". That comparison died
on **1 January 2017** when the transitional arrangements ended. Answering it
faithfully would have been more literal and less true — it would teach a
candidate to date himself by nine years. The obsolescence is stated in the
answer body, in the study guide and under `superseded_elements`; the examinable
substance survives whole.

---

## Invariants

| | Before | After |
|---|---|---|
| QI families | 270 | **270** |
| Recurrence-bearing occurrences | 1,584 | **1,584** |
| Examiner-evidence delta | — | **0** |
| Modern QI delta | — | **0** |
| Current-library items counted as occurrences | — | **0** |
| Roadmap recurrence score delta | — | **0** |
| Active study state (`study_progress.json`) | — | **unchanged** |

### Readiness

| State | Before | After |
|---|---|---|
| `READY_TO_STUDY_NOW` | 90 | **98** |
| `VERIFY_CURRENT_ANSWER` | 43 | **40** |
| `NEW_ANSWER_REQUIRED` | 31 | **26** |
| `MODERNISE_REQUIRED` | 3 | 3 |
| `CURRENTNESS_HOLD` | 12 | 12 |
| `HISTORICAL_ONLY` | 91 | 91 |

Eight families moved and nothing else did: +8 ready, −3 verify, −5 new-answer.

**No member question of any library-owned family became ready or solved.** The
grant reaches a `CA-EM-nnnn`, which matches no question id. `questions-2021.html`
and `questions-2022.html` still say MIW has not solved those papers, because it
has not.

### Topics

`QIF-EM-0185` → **D05**; `QIF-EM-0251` and `QIF-EM-0253` → **D03**. The five
new-answer families are **topic-unmapped**, and are reported as
**READY FAMILY — TOPIC UNMAPPED**. No mapping was invented to move a topic
number; mapping remains separate work, exactly as recorded for the two
tranche-002 acceptance families.

---

## Throughput — the real production cost

| | |
|---|---|
| Families processed | 8 |
| Authority research load | **heaviest single cost.** ~20 dated findings across IMO, ILO, IACS, Indian statute, ISO and one industry scheme |
| New answers authored | 5 (2 whole, 3 limb) |
| Existing solved owners reused | **5** — 4 whole, 1 limb |
| Existing library owners reused | 0 |
| Duplicate answers avoided | **2**, one of them a full 16-mark engineering answer |
| Sitting-date corrections | 1 (`QP2606-Q4`) |
| Governance defects found and fixed | 1 (`R-READY-SAFE` limb blindness) |
| Holds | **0** |

### Complexity per family

| Family | Complexity | Where the cost was |
|---|---|---|
| `QIF-EM-0185` | **MEDIUM** | locating the amendment boundary; the answer needed nothing |
| `QIF-EM-0251` | **HIGH** | two IMO sessions established, then a spec correction and a rebuild |
| `QIF-EM-0253` | **LOW** | one date, one negative finding (no TMSA 4) |
| `QIF-EM-0064` | **HIGH** | adjudicating a family-less owner against a standing precedent |
| `QIF-EM-0025` | **MEDIUM** | reading the solved candidate in full; then one limb authored |
| `QIF-EM-0080` | **HIGH** | Indian statute book rebuilt in 2025; drafted wrong, corrected |
| `QIF-EM-0043` | **MEDIUM** | one dated treaty amendment; long answer |
| `QIF-EM-0061` | **HIGH** | reframing an obsolete stem, two limbs, two entries |

**Recommended next tranche size: 8.** Not larger. Five of these eight were
`HIGH` or `MEDIUM` on authority research, and the two findings that most
improved the product — the `R-READY-SAFE` defect and the `CA-EM-0005`
correction — both came from *slack*, not from throughput. A twelve-family
tranche would have found neither.

---

## Known debts, untouched

- `export_roadmap_xlsx.py` is **not byte-deterministic**. Pre-existing.
- The `"added"` row in `solvedqp_content_index.json` inherits the paper's
  `updated` date, so `QP2606`'s "June 2026 added" note now reads 2026-08-24.
  Pre-existing generator behaviour, observed and **not** fixed here.
- Current-answer **search integration** remains deliberately deferred. The
  content indexes changed only by a `generated` date and the new correction-log
  row; **zero** `CA-EM` references were added to either.
- No **current-answer browse index** was built. Direct family, archive and topic
  routes are sufficient.
- No **2010–2020 archive**. The boundary remains 2021–2022 wording archive and
  2023–2026 solved index.
- `QIF-EM-0058` and the three other `HOLD_NO_CURRENT_ANSWER_OWNER` families
  stay held with their existing reasons.
- 40 families remain `VERIFY_CURRENT_ANSWER`; 26 remain `NEW_ANSWER_REQUIRED`.
