# Build prompt — MIW Past Paper EM2601 (January 2026)

> **How to use:** Paste this whole document as your first message to Claude Opus, in a session with
> Desktop Commander MCP (local clone at `F:\marine-intelligence-weekly`) and GitHub MCP connected —
> e.g. Claude Desktop. This session (web chat, no Desktop Commander) planned the architecture but
> cannot execute the local-filesystem/git steps below.

---

## 0. Environment check — do this first

1. `tool_search` for "desktop commander" and "github" to confirm both connect.
2. If Desktop Commander is available: `get_file_info` on `F:\marine-intelligence-weekly` to confirm repo
   access, then `git status` / `git log -1` to confirm the local clone is clean and in sync with
   `origin/main`.
3. If either tool is missing, stop and tell Nixon rather than improvising a workaround.
4. Read `tools/notes/miw_paths.py` if present (single source of truth for manifest paths) before
   touching any manifest.

---

## 1. Context — what you're building

You are producing the **first file** in a new MIW content series: complete model answers to an entire
official MEO Class 1 (Engineering Management) written exam paper — every question, exam-length,
marks-calibrated — as opposed to the existing QB (oral cards) or WA (single-topic deep-dive chapters)
series. This is paper **EM-2601, January 2026**, Sr. No. `EM-2601`, Total Marks 100, answer 6 of 9,
time allowed 3 hours.

Full architecture, rationale, and open questions are in
`miw-pastpapers-production_SKILL_DRAFT.md` (attached/uploaded to this session — read it in full before
starting). If it isn't present in this session, ask Nixon for it rather than guessing the schema. Key
points from it, restated here so you don't have to re-derive them:

- **New folder:** `meoclass1/pastpapers/`. **New file:** `meoclass1/pastpapers/EM2601.html`, all 9
  questions in one file, anchored `#q1`…`#q9`.
- **New manifest:** `meoclass1/pastpapers/pastpapers_content_index.json` — do not touch
  `qb_content_index.json`, `notes_content_index.json`, or `written_content_index.json`.
- **Dedup-first**: before drafting any question, check whether it's already answered elsewhere on the
  platform (WA chapter, QB card, or an earlier-built pastpapers file) and reuse/condense rather than
  redrafting from scratch. See the skill draft Section 3 for the A/B/C/D tiering.
- **Two-block answer format per question**: a Model Written Answer (exam-realistic length, see length
  table below) followed by a Study Notes companion box (why it works, common mistakes/examiner traps,
  CE Oral Tip, regs) — kept visually distinct.
- **Verification standard**: identical to the WA series (`miw-written-qa-production_SKILL.md` Section
  5) — verify every regulation/resolution number and consequential figure against a primary source,
  state the current legal stage explicitly for anything not fully in force, cross-check consequential
  numbers against 2+ sources, drop anything unverifiable rather than presenting it as fact.
- **Design system**: identical CSS tokens/typography to the rest of the platform — copy the `<style>`
  block from an existing WA file (e.g. `WA2-GHG1.html`) as baseline rather than reconstructing it.
- **Gating**: build ungated first (`<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->`), present to Nixon,
  gate only after his approval, using the canonical script:
  `<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>`

