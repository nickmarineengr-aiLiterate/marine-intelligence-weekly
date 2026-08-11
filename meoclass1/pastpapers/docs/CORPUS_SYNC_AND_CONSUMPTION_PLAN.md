# MARPOL ANNEX VI CORPUS SYNC — DESTINATION, CONSUMPTION CONTRACT, PILOT

**Status: PREPARATION ONLY. No corpus file was imported, copied, moved or referenced.**
Written 2026-08-11, in the pre-corpus-sync freeze session.

This file prepares the **receiving** architecture. The reference contract itself is
[`MIW_TRUE_SOURCE_CONTRACT.md`](MIW_TRUE_SOURCE_CONTRACT.md) and is **not restated here** —
this document adds only what that contract could not know: where the files physically go,
what is measurably missing today, and how a pilot would be judged.

---

## 1. The two repositories, and which one is canonical

There are two `RulesApp` trees on this machine and they are **not** the same thing. Confusing
them is the most likely way to corrupt this sync.

| | Canonical corpus repository | MIW consumer snapshot |
|---|---|---|
| Path | `F:\RulesApp\repository\` | `F:\Marine-Intelligence-Weekly\RulesApp\repository\` |
| Git remote | `nickmarineengr-aiLiterate/RulesApp` (**private**) | inside `marine-intelligence-weekly` (**public**) |
| Role | **Master.** Where corpus work is authored and verified | **Read-only projection.** What MIW products resolve against |
| Tracked in MIW | — | yes, 24 files, all under `repository/index/` |

**The Written QP product must never author corpus content.** It consumes a projection. That is
the same one-source-many-consumers rule the True Source contract settled on 2026-08-08.

---

## 2. Measured drift — the actual gap, as at 2026-08-11

Both figures below were counted from the files on disk in this session, not carried forward
from any document.

| Measure | Canonical `F:\RulesApp` | MIW snapshot | Gap |
|---|---|---|---|
| Registered standards | 78 | 78 | — |
| **Corpus nodes** (`repo-data.json`, recursive) | **1,006** | **788** | **218 behind** |
| Zero-node registered shells | 32 | 32 | — |
| `index/` files | 24 | 23 | **`provision-truth-aliases.json` absent** |
| `repository/` subdirectories | 14 | **1** (`index/` only) | 13 absent |
| `provision-truth/` store | present, 9 files, 3 batches | **absent** | entire store |

Two consequences follow, and both matter to this sync:

- **The MIW snapshot is a 2026-07-25 projection.** Its `manifest.json` and `version.json` both
  still report `788` nodes and `generatedAt: 2026-07-25`. `MIW_TRUE_SOURCE_CONTRACT.md` §13
  reports 1,006 nodes — that figure was measured against the **canonical** repository, not
  against MIW's copy. Neither document is wrong; they describe different files. Anyone
  re-measuring must say **which tree** they measured.
- **`provision-truth-aliases.json` is missing from MIW.** The contract (§13) names that exact
  file as the mechanism for resolving the MARPOL Annex VI dual-representation problem. The
  resolver seam cannot answer an Annex VI question without it.

### 2.1 The Annex VI dual-representation problem is live, and it is measurable

Counted in the MIW snapshot: **56 nodes** carry an Annex VI-shaped id, split across two
disjoint vocabularies with no stated rule for choosing between them —

```
MARPOL-VI-14      MARPOL-VI-14-141   MARPOL-VI-14-144   MARPOL-VI-14-148   (under marpol-73-78)
MEPC32876-3-14    MEPC32876-3-15     MEPC32876-3-16                        (under mepc-328-76)
```

**This must be resolved before a single Annex VI `reference_shelf` entry is written**, not
after. A question citing "Annex VI regulation 14" currently has two defensible ids; if
production picks one per paper, the corpus fragments silently and cross-paper relation (contract
§11 — one object, many questions) breaks without any build failing.

---

## 3. SYNC DESTINATION — where the Founder should place the completed corpus

**Primary action: refresh the MIW consumer snapshot from the canonical repository.**

```
FROM  F:\RulesApp\repository\index\                 (canonical, private)
TO    F:\Marine-Intelligence-Weekly\RulesApp\repository\index\
```

That single directory carries everything the resolver needs and is already tracked in MIW.
The refresh must include **`provision-truth-aliases.json`**, which does not exist in MIW today.

**Secondary, and only if the Founder wants provision-level evidence inside MIW:**

```
TO    F:\Marine-Intelligence-Weekly\RulesApp\repository\provision-truth\
        _batches\<batch>.manifest.json
        marpol-73-78\<batch>.json
```

mirroring the canonical layout exactly (`provision-truth/<standardId>/<batch>.json`). **This
directory does not exist in MIW and should not be created speculatively.** MIW needs it only if
the viewer is to serve verified provision text from the public repository — which raises a
publication question the Founder has not decided, because **the MIW repository is public and
the corpus repository is private**.

> **Publication boundary — Founder decision required before any `provision-truth/` sync.**
> Copying verified provision text into MIW publishes it. Syncing `index/` alone publishes only
> ids, labels and structural metadata, which is already the case today. Recommendation: sync
> `index/` now, and treat `provision-truth/` as a separate decision taken with the viewer.

### 3.1 What is NOT yet present anywhere on this laptop

Counted in the canonical repository this session, the `provision-truth/` store holds **three
batches**: MARPOL Annex I ODME reg 31, SOLAS II-1 reg 29, and SOLAS II-1 Part C regs 30–39.
**There is no MARPOL Annex VI provision-truth batch in the local canonical repository.**

The completed Annex VI work is therefore expected to arrive **from the desktop / GitHub**, not
from a local directory. This session did not invent a source path and could not verify Annex VI
content it has never seen. The Founder's sync is a real prerequisite, not a formality.

---

## 4. CONSUMPTION CONTRACT — how a Written answer uses the corpus

The schema already exists and is already validated. **No schema change is proposed.**

```
MIW CORPUS (private master)
    ↓  sync
