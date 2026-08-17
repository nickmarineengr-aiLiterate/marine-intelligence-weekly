# Limb model — what may key a recurrence

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

Limb-level recurrence is canonical: one 6-mark limb may repeat exactly while the
surrounding 16-mark question changes completely. `QP2608-Q8` is exactly that case.

That makes the *identity* of a limb load-bearing — and the corpus contains two
different things that both look like limbs.

---

## 1. The problem, measured

Sweeping `answer_route.steps[].limb` across all 40 specs (2,587 route steps,
88 distinct values):

| Shape | Steps | Example values |
|---|---|---|
| `null` — whole question | 1,001 | |
| alphanumeric limb label | 1,451 | `(a)` `a)` `a` `A.` `(b)(i)` `(iii)` |
| **non-alphanumeric token** | **135** | `framing` `main` `intro` `closing` `all` `head 1` `d1`…`d5` `report` `cause` `permanent` `temporary` `judgement` `comparison` |

Those 135 are **authoring scaffolds** — MIW constructs describing how the *answer*
is laid out. The source paper prints no such divisions. They must never key a
historical recurrence.

A second trap sits underneath. Only **73** route steps carry a limb that matches a
printed subpart label *exactly*, because specs write `(a)` while routes often write
`a)` or `a`. Naïve string matching would reject ~1,378 genuine limbs as unmatched.
**Labels must be normalised before comparison** — strip parentheses, dots and
whitespace, lowercase — or the model will conclude that almost nothing is a real
limb.

---

## 2. The four kinds

Every occurrence record carries `limb_kind`.

| `limb_kind` | Meaning | May key a recurrence? |
|---|---|---|
| `SOURCE_LIMB_CONFIRMED` | normalises to a printed subpart label in the paper's spec | **yes** |
| `SOURCE_LIMB_ASSERTED` | the paper prints limbs but the spec's `subparts` carries no labels; the limb is read off the printed stem | yes, flagged |
| `ANALYTICAL_SEGMENT` | a sentence or clause MIW isolated for comparison; the paper prints no such division | yes, and **must be disclosed as MIW's own division** |
| `AUTHORING_SCAFFOLD` | `framing`, `intro`, `main`, `closing`, `head N`, `dN`, … | **never** |
| `WHOLE_QUESTION` | no limb; the question is the unit | yes |

`ANALYTICAL_SEGMENT` is the honest name for what Phase 1 was doing when it wrote
`limb_label: "limb-1"` on `QP2608-Q2` and `"second sentence"` on `QP2512-Q4`. Those
papers print a single undivided question. The division is MIW's, it is legitimate
for comparison, and it may not be presented to a candidate as *“limb 1 repeated”* —
because there is no limb 1.

---

## 3. Enforcement

`tools/validate_families.py`:

- **C2** — `limb_kind` must come from the enum
- **C4** — a scaffold-shaped label (`framing`, `head N`, `dN`, …) not marked
  `AUTHORING_SCAFFOLD` fails
- **C5** — no occurrence may be keyed on an `AUTHORING_SCAFFOLD` at all
- **C7** — a `SOURCE_LIMB_CONFIRMED` limb must match a printed subpart label
- **C8** — marks must equal the spec's printed marks; a limb may not assert marks
  where the spec prints none

Mutation-tested: *"use an authoring scaffold as a source limb"*, *"key an occurrence
on a scaffold"*, *"invent a limb the paper does not print"* and *"invent marks for a
limb"* each make a named check fail.

---

## 4. Deliberately out of scope

The Laptop's audit found **393 of 689** limb dividers carry marks and **296** are
label-only, of which **189** are source or spec subparts whose marks are `null` and
**107** are authoring scaffolds.

QI-v2 does **not** repair any of that. It only has to be unable to be *misled* by
it. Concretely:

- known marks are respected
- missing marks are **never inferred** — `marks_if_known` stays `null` and the
  Paper DNA reports `UNAVAILABLE` with a reason
- scaffolds are never treated as exam limbs

Recovering the 189 null-mark subparts, and cleaning the 107 scaffolds out of the
route data, remain separate pieces of work.
