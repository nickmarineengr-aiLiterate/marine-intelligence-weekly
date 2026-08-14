# INTERNAL PRODUCTION VOCABULARY — REMEDIATION PLAN

**Status:** measured and scoped, **not executed**. Produced at the QP2304 laptop review,
2026-08-14, under Part 36 of that session's brief, which directed that the debt be *planned*
rather than mass-fixed mid-review.

**Owning rule:** `PASTPAPER_PRODUCTION_PROTOCOL.md` §7 — the candidate-facing boundary.

---

## 1. THE MEASUREMENT, AND WHY IT DISAGREES WITH THE PREVIOUS ONE

The QP2312 session recorded **59 occurrences across 15 of 29 paid pages**. This review measures
**311 occurrences across 20 of 30 paid pages**. Both numbers are right; they measure different
things.

| | QP2312 session | This review |
|---|---|---|
| Measured against | a narrower term list | a wider term list (12 classes) |
| Measured on | the spec | **the built `solvedQP/*.html`, tags stripped** |

**Measuring the rendered page is the correct method** and should be the standing one. A spec-level
scan over-reports badly: a naive spec scan of the same term list returns 3,270 hits, of which
**2,508 are `retrieval_cards[].id` values** (`QP2304-Q1-C1`) that are never rendered as text. A
spec scan also cannot see the `if not publish` guard that already strips production metadata from
delivery builds.

**Detection is fully deterministic.** Every class below is a fixed regex over the tag-stripped
delivery HTML. No judgement is needed to *find* an occurrence; judgement is needed only to decide
the replacement wording. This should become a toolchain stage rather than a session activity.

---

## 2. THE CLASSES, RANKED BY HOW INDEFENSIBLE THEY ARE

| Class | Count | Verdict | Example as a customer sees it |
|---|---|---|---|
| `production-protocol` | 28 | **Indefensible** | *"Declared as engineering judgement under `PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1"* — a repository filename, on a paid page |
| `founder` | 3 | **Indefensible** | *"Founder policy and a recorded trap: …"* |
| `anchor-doc` | 7 | **Indefensible** | *"`known_traps.md` Entry 12 records …"* |
| `donor` | 32 | **Internal vocabulary** | *"The donor's evidence discipline is carried with its content"* |
| `qp-xref-visible` | 32 | **Mixed — see §3** | *"carried from the MIW built set, `QP2511-Q2`"* |
| `MIW-record` | 23 | **Mixed — see §3** | *"established from the Gazette reading in MIW record `QP2607/Q7`"* |
| `corpus` | 175 | **Largely legitimate — see §3** | *"The MIW corpus holds no HNS material of any kind"* |
| `review-jargon` | 11 | Case by case | *"A reviewer should treat …"* |

**Total 311 across 20 of 30 pages.**

### Distribution

Concentrated, not uniform — which makes a targeted fix viable:

```
QP2408 59 · QP2504 36 · QP2502 27 · QP2406 24 · QP2501 23 · QP2402 21 · QP2409 21 · QP2507 21
QP2503 17 · QP2312 13 · QP2407 13 · QP2411 13 · QP2511 5 · QP2401 4 · QP2508 4 · QP2410 3
QP2509 2 · QP2510 2 · QP2512 2 · QP2403 1
```

Ten pages carry **262 of the 311** (84%). Ten pages carry none at all.

---

## 3. THE FALSE POSITIVES, WHICH ARE MOST OF THE VOLUME

**`corpus` (175) is mostly not a defect.** Sentences like *"The MIW corpus holds no HNS material of
any kind"* appear in an *"Uncertainty and currency"* block that exists precisely to tell a paying
candidate how strong the evidence behind an answer is. That is a **product feature**, and removing
it would make the answers look more authoritative than they are — which the protocol's own
evidence-declaration discipline forbids. What needs changing is the **noun**, not the disclosure:
"the MIW corpus" is an internal system name. *"our verified source library"*, or simply *"no
primary text of the HNS Convention was available for this answer"*, says the same thing without
naming an internal store.

**`qp-xref-visible` (32) splits two ways.** A visible cross-link to another paper the customer owns
(*"Also on the platform: QP2411 Q4"*) is a navigation feature and should stay. A *citation* to an
internal record (*"carried from the MIW built set, QP2511-Q2"*) is provenance vocabulary and should
be reworded to describe the evidence, not the filing system.

**`MIW-record` (23) is the same split**, and mostly falls on the citation side.

**Estimated true defect count after triage: roughly 100–120**, concentrated in the four
indefensible classes (70) plus the citation half of the mixed classes.

---

## 4. RECOMMENDATION — ONE DEDICATED SESSION, NOT OPPORTUNISTIC CORRECTION

**Do it as a single dedicated cleanup package.** Three reasons:

1. **It is a wording problem with one vocabulary.** The same eight phrases recur across twenty
   pages. Fixing them together produces one consistent replacement vocabulary; fixing them paper by
   paper produces twenty slightly different ones, which is how the inconsistency arose.
2. **Opportunistic correction has already been tried and has not converged.** The debt was recorded
   at the QP2312 review and is larger now, because each new paper adds its own provenance prose in
   the same house style. The style is the defect; papers will keep inheriting it until the style
   changes.
3. **It touches live paid pages.** Twenty customer-visible pages is a change that deserves its own
   review and its own gate, not a subordinate clause inside a paper review.

**Sequence for that session:**

1. Promote the detector to `tools/pastpapers/` as a check stage over the **delivery** HTML, with the
   four indefensible classes failing the build and the mixed classes reporting.
2. Agree the replacement vocabulary once, in writing, before editing anything.
3. Fix at the **spec** level — never the generated HTML — and rebuild.
4. Re-run determinism and the delivery gate; the page count that changes should equal 20.

**Estimated burden:** roughly 100–120 edits across 20 specs, all wording, no restructuring, no
re-verification of any regulatory claim. One focused session.

**Do not** wire the four indefensible classes into the failing gate until the existing 70 are
cleared, or every subsequent paper build fails on inherited debt.

---

## 5. QP2304 SPECIFICALLY

QP2304 was checked as part of its own review. It carries the **same house-style provenance prose as
its siblings** — `corpus` and `MIW-record` mentions inside "Uncertainty and currency" blocks — and
**none of the four indefensible classes**: no protocol filename, no `Founder`, no `known_traps`, no
branch name. It neither improves nor worsens the debt, and it is not a reason to hold the paper.
