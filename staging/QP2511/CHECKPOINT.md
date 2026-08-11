# QP2511 — PRODUCTION CHECKPOINT

**Paper:** QP2511, November 2025, serial `EM – 2511`.
**Branch:** `pastpapers/qp2511-founder-review`, branched from `commerce/solvedqp-recovery` @ `462cfbc`.
**Stopped:** 2026-08-11.
**State: 1 of 9 authored. THE PAPER IS NOT COMPLETE AND MUST NOT BE BUILT.**

---

## 1. THE RULE THIS CHECKPOINT EXISTS TO OBEY

`PASTPAPER_PRODUCTION_PROTOCOL.md` §3: *there is no valid half-authored-paper state.*
`PASTPAPER_PRODUCTION_PROTOCOL.md` §4: *build only when the paper is complete.*

Accordingly:

- **`specs/QP2511.json` is UNTOUCHED.** It remains answerless intake, `build_state: "Intake
  Complete"`, `answer_status: "Not Built"` on all nine questions. The corpus therefore still reads
  **252 / 108 / 144, 12 solved papers** — QP2511 has not entered the solved set.
- The one authored question is **staged**, not promoted: `staging/QP2511/Q9.json`.
- **No build was run. No `solvedQP/` regeneration was run.** The delivery product is unchanged at
  12 papers.

Promoting a single question into the spec would have created exactly the misleading artefact the
protocol forbids: a paper that renders, indexes and counts as solved while eight of its nine
answers do not exist.

---

## 2. WHAT IS DONE AND DURABLE

| Work | State | Where |
|---|---|---|
| Source verification, 2 of 2 pages read back visually | **COMPLETE** | §3 below |
| November 2025 temporal anchor | **COMPLETE** | `docs/QP2511_TEMPORAL_AND_DONOR_ANCHOR.md` |
| Reverse-hint adjudication (3 rows) | **COMPLETE** | anchor §4 |
| Donor map recomputed from derived state | **COMPLETE** | anchor §5 |
| Donor-material sweep against the Nov-2025 line | **COMPLETE** | anchor §6, §7 |
| **Q9 authored + verified** | **COMPLETE (staged)** | `staging/QP2511/Q9.json`, `verification/QP2511/Q9.md` |
| Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 | **NOT STARTED** | — |

**The research foundation is the bulk of the durable value here.** Q7's FAL research is complete to
primary level even though Q7 is unauthored (see §5).

---

## 3. SOURCE TRUTH — VERIFIED, NO CORRECTION NEEDED

Text layer extracted and **both pages read back against a 150 dpi render**, closing the residual
risk the intake spec itself recorded (*"Pages read back this session: 1 of 2"*).

Confirmed as printed: serial `EM – 2511`; November 2025; `(India 2025)`; Total Marks 100 with six
questions required at equal marks (the 96-against-100 anomaly is printed, and is reproduced not
corrected); marks printed **only** on Q7, Q8 and Q9 as `(16)`.

All three printed anomalies confirmed and correctly preserved in the intake spec:

- **Q2(d)** — sentence break: *"take. If your vessel is torque rich."*
- **Q3** — missing word: *"What is the Role the WHO organisation"*
- **Q6** — missing verb: *"during which you a surface crack"*

**No correction to source truth was required.**

---

## 4. THE DONOR MAP AS ADJUDICATED — 6/9 TIER D

Reverse-hint adjudication accepted three new edges, moving the paper from **3/9 to 6/9 Tier D**.

| Q | Tier | Donor | Direction | Status |
|---|---|---|---|---|
| Q1 | C | — | — | fresh research required |
| Q2 | C | — | — | fresh research required; §2.1 technical-source policy applies |
| Q3 | **D (new)** | `QP2601-Q6` | **backwards** | NEAR, accepted |
| Q4 | **D (new)** | `QP2603-Q5` | **backwards** | EXACT, accepted |
| Q5 | D | `QP2603-Q6` | **backwards** | EXACT |
| Q6 | **D (new)** | `QP2603-Q7` | **backwards** | EXACT, accepted |
| Q7 | C | — | — | **research COMPLETE, authoring not started** |
| Q8 | D | `QP2603-Q9` | **backwards** | EXACT |
| Q9 | D | `QP2508-Q7` | **forward** | **AUTHORED** |

**Five of six donors are pulled backwards from 2026.** Currency corrections made for a later
sitting must be **reversed, not inherited**, on every one of them.

---

## 5. RESEARCH BANKED FOR UNAUTHORED QUESTIONS

### Q7 — FAL Convention. Research is COMPLETE to primary level.

The position at November 2025, established this session:

| | Status at the sitting |
|---|---|
| `FAL.14(46)`, 2022 amendments | **IN FORCE 1 Jan 2024** — mandatory Maritime Single Window, Standard 1.3quin (already primary in corpus via `QP2403-Q1`) |
| `FAL.15(47)`, adopted 17 Mar 2023 | **IN FORCE 1 Jan 2025** — amends **RP 7.11**, national facilitation programmes, *"taking into account the need to combat illicit activities"*. **Read in full this session** |
| FAL 49 (10–14 Mar 2025) | **APPROVED ONLY** — RP 6.24 vaccinations/medical care; revised MSW Guidelines `FAL.5/Circ.42/Rev.4`; new IMO Compendium |
| `FAL.18(49)` | **ADOPTED** — mooring personnel guidelines. A *guidelines* resolution, **not** an annex amendment |
| `FAL.17(48)` | **ADOPTED** Apr 2024 — wildlife smuggling guidelines. Likewise not an annex amendment |
| FAL 50 (23–27 Mar 2026) | **AFTER THE SITTING — EXCLUDE** |
| IMO Strategy on Maritime Digitalization | work plan only; adoption expected at the **35th** Assembly by end-2027 |

**There is no FAL annex amendment adopted-and-pending at this sitting.** The "recent amendments"
limb is therefore answered on FAL.14(46) and FAL.15(47), and the *sustainability/digitalization*
limb on the single window, the Compendium datasets and just-in-time port calls.

> **Correction recorded.** The IMO "Amendments to IMO instruments" summary page describes
> `FAL.15(47)` as *"mandatory garbage record books for smaller ships"* — that is a MARPOL Annex V
> item, not FAL. The **primary resolution text was read** and governs: FAL.15(47) amends
> **Recommended Practice 7.11**. Do not author from that summary page.

### Q8 — the Merchant Shipping Act boundary is the whole risk

At November 2025 the **Merchant Shipping Act 1958** governs. The 2025 Act was assented **18 August
2025** and commenced **15 March 2026** (`S.O. 1244(E)`). The donor `QP2603-Q9` (March 2026) reasons
about the 2025 Act as live law across at least three study-note blocks — **all of that must be
reversed.** The Indian recycling statute is the **Recycling of Ships Act, 2019**.

**`26 June 2030` in that donor is LEGITIMATE** — the HKC's own transitional deadline for existing
ships. Adjudicated as keep. Do not blind-strip it.

### Q5 — the Assembly boundary bites here

The donor `QP2603-Q6` (March 2026) may legitimately cite the **2025** HSSC Survey Guidelines. At
November 2025 the operative Assembly editions are the **33rd Assembly (6 December 2023)** ones. See
anchor §2.

---

## 6. RESUME INSTRUCTIONS

```bash
cd F:\Marine-Intelligence-Weekly
git -c safe.directory=* checkout pastpapers/qp2511-founder-review
python tools/pastpapers/run_toolchain.py          # must be ALL STAGES PASS before starting
```

Then, in order:

1. Read `docs/QP2511_TEMPORAL_AND_DONOR_ANCHOR.md` **first**. It is the fixed line for this paper.
2. Read this checkpoint.
3. Author **Q1–Q8**. Suggested order, cheapest-risk first:
   **Q4 → Q6** (EXACT donors, low temporal risk) → **Q5** (EXACT donor + Assembly regression) →
   **Q3** (NEAR donor, compress the stem) → **Q8** (EXACT donor + MS Act reversal) →
   **Q7** (fresh, research already banked) → **Q1**, **Q2** (fresh research).
4. Only when **all nine** are authored: promote every staged object into `specs/QP2511.json` in one
   operation, then build.

### The one trap that will bite the resuming session

**`staging/QP2511/Q9.json` is already correct and must not be re-derived.** In particular:

- its donor is **`QP2508-Q7`**, **not** the `QP2602-Q7` still recorded in the intake spec. When Q9
  is promoted, `reused_from` must be **overwritten**, not merged;
- its cross-links point at **QP2511 Q7 and Q8**, which are not yet authored. Those links will not
  resolve until Q7 and Q8 exist. **Do not "fix" them by pointing them back at QP2508.**

---

## 7. HONEST STATEMENT OF SCOPE

One solved question object in this corpus is ~37 KB of JSON across 38 keys, plus a verification
record. Nine of them is ~330 KB of primary-verified content, and three of this paper's questions
have no donor at all. **The session produced a complete research foundation and one finished
question; it did not produce a paper.**

This is consistent with the corpus's own history — `QP2404` stopped at 4/9 and `QP2403` at 2/9
before being finished in later sessions. Nothing here is blocked; the work is simply unfinished.