repository/index/  — repo-data.json + provision-truth-aliases.json
    ↓  resolver
object_id  →  standard → edition → version → bookmark → viewer destination
    ↓
QP spec: questions[].reference_shelf[]
    ↓
build_paper.py → reference_href() → /reference/<object-id>
```

The minimum fields needed to reference a provision are **already** the five in the contract's
data contract, and they are already enforced by `validate_spec.py::check_reference_shelf`:

| Need | Carried by | Owned by |
|---|---|---|
| instrument + provision | `object_id` (e.g. `MARPOL-VI-14-146`) | corpus |
| version / effective date | `standards[].editions[].versions[]` — `effectiveFrom` / `effectiveTo` / `status` | corpus |
| citation / display text | `label` | QP spec, derived |
| which claim it supports | `claim_scope` | QP spec, authored |
| relation type | `relationship` (closed vocabulary) | QP spec, authored |
| availability | `state` | build-time, from resolver |
| source URL / path | **nothing** — deliberately | resolver only |

**Nothing needs to be added.** The one file that changes when the resolver lands is
`reference_href()` in `build_paper.py`. That is by design and it must stay that way: the paper
builder must not learn what an edition is.

### 4.1 What sync does NOT change

- No spec gains a reference until a **resolvable** object exists (standing stop condition).
- No regulation text is copied into a spec, ever. Contract §11.
- Page numbers remain forbidden; `validate_spec.py` fails the build on them and did so before
  the first reference existed.

---

## 5. ENRICHMENT BOUNDARY — authority versus authorship

The corpus is **evidence**. It is not an answer author. This boundary is not negotiable, because
an examiner marks judgement, not quotation.

| The corpus supplies (authority) | Production Claude still decides (authorship) |
|---|---|
| verified regulation wording | which provision actually answers *this* question |
| instrument, annex, edition | examiner relevance and weighting |
| effective / amendment dates | **temporal applicability at the sitting date** |
| provision ownership and hierarchy | what belongs in Model Answer vs Study Guide |
| amendment status | technical and legal interpretation |
| citation metadata | how much detail a limb can carry in the word budget |

**The sharpest case, and the one most likely to go wrong.** The corpus states when an amendment
entered into force. It cannot state whether that amendment was in force **at the sitting being
answered**. Every temporal trap this corpus has produced — the 34th Assembly boundary, MLC 2025,
COGSA 2025, MS Act 2025 commencement — was a *sitting-relative* judgement. A corpus lookup would
have supplied the date and still left the judgement untouched.

> **Corpus availability must never be read as corpus applicability.** A resolvable
> `REFERENCE_AVAILABLE` object proves the provision exists and is current *today*; it proves
> nothing about the paper being answered.

Derived-layer integrity (contract §10) applies to shelf `label` and `claim_scope` exactly as to
flashcards: a reference label may not be more categorical than the verified answer.

---

## 6. PILOT PLAN — designed, NOT EXECUTED

**Do not run this before the Founder's sync.** It is scoped small on purpose: the question is
whether corpus backing changes anything measurable, and three questions answer that.

### 6.1 Candidate questions

Chosen because each is Annex VI-dependent and already solved and verified, so the pilot compares
against a known-good baseline rather than authoring anything new. The final three should be
picked by grepping the solved specs for Annex VI dependence at pilot time — the shortlist below
is a starting point, not an allocation:

- a **sulphur / ECA changeover** question (`MARPOL-VI-14`, the reg 14.6 record requirement)
- a **fuel oil quality / bunker delivery note** question (`MARPOL-VI-18`)
- a **CII / EEXI or Net-Zero Framework** question — deliberately included because it is the one
  where the corpus's amendment status and the sitting-relative judgement most obviously diverge

### 6.2 What is compared

For each pilot question, current handling versus corpus-backed handling:

| Measure | What counts as a result |
|---|---|
| Duplicate research avoided | research steps the corpus would have made unnecessary |
| Citation completeness | provisions named in the answer that resolve to an object |
| **Version correctness** | did the corpus edition agree with what the answer asserts |
| Candidate link quality | does `/reference/<id>` land on the exact section, or near it |
| Enrichment value | did anything in the answer actually improve, or only gain a link |
| **Dual-representation resolution** | did `MARPOL-VI-*` or `MEPC32876-*` win, and by what rule |

### 6.3 Stop conditions for the pilot

- If the dual-representation rule (§2.1) is unresolved, **stop** — do not pick an id per paper.
- If a pilot reference would require editing a verified answer, that is a **finding**, not a
  licence to edit. Record it; do not change an approved answer to fit a corpus object.
- If no measure improves, the honest result is *the corpus adds link value only*, and that is a
  legitimate outcome to report rather than to engineer around.

---

## 7. Acceptance for the sync itself

After the Founder syncs, before anything consumes it:

1. Re-count nodes in **both** trees and state which tree each figure came from.
2. Confirm `provision-truth-aliases.json` is present in MIW.
3. Confirm `manifest.json` / `version.json` in MIW report the **new** counts — a stale manifest
   beside fresh data is exactly the drift this document exists to catch.
4. Run `run_toolchain.py` and `solvedqp_check.py`. **Neither should change a single product
   byte** — no spec references the corpus yet, so a sync that moves product output means
   something consumed it that should not have.
5. Only then resolve §2.1, and only then write the first `reference_shelf` entry.
