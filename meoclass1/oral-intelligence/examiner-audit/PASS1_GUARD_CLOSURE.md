# PASS 1 GUARD CLOSURE — 6 September 2026

**Record id:** `P1GUARD-20260906`
**Baseline:** `8446a55` · **Governing:** `a2c83bd`
**Product bytes changed: ZERO.**

## Why this is not a correction manifest

The correction schema requires at least one card, one `PRIMARY_CORRECTION`, and a
pre/post digest pair. This record corrects no card, so it cannot honestly satisfy any
of them. Manufacturing a card to fit the schema would produce exactly the decorative
record that schema exists to forbid — the audit refusing a card-less correction is the
audit working. It is recorded here instead, and chained explicitly.

## The chain

```
CORR-T5-DDCASCADE / -REACH / -HYDRANT      the original Pass 1
  └─> CORR-P1REPAIR-20260906               its two P0 escapes
        └─> CORR-P1CLOSE-20260906          the repair's three P1 escapes
              └─> P1GUARD-20260906         the guard weaknesses that survived all three
```

Nothing earlier is rewritten. Four independent reviews found four defects, and the trail
of all four is the point: a record that tidied its predecessors would destroy the only
evidence of how a green gate stayed green while a defect was live.

## What was closed

Content was **independently measured clean before this pass** — twice, by two clean-context
verifiers using their own enumerations and their own regexes. The ruling was explicit that a
guard being hardened is not a reason to reopen content, and none was reopened. What this
closes is the reason nobody could yet be *sure*: a detector that recognises renderings cannot
prove the absence it asserts.

| Finding | What was wrong | How it is closed |
|---|---|---|
| **D2** | BMP5 currentness was a fixed `OPERATIVE` phrase list. It missed *"BMP5 is the current industry guidance"* — the plainest form of the proposition it was named for. | Inverted to **default-suspicious**. The question is no longer "does this match a phrasing I listed?" but "is this mention **excused**?" — historical, quoted, a stem, navigation, bibliography, or governed by a supersession statement in its own container. An unlisted phrasing now fails **closed**. |
| **D4** | A single `DENIAL` keyword anywhere in an element silenced **both** detectors, so *"BMP5 replaced BMP4, but BMP5 is what we use today"* passed. | Denial is **sentence- and clause-scoped**. Coordinating conjunctions end a proposition, so a historical first clause can no longer silence a live second one. |
| **D3** | The pressure matcher read raw HTML with closed vocabularies: entities, `&nbsp;`, split tags, `kg/cm²`, `psi`, `<dd>`, `<figcaption>` and attribute text were all outside it. Latent — no live instance. | Matching runs on **normalised visible text**. Renderings collapse before comparison; element coverage is by **exclusion** (the inline-tag set is closed, everything else is a block); pressure is compared as a **quantity in MPa** across eleven units. |
| **D5** | The container currentness exemption ignored subject, so a note about MSC.535(107) would have excused a BMP5 claim beside it. | The exemption requires the container to discuss **BMP5 and its successor** with a supersession verb. Asserted adversarially in the gate. |
| **D9** | Stem detection used a ±220-character window that could swallow live teaching text. | Replaced by **container identity** — a segment's classes, unioned over the whole segment. |
| **D7** | The "detection only" invariant asserted `"0.27 MPa" in QB2_F.html`, which was **equally true before** the correction it claimed to guard. | Replaced by a real invariant: the same claim gets the same verdict in MPa, N/mm², and bar; the detector is pure; and QB2_F keeps MPa while QB2_B keeps N/mm² — both passing the same guard. |
| **scope probe** | `test_corpus_scope.py` planted a file inside `meoclass1/` and removed it in a `finally:`, which does not run when a process is killed — and a killed gate has left product bytes in this repository before. | `corpus_files()` takes a root; the control proves recursion on a **synthetic tree** and asserts no probe exists in the product corpus. |

## Why the lists could never converge

Five rounds, one defect class, each round enumerating one more list and each next reviewer
finding that list's edge:

| round | the guard recognised | what defeated it |
|---|---|---|
| 1 | the string `"4.0 bar"` | **case** |
| 2 | `"0.27 N/mm"`, in `<li>`/`<p>` | **unit and element type** |
| 3 | `<span class="reg-code">` | **HTML class name** |
| 4 | a figure adjacent to its unit | **number formatting** (`0.27-0.35 MPa`) |
| 5 | 14 operative phrasings | **wording** |

An enumeration of renderings is an open set; the reviewer always has one more. The remedy
is to make the *rendering* stop mattering — normalise it away, invert the default so an
unlisted form fails closed, and compare quantities rather than strings. The lists that
remain (inline tags, unit conversions, excused container classes) are closed sets by nature.

## Three bugs found building it, worth as much as the fix

- **A stack sampled at flush time loses every inline ancestor.** An inline end tag pops
  before the flush, so `<span class="q-version">` emitted its text with an empty stack and
  the provenance skip could never see it.
- **Classes must be unioned over the whole segment.** An inline `<a class="toc-link">`
  opened mid-run is still the container of the words it wraps; a stack sampled once at the
  start made every navigation and index row look like teaching.
- **An em-dash aside is not a proposition boundary.** Splitting there severed *"Before 2025
  the guidance was region-locked"* from the clause it governs, and reported the corpus's own
  supersession card as a defect.

## Evidence

- **60 adversarial cases**, `tools/oral/test_currentness_detectors.py`: 30 pressure
  MUST-CATCH across every rendering listed above, 7 MUST-NOT-CATCH (HydroPen operating
  pressure, the weathertightness hose test, unrelated control air, a version stamp quoting
  the removed figure, a complete two-limb claim), 12 BMP5 MUST-CATCH including the bare
  `<td>` code cell and the `<h4>` heading, 11 MUST-NOT-CATCH. **All pass.**
- **Live corpus:** 0 fire-main incomplete-scope claims, 0 surfaces teaching BMP5 as current.
- **Gates:** p1repair 44, struct 23, reach 42, hydrant 35, scope 10, detectors 12 — 0 FAIL.
- **Manifest audit:** 1422/1422.

## Residual limits, stated not hidden

This is not a natural-language parser, and the agreed closure standard does not ask for one.
A claim expressed with no modal word and no recognisable unit, or spread across two sibling
blocks with neither carrying a governed figure, remains outside detection. That is **P3 debt**.
Also deferred: `oral_lib.all_anchors()` enumerates top level only — used by the examiner-index
and matcher validators, by no Pass-1 closure gate, and its subject (q-card anchors) exists only
on top-level pages.

`QB4_B.html:1931` lists BMP5 among the publications the bank was compiled from. Adjudicated
**KEEP**: a compilation provenance statement is a historical fact about the sources read, not a
claim that BMP5 is current authority. The detector excuses it as provenance, by construction.
