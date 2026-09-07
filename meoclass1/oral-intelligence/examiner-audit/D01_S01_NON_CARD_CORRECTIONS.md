# D01-S01 — the two corrections that are not oral cards

**Record id:** `D01-S01-NONCARD-20260907`
**Baseline:** `1eb467f` · **Governing:** `d615eae`
**Covers:** RC-03 (the D01 mental skeleton) and RC-04 (QP2506 q2, a past paper)

## Why these are not correction manifests

The correction-manifest schema is built for **oral question cards**: it digests a
balanced `<div class="q-card" id="qN">` with
`tools/oral/validate_batch_h_series.card_digests`, and every corpus-wide check —
`declared_cards_present_live`, `pre_edit_digests_match_baseline`,
`live_matches_authorised_post_state` — resolves a declared entry through that one
function.

Neither of these corrections is such a card:

| RC | Target | Why the schema cannot hold it |
|---|---|---|
| **RC-03** | `docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md`, MENTAL SKELETON branch 1 | A markdown study pack. It has no card anchor and no card digest. |
| **RC-04** | `meoclass1/pastpapers/QP2506.html` `q2` | A past paper, whose answers are `<article class="q-card">`. `card_digests` reads `<div>` cards and returns nothing for it. |

I wrote both as correction manifests first. `validate_corrections.py` refused them —
`declared_cards_present_live missing=[…#MENTAL_SKELETON_branch_1]`,
`…missing=['meoclass1/pastpapers/QP2506.html#q2']` — and the refusal was **correct**.
A record that declares a card the card layer cannot see is a record whose pins cannot
be verified by anything, which is exactly the decorative governance the schema exists
to forbid. This is the same lesson as `P1GUARD-20260906`, which could not be a
correction manifest because it corrected no card: **when the schema refuses your
record, the schema is usually right and the vehicle is usually wrong.**

## RC-03 — the D01 mental skeleton

| | |
|---|---|
| **File** | `docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md` |
| **Scope** | MENTAL SKELETON, **branch 1 only** |
| **Digest method** | `STUDY_ASSURANCE_LOCAL_V1_FILE` — sha256 over LF-normalised whole-file bytes, the method the Lane-B audit recorded |
| **Pre** | `5f704a681ae001cc80cc3924ae80d4efdf789386c80b42618c3bb843edd55cdf` |
| **Post** | `7a017db23239826b39f499dafbb85ed3f42481b06dbd90123ebbeaad4f5b9333` |

**The defect.** Branch 1 read *"The IMO instrument hierarchy — Convention → Protocol →
Code → Resolution → Circular."* An arrow chain in a memorisation skeleton reads as
descending legal force, and `known_traps.md` #53 had already struck the same ladder down
in `QB9_G`. A skeleton is the most dangerous place for it: it is designed to be recalled
without re-derivation.

**The correction.** Branch 1 is now *"IMO instrument families & legal effect"* — three
questions (which instrument? what makes this provision binding, and on whom? mandatory
or recommendatory?) and three facts: a **Protocol may itself be treaty law** (the 1988
SOLAS and Load Line Protocols); a **Code is mandatory when a binding instrument makes it
so** (ISM via SOLAS IX); a **Resolution or Circular has no single legal effect** — MSC
resolutions adopt mandatory amendments, Assembly resolutions recommend. **74 words**, and
a gate asserts it stays short, because a skeleton that cannot be recalled in seconds is
not a skeleton.

**Authority.** HELD — `known_traps.md` #53 on VCLT 1969 Art.2(1)(a): a treaty is an
international agreement governed by international law *"whatever its particular
designation"*. The 1988 Protocols are treaty law and are the HSSC instruments — the same
fact RC-01 turns on. SOLAS Art.VIII(b) annex amendments are adopted **by MSC
resolution**, which is what makes the ladder wrong in both directions.

**Invariants.** Only branch 1 changed; branches 2–9 are byte-identical, asserted by a
gate. No instrument is presented as outranking another.

## RC-04 — QP2506 q2, the Net-Zero worked example

| | |
|---|---|
| **File** | `meoclass1/pastpapers/QP2506.html` `q2` |
| **Digest method** | `STUDY_ASSURANCE_LOCAL_V1` — sha256 over LF-normalised balanced `<article class="q-card" id="qN">` bytes |
| **Pre** | `3b9bc9bc65328934cc95eced1a07722a0db43f3ab088ae08c94e197ef5cccd0e` |
| **Post** | `91e595b0b8e5558f9d6b662d008f960793b3d47f3c4fe288b31fbc41f516ac95` |

**The defect.** One clause of the source map: *"circulated two months before this
examination and **not adopted until four months after it**."* Four months after a June
2025 sitting is MEPC/ES.2, October 2025 — which **did not adopt** the Framework.

**The correction.** That clause alone. The Framework has still not been adopted;
adoption was taken up at MEPC/ES.2 (14–17 October 2025) and **adjourned for one year**;
MEPC 84 (April–May 2026) reached no final agreement; it is **not adopted and not in
force**. The next decision point is a moving date and is **not asserted** — §8 of the
instruction forbids asserting an adoption or reconvening date not verified from official
IMO scheduling, so the volatile part is routed to `known_traps.md` #30 with a re-verify
instruction. The teaching point is stated explicitly: approval ≠ adoption ≠ entry into
force.

**Why the rest of the answer was not touched.** A past paper is anchored to its sitting.
It may be wrong about what happened *after* that sitting without being wrong about the
sitting itself — and this answer's own flashcard already said *"At the date of this
examination it had been circulated but not adopted"*, which is correct and is
byte-identical. The entry-into-force spine (SOLAS 1974, the 1978 MARPOL Protocol, tacit
acceptance, VCLT Arts. 14(2) and 15) and the "Uncertainty and currency" section are
byte-identical. **The examiner's question stem is untouched.**

**Referred, not corrected.** Lane B flagged the same answer's citation of *"IMO
Convention, Article 38(e) — the Organization's depositary and convention functions"* as
probably wrong (Art. 38 concerns the functions of the Maritime Safety Committee) but did
**not** establish the correct article. It is left as it stands and referred to Lane B.
Substituting a plausible article number would reproduce the exact defect RC-06 exists to
punish — a real instrument cited for the wrong proposition.

## Verification

Both corrections are guarded by named checks in
`tools/oral/validate_correction_d01s01.py` (RC03_* and RC04_*, 12 checks) and attacked by
mutations **B** and **C** in `tools/oral/mutate_correction_d01s01.py`, which restore the
ladder and restore "adopted" respectively. Both are caught.

Digests are pinned above and re-derived from the live bytes by the gate, so this record
is verifiable even though the card layer cannot read either target.
