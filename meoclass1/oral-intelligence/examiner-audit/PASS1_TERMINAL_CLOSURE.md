# PASS 1 TERMINAL CLOSURE — 7 September 2026

**Record id:** `P1TERM-20260907`
**Baseline:** `ac61228` · **Predecessor:** `P1GUARD-20260906`
**Product bytes changed: ZERO.**

## The chain

```
CORR-T5-DDCASCADE / -REACH / -HYDRANT      the original Pass 1
  └─> CORR-P1REPAIR-20260906               its two P0 escapes
        └─> CORR-P1CLOSE-20260906          the repair's three P1 escapes
              └─> P1GUARD-20260906         the guard weaknesses that survived all three
                    └─> P1TERM-20260907    E1-E4 + generated-surface provenance
```

Nothing earlier is rewritten. `P1GUARD-20260906` recorded four escapes as OPEN and
declined to claim closure over them; this record closes exactly those four and the
generated-surface question they exposed, and nothing else.

## What was closed

| id | The escape | How it is closed |
|---|---|---|
| **E1** | A denial clause silenced a live claim coordinated with it: *"BMP5 replaced BMP4 **and** remains the current industry standard"*. | Two parts, and the second is the one that mattered. **Bounded clause segmentation**: a coordinator splits only where it joins two CLAUSES — the left side already carries a finite verb, and the right side OPENS with one, because a coordinated predicate shares its subject. And **subject inheritance**: the live clause never names BMP5, so splitting alone left nothing to match. A clause with an inherited subject is judged only on an explicit currency assertion — narrower than the default-suspicious rule, because an inherited subject is an inference. |
| **E2** | `BMP-5` was invisible, and `normalise` folds every unicode dash toward that unmatched ASCII form — normalisation and matcher pulled opposite ways. | One publication, three ordinary spellings: `BMP5`, `BMP 5`, `BMP-5`. Detection only; no card's spelling is rewritten. |
| **E3** | A governing figure with no modal — `Hydrant pressure - 0.27 N/mm²` — was undetectable at any unit. | Two ways a modal-free figure reads as governing: **label:value**, where the label IS the assertion and the segment ends at the figure; and a **numbers context** (key numbers, figures to memorise, regulatory values, benchmarks, criteria). Neither fires on prose, so a machinery description that mentions a pump discharge is still left alone. |
| **E4** | The subject in a preceding sibling block — `<h4>Fire main</h4><li>Minimum 0.27 MPa</li>` — defeated the detector. | A structural label reaches the block beneath it, bounded by **element identity** and by a segment count. Not a character window: the ±220-character window is the defect this replaces. |
| **generated surfaces** | `topics.html` carried four BMP5 mentions the gate never examined, because the whole surface was skipped. | The surface is now swept, and status is decided **item by item from provenance**. |

## Generated-surface policy

A generated page gets **no blanket exemption**. Its status is inherited from the
provenance of each item:

- a **question-stem echo** — a row that is entirely the text of a link into a question
  card — is the examiner's wording and takes the historical policy, exactly as it does
  on the card it quotes;
- a **label or description the generator authors itself** is teaching, and takes the
  currentness policy like any other teaching text;
- **navigation** inherits the semantics of what it points at.

The distinction is structural, so it cannot be satisfied by adding a class to a
template: a stem echo is recognised by the `href` that names the card it quotes. One
test asserts both directions on the same page, same class, same element — opposite
verdicts decided by provenance alone.

### The four `topics.html` mentions, adjudicated

All four are **A / C — HISTORICAL EXAMINER WORDING, echoed as navigation — KEEP**.
Each traces to a `q-text` question stem in a question-bank card, and each is emitted by
`tools/study/build_topic_pages.py` as `<li><a href="QBx.html#qN">` inside
`<ul class="q-list">`:

| row | owning stem |
|---|---|
| "What are the Best Management Practices (BMP5) for piracy prevention…" | `QB4_B.html#q16` |
| "Describe the key content and operational phases of BMP5…" | `QB4_H.html#q11` |
| "…BMP5 measures." | `QB9_A.html#q9` |
| "War risk / vessel hardening / BMP5 — provide detailed…" | `QB9_B.html#q5` |

No source correction is required and no generated HTML was hand-edited. The earlier
report's guess that two of the four were generator-authored topic labels was **wrong**:
both are sentences of an examiner's stem, and the second is the whole stem.

