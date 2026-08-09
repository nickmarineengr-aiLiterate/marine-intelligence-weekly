# 2025 PRODUCTION STRATEGY

**Written in the review session, 2026-08-09, on branch `pastpapers/2026-v1-product-review`.**
**No 2025 production was started. No transcription, no spec, no answer.**

---

## 1. THE SOURCE SET — RE-VERIFIED THIS SESSION

Eleven files under `meoclass1/pastpapers/docs/`, all `EXAMINATION OF MARINE ENGINEER OFFICER`,
subject `ENGINEERING MANAGEMENT`, nine questions each. **≈99 question instances.**

Serials were extracted from page 1 of each PDF this session rather than taken from the earlier
inventory:

```
2501  2502  2503  2504   ——   2506  2507  2508  2509  2510  2511  2512
 Jan   Feb   Mar   Apr   MAY   Jun   Jul   Aug   Sep   Oct   Nov   Dec
                          ^
                          no 2505 exists
```

> **CONFIRMED INDEPENDENTLY. May is the examiner's gap, not a hole in the Founder's file set — and
> May is absent in 2026 as well.** This matters beyond bookkeeping: it is the evidence behind the
> sentence a candidate reads on `questions-2026.html`, so it had to be verified rather than
> inherited.

**Git hygiene — checked and clear.** `.gitignore:42` covers `meoclass1/pastpapers/docs/*.pdf`, and
`git check-ignore` confirms all eleven 2025 files and all six 2026 files are ignored. The risk
flagged in `CURRENT_STATUS.md` §20 is closed. **Do not commit them; do not delete them.**

---

## 2. THE PROPOSED METHOD — CONFIRMED, WITH TWO CHANGES

The Founder's A→E staging is right and is adopted. Two modifications follow from six papers of
evidence.

### STAGE A — transcribe all eleven papers first, questions only

Character-level transcription with the same visual verification every 2026 paper received: text
extracted with PyMuPDF, then every page rendered and read against the extraction. No answers, no
routes, no study guides.

**CHANGE 1 — Stage A must produce a real spec, not a scratch file.** Write `specs/QP25xx.json`
carrying the paper block, the nine question stems, subparts, printed marks, and nothing else. The
existing `build_index.paper_status()` already renders a paper as `coming_later` until answers exist,
so an answerless spec is safe: **holding questions can never make a paper read as solved.** This
also means the toolchain validates the transcription immediately instead of a month later.

> **Verified this session: no change is needed.** `validate_spec.py:563-583` treats
> `answer_status: "Not Built"` as a first-class state — `built = st not in ('Not Built',
> 'Drafting')` — and every answer-layer requirement (`model_answer`, `study_notes`, `answer_route`,
> `verification_file`, `sources`) is gated behind `built`. An answerless spec validates cleanly
> today, and the validator will reject it the moment someone adds a `model_answer` without
> promoting `answer_status`. Stage A can start immediately.

### STAGE B — generate `questions-2025.html`

**Nothing to build.** `build_questions_year.py` is generic: it derives years from the specs, months
from the data, and known-absent sittings from a table that already contains `(2025, 5)`. Dropping in
a 2025 spec produces `questions-2025.html` with **no code change**, exactly as `topics-<year>.html`
already behaves.

### STAGE C — cross-year recurrence

`recurrence_model.py` is already cross-year: it loads every spec, unions families over the whole
corpus and orders by `(year, month)`. Adding 2025 automatically:

- links 2025↔2025 and 2025↔2026 families;
- **re-ranks 2026 questions that currently read "Set once"** — a 2026 question with a 2025 ancestor
  becomes a repeat, and its 2025 ancestor becomes the first occurrence;
- keeps direction correct without any spec edit, because direction is computed from the calendar.

> **This is the payoff of fixing the chronology model before 2025 rather than after.** Had the year
> sheet shipped reading `recurrence_class`, every 2026 tag would have needed manual revision.

**CHANGE 2 — expect the 2026 "Set once" count to fall, and treat that as the product improving.**
33 of 54 are singletons today. That number is scoped to the sittings MIW has transcribed, the pages
say so, and it will drop when 2025 lands.

### STAGE D — reuse map

Classify every 2025 question A/B/C/D and EXACT/NEAR/TOPIC/NONE against the whole corpus, using the
established rules:

- **String comparison of transcribed stems establishes EXACT.** Nothing else does.
- **Similarity ranking is discovery only.** It has already failed three ways in this corpus: it
  ranked the wrong neighbour (June Q3), it scored genuine one-to-one task matches at 0.15 because
  the stems differ in length (April Q6, Q7), and it flagged a homonym (June Q4 "decarbonisation").