**Length calibration ([Speculative] — flag to Nixon if a question's real weight seems mismatched):**

| Marks | Target length |
|---|---|
| 4 | 60–90 words |
| 5 | 80–110 words |
| 6 | 90–130 words |
| 8 | 150–200 words |
| 10 | 180–240 words |
| 16 (or unmarked — treat as full-weight) | 320–420 words |

---

## 2. Source — the full January 2026 paper (verbatim from the official exam)

**EXAMINATION OF MARINE ENGINEER OFFICER — Function: Marine Engineering Management at Management
Level — ENGINEERING MANAGEMENT — M.E.O CLASS I — Time Allowed: 3 hours — (India 2026) — Sr. No.
EM-2601 — Total Marks: 100**

NB: Answer SIX questions only. All questions carry equal marks. Neatness and clarity carry weightage.

**Q1.** Reducing the speed of main propulsion engines is considered to be the simplest and most
practical short-term solution for lowering GHG emissions from ships. What are the drawbacks and dangers
of operating main propulsion two-stroke marine engines at low speeds for extended periods of time? How
can these issues be resolved and the risks associated with low-speed operation reduced?
*Recurrence: 2026/JAN/Q1 (new/rare)*

**Q2.** Define communication. Enumerate and discuss the different types of communications. Discuss the
various barriers to effective communication. You are carrying out a Main Engine decarbonisation and the
work is carried out in two groups, one working on the cylinder head platform and the other group
working in the bottom platform. Identify the areas in this operation where there can be a hazard due to
failure of communication. Also suggest risk mitigation measures to mitigate the hazard of failure of
communication.
*Recurrence: highly recurring — 2018/APR, 2018/JULY, 2018/SR09, 2018/DEC, 2019/FEB, 2019/APR, 2019/JUN,
2019/JULY, 2019/OCT, 2020/MAR/Q5, 2022/JAN/Q5, 2025/SEP/Q6, 2026/JAN/Q2*

**Q3.** What are the principles of modern salvage law? (4) What is General Average? (4) Explain with
context to General Average: (8) i. Entitlement ii. Artificial iii. Adjustment iv. Contestation
*Recurrence: highly recurring — 2012/MAR, 2016/APR, 2017/FEB, 2017/DEC, 2018/APR, 2018/JULY, 2019/JUN,
2019/SEP, 2019/NOV, 2021/FEB/Q6, 2021/JUL/Q9, 2022/FEB/Q4, 2024/JUN/Q8, 2026/JAN/Q3*

**Q4.** A VLCC suffered hull damage following a tank explosion and sank after a few days while
undergoing salvage operations in the territorial sea of a coastal state. Discuss ship-owner's
protections with reference to (a) marine insurance and (b) liabilities under international conventions.
*Recurrence: 2026/JAN/Q4 (new)*

**Q5.** Corrosion is considered to pose a considerable danger to ships' hulls, cargo and ballast tanks;
discuss the following: i. Influence of temperature on the corrosion rate of cargo and water ballast
tanks. ii. Causes of coating deterioration in cargo and ballast tanks. iii. Describe how an assessment
of the coating condition helps to be aware of the tank corrosion status. iv. State the information
obtained from the Coating Technical File.
*Recurrence: 2026/JAN/Q5 (new)*

**Q6.** Control of disease vectors is necessary for maintenance of health on board ships. What is the
role of the WHO organisation in this regard, and which are the national agencies tasked with the
maintenance of the ship and the crew in good health? What are the different certificates issued to a
vessel for maintenance of the ship in good health? Who can issue these certificates in India, and what
is the validity and extension options for such certificates?
*Recurrence: 2025/NOV/Q3, 2025/DEC/Q1, 2026/JAN/Q6*

**Q7.** State the UNCLOS requirements for member States: (a) to register ships flagged with them, and
(b) to control safety, pollution and social aspects of ships. (c) What mechanism is used in India to
comply with these requirements enumerated at (a) and (b) above?
*Recurrence: highly recurring — 2017/FEB, 2017/DEC, 2018/APR, 2018/JUL, 2019/JUN, 2019/SEP, 2019/NOV,
2020/JAN, 2022/MAR/1, 2026/JAN/Q7*

**Q8.** a) State the applicable regulation of SOLAS and MARPOL under which it is mandatory for a flag
state to conduct an investigation into any casualty. b) Briefly write the salient points of the
casualty investigation code and the recommended practices for a safety investigation into a marine
casualty or marine incident. c) What do you understand by the term "very serious marine casualty"? (16)
*Recurrence: highly recurring — 2013/FEB, 2014/SEP, 2014/DEC, 2015/JUN, 2016/JUL, 2016/DEC, 2017/JAN,
2017/MAR, 2018/DEC, 2023/JAN/Q7, 2024/AUG/Q3, 2025/JUN/Q7, 2026/JAN/Q8*

**Q9.** A) How is the Human Element issue addressed in the STCW Code? (8) B) Discuss the IMO guidance on
fatigue mitigation and management on board ships. (8)
*Recurrence: 2025/AUG/Q4, 2026/JAN/Q9*

---

## 3. What to do, in order

1. Run the Section 0 environment check.
2. For each of the 9 questions, run the dedup check: search `written_content_index.json` and
   `qb_content_index.json` (and, if it exists yet, `pastpapers_content_index.json`) for topical overlap.
   Tag each question A/B/C/D per the skill draft's Section 3 before drafting.
3. Draft each question's Model Written Answer + Study Notes block. Web-search and verify every
   regulation/figure per Section 1's verification standard above — flag anything you can't verify rather
   than inventing it. Several of these (Q1 GHG/low-speed operation, Q4 VLCC liabilities, Q7 UNCLOS/India
   mechanism) intersect with the Merchant Shipping Act 2025/DGMA transition already tracked in project
   memory — check current status, don't assume the pre-2025 MSA framework still applies where India-
   specific mechanisms are asked.
4. Build `meoclass1/pastpapers/EM2601.html` per the Section 7 page structure in the skill draft — gate
   stripped, review-copy comment in its place.
5. Run an HTML tag-balance check (Python `HTMLParser` stack check) before presenting anything.
6. Present the full ungated file to Nixon for review. **Stop here and wait for his approval** — do not
   gate, index, commit, or push until he signs off.
7. On approval: gate the file, create/update `pastpapers_content_index.json` (mark all 9 questions
   Built, with `reuse_tier`/`cross_ref` set), build/update `meoclass1/pastpapers/index.html`, and add a
   card to the MEO Class 1 hub page (verify its actual filename in the repo first — don't guess).
8. Commit with files staged explicitly by name (not `git add .`), push to `origin/main`.
9. Cache-busted live verification via `raw.githubusercontent.com`, and report back: files touched,
   commit hash, live-verification confirmation, and which questions were Tier A/B/C/D and why.

---

## 4. Guardrails

- Do not invent regulation numbers, resolution numbers, or figures. If something can't be verified,
  say so explicitly in the paper's verify-box and omit the specific number.
- Do not touch `qb_content_index.json`, `notes_content_index.json`, or `written_content_index.json`.
- Do not reproduce the source aggregator's marketing copy or watermark text anywhere in the output.
- Do not gate or push without Nixon's explicit review approval of the ungated copy first.