## Two defects found while closing, worth as much as the closure

**A committed regex had two dead alternatives.** `oral_currentness.py` carried a literal
`0x08` byte where `\b` was intended, in `PROVENANCE_HINT` (`questions on\b`) and
`CURRENTNESS_MARK` (`replaced\b`) — written that way at `a2c83bd` by a shell heredoc that
ate the backslash. Both alternatives could never match. Both fail **closed** (a lost
excuse makes the detector more suspicious, not less), so no defect escaped through them,
but a named alternative that cannot fire is a check that is not there. Repaired, and a
scan now catches the byte class.

**A control passed for the wrong reason.** `E4_label_does_not_leak_across_containers`
used an unrelated heading ("Lifeboat davits"), which is refused by the *subject* test
whether or not the container bound exists — so the bound was never actually proven. The
mutation that removed the bound exposed it. The check now uses the same "Fire main"
label and the same governed figure separated only by a **closed** container, and the
container bound is compared by **element identity**: two sibling `<div>`s both spell
"div", so a tag-name comparison let a label leak across a boundary it was supposed to
stop at.

## Vacuous-check audit (new controls only)

Each new control names a reachable failing state and one mutation reaches it:

| control | mutation that kills it |
|---|---|
| `E1_coordinator_splits_clauses_not_noun_lists` | `E1-E` |
| `E1_MUST_CATCH_denial_then_live_claim` | `E1-D` |
| `E2_hyphenated_name_is_the_same_publication` | `E2-D` |
| `E3_MUST_CATCH_modal_free_governing_figure` | `E3-D` |
| `E4_label_does_not_leak_across_containers` | `E4-D` |
| `generated_surface_status_follows_item_provenance` | `G-D` |

`E1-E` is **three edits in one mutation**, and that is a finding in itself. The noun-list
rule turned out to be defended three times over — the left side must contain a finite
verb, the right side must open with one, and a verbless fragment merges forward instead
of standing as a proposition. Removing any one, or any two, changed nothing the control
could see. The redundancy is good design and bad for a mutation suite: crediting a kill
to an edit that left the property standing is exactly the false credit these suites
exist to refuse.

## Evidence

- **Controls:** `tools/oral/test_currentness_detectors.py` — 22 checks, 0 FAIL, over 60+
  adversarial cases including the 6 E1 sentences, the 3 E2 spellings, 3 E3 MUST-CATCH
  and 4 MUST-NOT-CATCH, and both E4 directions.
- **Mutations:** `tools/oral/mutate_correction_p1guard.py` — **30 of 30 behaved as
  required, 0 escapes, 0 crashes**, serial, byte-exact restore. 26 must-catch (product
  and detector) and 4 must-NOT-catch: past-paper wording, a wholly historical
  coordinated sentence, an unrelated heading, and a generated stem echo.
- **Gates:** p1repair 50, struct 23, reach 42, hydrant 35, scope 10, detectors 22 —
  0 FAIL.
- **Live corpus, recursive, 224 files:** fire-main incomplete-scope claims **0**;
  BMP5-as-current **0**, generated surfaces now included.

## Residual P2/P3 release-hardening debt

Declared, not hidden, and outside the closure contract:

- **P3** — CSS- or JavaScript-generated text, malformed markup beyond the parser's
  recovery, OCR-style corruption, and claims carried only in HTML attribute text.
- **P3** — units outside the eleven in the conversion table, and unit spellings no
  maritime author uses.
- **P3** — `oral_lib.all_anchors()` enumerates top level only. Used by the
  examiner-index and matcher validators, by no closure gate, and its subject (q-card
  anchors) exists only on top-level pages.
- **P2** — clause segmentation is bounded, not a parser. A subject carried across a
  full sentence boundary, or through a construction outside the coordinator set, is not
  inherited. No live instance; a defect of this shape would have to be written
  deliberately.
- **KEEP, adjudicated** — `QB4_B.html:1931` lists BMP5 among the publications the bank
  was compiled from. A compilation provenance statement is a historical fact about the
  sources read, not a claim of current authority.

## Closure standard applied

Pass 1 closes when no LIVE P0/P1 content defect remains and no realistic E1–E4-class
guard escape remains. A verifier's sixth, seventh or eighth theoretical parsing edge
case outside the declared contract is release-hardening debt, recorded above — not a
reason to keep Pass 1 open.