- **Human adjudication decides.** Of 55 sweep hits in April, exactly one was a defect.

### STAGE E — solved production, cheapest-first

Research only what genuinely needs research. With ~99 new instances against 54 built, a large
fraction will be Tier D reuse.

**Tier D carries three mandatory steps, all proven over two papers and none optional:**

1. Scan the reused object for **sitting-relative prose** — `this paper`, `this sitting`, `this
   examination`, `weeks/months before`, a named month-year, a cross-reference to another question by
   number.
2. **Sweep the assembled spec afterwards.** Never trust the patch list: it missed one in March and
   one in April, and the sweep caught both. Adjudicate every hit by hand.
3. **Check whether the governing instrument itself differs at the two sittings.** This is the
   category above re-anchoring, and 2025 makes it sharper than 2026 did — see §3.

---

## 3. THE 2025-SPECIFIC RISK NOBODY HAS FACED YET

> **Every 2025 sitting falls BEFORE the Merchant Shipping Act, 2025 commenced on 15 March 2026.**

So every 2025 question touching Indian shipping law is answered on the **Merchant Shipping Act,
1958** — the statute repealed by s.324(1) of the 2025 Act. The 2026 set had this problem on one
boundary; 2025 has it on **all eleven papers at once**, in the opposite direction.

Two consequences:

1. **Reusing a 2026 answer into a 2025 paper is a statute regression, not a re-anchor.** QP2604 Q7
   re-authored limb (c) onto the 2025 Act because April fell after commencement. Pulling that answer
   back to a 2025 sitting requires re-authoring it *back* onto the 1958 Act. The April sweep found
   the 1958 Act asserted on **eight separate surfaces** of the January object — model answer, study
   guide, `recall_15s`, `major_trap`, an `answer_route` core point, a retrieval card, `regulations`
   and `search_aliases`. Expect eight again, in reverse.
2. **A 2025 answer must not be "corrected" to the current law.** It answers the examination as sat.
   The study guide is where the candidate is told the law has since changed — that is what the
   three-layer rule is for.

**RECOMMENDATION — run a single statute-boundary pass across all eleven 2025 papers before any Tier
D reuse begins**, listing every question that touches Indian shipping legislation. Cheaper once than
eleven times, and it makes the reuse map honest.

---

## 4. HOST RECURRENCE TAGS — DISCOVERY ONLY

The 2025 files carry the same host-printed annotations (`2024/MAR/Q5`) as the 2026 set.

**They are not authority and must never reach a spec, a generated page or the manifest.** The 2026
set measured them wrong in both directions on four questions across two papers. Canonical recurrence
comes from actual question wording plus human-reviewed examiner demand.

**Host branding must never be committed** — this repository is **public**. `validate_spec.py` rejects
`host_branding` and trap 14 scans pages, specs *and* the manifest.

See also `2026_SIX_PAPER_INTELLIGENCE_REVIEW.md` §2.4: the host table currently renders on the paper
and topic pages in `--publish` mode. **That should be settled before 2025 multiplies it by eleven.**

---

## 5. SEQUENCING AND EFFORT

| Stage | Output | Rough scale |
|---|---|---|
| A | 11 answerless specs, transcribed and visually verified | the bulk of one focused session per 3–4 papers |
| B | `questions-2025.html` | **zero** — generator already generic |
| C | cross-year families over 165 questions | one pass, mostly automated |
| D | reuse map, A/B/C/D + EXACT/NEAR/TOPIC/NONE | one session, human adjudication throughout |
| E | solved production, cheapest-first | the long tail |

**Do Stage A completely before Stage E starts on any paper.** The 2026 set showed that recurrence is
only visible once the whole year exists: June's profile (EXACT 0 · NEAR 0 · TOPIC 4 · NONE 5) was
unlike March's (3 · 0 · 5 · 1) and April's (0 · 7 · 1 · 1), and no early paper predicted the others.
Solving papers one at a time in calendar order would repeat research that a completed reuse map
would have avoided.

**Commercial note:** Stage B alone doubles the free discovery surface — a 2025 question sheet with no
answers — and is nearly free. It is the highest return-per-hour item on this list and should not
wait for Stage E.

---

## 6. WHAT MUST NOT HAPPEN

- **Do not start 2025 solved-answer production** until the reuse map exists.
- **Do not commit or delete the source PDFs.**
- **Do not let a host recurrence annotation into a spec.**
- **Do not create a `QP2505` spec.** May does not exist, in either year.
- **Do not "fix" a 2025 answer onto current law.** It answers the sitting.
- **Do not build the autonomous production agent yet** — still a §16 stop condition.
