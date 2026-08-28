**Date:** 2026-08-28
**Classification:** Content
**Severity:** Critical
**Summary:** CA-EM-0003, the current framework answer on Treaty/Convention/Protocol, taught a legal hierarchy that does not exist, and then carried four unsourced generalisations after the hierarchy itself was corrected.
**What Was Wrong:** Version 1.0 of the current-answer library entry CA-EM-0003 presented Treaty, Convention and Protocol as a ranked ladder. It stated that a protocol is "a treaty subordinate to a parent convention", extended the ladder to a fourth rung with "Below all three sit the codes", opened the study guidance on that hierarchy, carried the same ranking into the comparison table, and put the ranking into the 15-second recall — the surface a candidate actually memorises. It also narrowed a protocol to "the instrument that modifies or supplements a convention", and collapsed consent to be bound into four named acts as though they were the only routes. Version 2.0 corrected the hierarchy but over-reached on authority: it asserted an IMO example list, a general rule about convention entry into force and amendment, a general protocol-relation taxonomy, and a general claim about party status, none of which the available source pack establishes.
**Correct Position:** VCLT 1969 Article 2(1)(a) makes an international agreement a treaty "whatever its particular designation", so the designation does not determine whether an instrument falls within that definition. Convention and Protocol are designations; a protocol meeting the Article 2(1)(a) criteria is itself a treaty, and its title alone does not alter that conclusion. Article 2(1)(b) defines ratification, acceptance, approval and accession; Article 11 supplies the means by which consent to be bound may be expressed, and ratification is not the only means it lists; Article 3 keeps Article 2(1)(a) a definition for the Convention's purposes rather than an exhaustive one. The Protocol of 1978 relating to MARPOL, Article IV(1) permits three distinct routes, which disproves any universal protocol-ratification rule. Sources A–F do not establish any general proposition about legal rank or hierarchy, and nothing beyond them is asserted. This field states the FINAL position at version 2.7. It was written on 2026-08-26 against the version 2.0 position and, until this correction, still carried three propositions the later reviews withdrew as unsourced: that a title confers no rank and there is no ladder; that the available means of consent are fixed by an instrument's own final clauses; and that a convention's legal effect and operation depend on the terms of that instrument. Those withdrawals are recorded in the version trail and the withdrawn-wording inventories below, which are preserved verbatim as history and are NOT corrected forward here.
**Primary Source:** Vienna Convention on the Law of Treaties 1969, Articles 2(1)(a), 2(1)(b), 3 and 11, read at source; Protocol of 1978 relating to the International Convention for the Prevention of Pollution from Ships, 1973, Article IV(1), read at source; IMO MARPOL summary propositions, used only as MARPOL's own provenance and deliberately not generalised. These are Sources A–F of the frozen review envelope and they are the complete authority boundary of the corrected entry.
**Files Affected:** meoclass1/current-answers/specs/CA-EM-0003.json (canonical), meoclass1/current-answers/registry.json (regenerated projection), solvedQP/current/CA-EM-0003.html (regenerated projection), tools/current_answers/validate_open_g1_014.py (targeted gate), tools/current_answers/test_open_g1_014_mutations.py (mutation harness), corrections/2026-08-26_open-g1-014-treaty-convention-protocol-hierarchy.md (this record), meoclass1/oral-intelligence/examiner-audit/AUGUST2026_OPEN_ITEMS.json (status pointer only). These SEVEN paths are the complete publication payload. REVIEW PACKETS ARE NOT AMONG THEM: the eight packets produced across this lineage, v2.1 through the final CA-EM-0003-v2.7-final-review-packet.md, are immutable external-review evidence held OUTSIDE this repository at F:\AI-Controller-Runtimes\miw\review-packets\, and none is published or committed. An earlier draft of this line named a v2.2 packet as an affected file and omitted the v2.7 packet that actually carries the closing PASS; that was wrong on both counts and is corrected here before this record was ever committed. The verdict-bearing object is CA-EM-0003-v2.7-final-review-packet.md, 8201 bytes, sha256 26eff52132f3fa83d398d4128510aeaf82eeb2533479b7129e3488254bb62df2, recorded in full in CA-EM-0003-v2.7-EXTERNAL-REVIEW-RECORD.json alongside the v2.5 and v2.6 records.
**Related known_traps.md Entry:** None. `meoclass1/known_traps.md` owns the Oral question-bank current-state reference; this correction is in the current-answer library pipeline, which carries its own gate (`tools/current_answers/validate_open_g1_014.py`) and its own mutation harness. Adding a trap entry here would duplicate that gate in prose, against `docs/ENGINEERING_PRINCIPLES.md` P2. The sibling defect in the Oral bank (QB9_G#q6) was corrected separately by CORR-DEFN-TREATY-20260825.
**Related Manifest Update:** meoclass1/current-answers/registry.json, regenerated by `tools/current_answers/build_current_answers.py`. Never hand-edited. `meoclass1/qb_content_index.json` is not touched: it is the Oral question-bank manifest and this entry is not in that pipeline.
**Flagged By:** Audit/review finding — the bank-wide definition/legal-terminology audit run under CORR-DEFN-TREATY-20260825 after QB9_G#q6 was corrected, by an INDEPENDENT clean-context consistency sweep rather than by the producing pass. The four version 2.2 fixes were flagged by a second, external independent clean-context review of the version 2.1 text.
**Commit:** PENDING LANDING COMMIT. This entry lands in the substantive publication commit together with the content fix and the register transition, per `corrections/README.md` Lifecycle §4. That commit cannot contain its own hash, so this token is written locally and is replaced with the real hash by an immediately following metadata-only commit; both are pushed together, and the token never reaches the remote. The hash recorded here is the SUBSTANTIVE publication commit, not the metadata commit that writes it.

---

## Why this record lives here

`R-CA-NO-EXAMINER` in `tools/current_answers/validate_current_answers.py` forbids any `CA-EM-####` identifier from appearing anywhere in the examiner / oral evidence layer, which the gate defines as `meoclass1/oral-intelligence/**` plus three named index files. The rule exists for a reason that is not negotiable: a present-day canonical question was set by nobody, and if a synthetic question's id leaks into the evidence layer, every recurrence count MIW publishes becomes partly a count of MIW itself.

The full OPEN-G1-014 operational record could not satisfy that rule and remain useful, because the record's entire content is about a specific current-answer entry and cannot describe itself without naming it. Registering the finding in `meoclass1/oral-intelligence/examiner-audit/AUGUST2026_OPEN_ITEMS.json` therefore put the two in direct conflict from the moment the finding was registered (commit `47aa3dd`).

The conflict is resolved by placement, not by weakening the rule. `corrections/` is this repository's existing, governed home for exactly this artifact — "the durable, greppable record of what was corrected in this repository, when, and why" (`corrections/README.md`, Purpose). It is not part of the examiner evidence layer, so a `CA-EM-####` id here is not a claim that an examiner asked anything. `R-CA-NO-EXAMINER` is unchanged, unnarrowed and unrefactored. The August intake file retains a status pointer only, naming `CORR-DEFN-TREATY-20260825` and this record, and carrying no `CA-EM-####` identifier.

No examiner evidence is invented by this move, and none is removed: the intake entry's own registration facts, its found-via provenance, its status and its history are preserved below in full.

---

## Current state — CLOSED

**Status: CLOSED — CORRECTED AND INDEPENDENTLY REVIEWED.**

This finding is CLOSED and VERIFIED at **answer_version 2.7**, on an independent external review that returned
**PASS** with **no required fixes**. It is the first PASS in this lineage: the seven earlier 2.x reviews all
returned PASS_WITH_FIX and authorised nothing.

The reviewed object is the version 2.7 review packet, **8201 bytes**, sha256
`26eff52132f3fa83d398d4128510aeaf82eeb2533479b7129e3488254bb62df2`. Its embedded Sources A–F block is
**1384 bytes**, sha256 `deac75a6fe61ace07bfdd6cb2d398632d064eee7b847fdae469c8f47aaa17bd5` — an exact match to the
baseline carried unchanged since version 2.4. The reviewer worked from Sources A–F alone: no web, no new official
source, no treatise, no dictionary, no general international-law knowledge, and no MIW prose used as authority.
The packet is external review evidence held outside this repository and is not a published page.

**Publication eligibility attaches to version 2.7 ONLY.** The version 2.5 and 2.6 verdicts were PASS_WITH_FIX and
carry no authority, and the PASS already recorded in `review_record` belongs to version 1.0 and does not carry
forward. The externally reviewed text is now immutable: any candidate-facing character change would invalidate the
PASS that closes this finding.

**The hold recorded on 2026-08-26 was correct and is preserved, not erased.** At that time the content correction
was applied and proven but no independent PASS was tied to it, and closing on a self-review would have been the
precise failure the current-answer gate exists to prevent — "verified" spent on an unverified answer. The hold is
what made this closure honest: the review was obtained rather than assumed.

### Version trail

| Version | What it did | Independent review |
|---|---|---|
| 1.0 | First publication. Taught the hierarchy. | PASS — covers 1.0 only |
| 2.0 | Withdrew the hierarchy; restated the model provision by provision from VCLT and MARPOL Protocol 1978. | PASS_WITH_FIX (7 fixes) |
| 2.1 | Applied FIX-01..07: withdrew the taxonomy statements, the generalised entry-into-force formula, the amendment-mechanism claim, two protocol examples, the codes digression; narrowed the adoption statement; cut the recall to four spoken sentences. | PASS_WITH_FIX (4 fixes) — core legal correction PASSED against Sources A–F |
| 2.2 | Applied FIX-A..D: removed the unsourced IMO example list; replaced the general convention entry-into-force/amendment claim; narrowed the protocol-relation claim to the MARPOL 1978/1973 example; removed the general party-status claim. Plus one MARPOL wording refinement. No core conclusion changed. Recall unchanged byte for byte. | PASS_WITH_FIX (5 fixes) — core legal correction PASSED against Sources A–F |
| 2.3 | Applied FINAL FIX 1..5: removed the unsourced designation example list; anchored the means-of-consent sentence to Article 11 with availability depending on what is agreed; applied the same Source-D-safe wording to the protocol paragraph and the comparison table with MARPOL Art.IV(1) and its three routes intact; withdrew the general functional taxonomy in favour of the no-hierarchy statement; corrected the single recall sentence. No core conclusion changed. | PASS_WITH_FIX (4 fixes) — core legal correction PASSED against Sources A–F |
| 2.4 | Applied FINAL FIX A..D: deleted the unsourced adoption-of-text limb; replaced the broad Convention legal-effect/operation formulation, in the answer body and the comparison table alike, with "The title Convention does not itself create a legal rank"; replaced the Protocol absolute with "The title Protocol does not by itself make the instrument legally inferior or subordinate to a convention", keeping the Article 2(1)(a) point that such a protocol is itself a treaty; deleted the two MARPOL propositions Source F does not carry, retaining its dated history in full. No core conclusion changed. Recall unchanged byte for byte. | PASS_WITH_FIX — central legal core found sound provision by provision with no primary-source conflict; five bounded contractions required, applied at 2.5. Recorded in this entry's own `review_record.scope_of_this_review`. |
| 2.5 | Applied the five bounded contractions required by the fifth independent clean-context review of the version 2.4 text, each of which deletes or narrows a statement to what the primary instruments actually establish. No core conclusion changed, the answer was not expanded and no authority was added. | PASS_WITH_FIX (4 fixes, EXT-01..EXT-04) — central legal direction SOUND; the answer still converted designation-independence into statements of legal RANK, which Sources A–F do not establish. |
| 2.6 | Applied EXT-01..EXT-04: removed "confers no rank" from the Treaty paragraph and the major-trap recall; contracted the Convention paragraph and table row; removed "legally inferior class" and the subordination claim from the Protocol paragraph and table row; narrowed the final takeaway so Article 2(1)(a) no longer "settles" every hierarchy question. | PASS_WITH_FIX (3 fixes, EXT-2.6-01..EXT-2.6-03) — substantially correct; three residual affirmative rank/hierarchy propositions remained. |
| **2.7** | Applied EXT-2.6-01..EXT-2.6-03 as **contraction by removal**, substituting nothing: the Convention heading "a designation, not a rank" became "Article 2(1)(a) applies whatever the designation"; the MARPOL paragraph lost "but that relationship does not create a legal hierarchy merely from the titles", leaving the 1978/1973 relationship and continuing into the Article 11 and Article IV(1) discussion untouched; the final takeaway lost "and do not create a hierarchy between these instruments". No core conclusion changed. | **PASS — no required fixes.** |

### FINAL FIX 1..5 — the withdrawn wording, verbatim

Held here and **not** on any candidate-facing surface. This is the inventory the
rendered version history deliberately does not repeat.

| Fix | Withdrawn wording (verbatim) | Replaced by | Guard |
|---|---|---|---|
| FINAL FIX 1 | "An instrument titled convention, protocol, agreement, charter or covenant is a treaty if it meets those criteria." | "An instrument is a treaty if it meets those criteria, whatever its particular designation." | G20 |
| FINAL FIX 2 | "Which of the Article 11 means is actually available for any given instrument is decided by **that instrument's own final clauses** - not by what the instrument is called." | "Which of the **Article 11** means of expressing consent is available for a particular instrument depends on what is agreed for that instrument, not on what the instrument is called." | G21 |
| FINAL FIX 3 | "How a State becomes party to a protocol is decided by that instrument's **own final clauses** and not by its title"; and, in the comparison table, "by whichever means its own final clauses allow" | "The means by which a State expresses consent to be bound depend on what is agreed for that particular instrument, not on its title"; and "by whichever means are agreed for that particular instrument" | G22 |
| FINAL FIX 4 | "The distinction between the three is one of **function**, not of rank:" | "The key legal point is that these titles **do not create a hierarchy**:" | G23 |
| FINAL FIX 5 | "How a State becomes bound is decided by the instrument's OWN FINAL CLAUSES, not by what the instrument is called." | "How a State expresses consent to be bound depends on what is agreed for that particular instrument, not on what it is called." | G24 |

Consequential sweeps made under the same five fixes, so that no candidate-facing
surface retained a withdrawn formulation while one block was corrected:

- `present_day_examinable_core`: "the difference between them is one of FUNCTION and not of legal rank" → "these titles do not create a legal hierarchy".
- `understand_first`: "What separates a convention from a protocol is the JOB the instrument does, not a position on a ladder." → "These titles do not create a hierarchy, and neither designation occupies a position on a ladder."
- `study_guide`: "distinguished by the job the instrument does and not by rank" → "because these titles do not create a hierarchy".
- `quick_revision.keywords`: "own final clauses" → "what is agreed for that instrument".
- `quick_revision.critical_regulation`: "the worked maritime example of an instrument's own final clauses offering several of those means" → "…of an instrument for which several of those means are agreed".
- `quick_revision.major_trap`: "consent to be bound follows the instrument's own final clauses (VCLT Article 11)" → "the means of expressing consent to be bound are those of VCLT Article 11, and which of them is available depends on what is agreed for that instrument".
- `authority_sources[2].checked`: "a protocol's own final clauses - not its title - decide how consent to be bound is expressed" → "what is agreed for a particular instrument - not its title - determines how consent to be bound may be expressed".
- `version_history[2.0].reason`, a **rendered** field: the clause "the difference between one designation and another is one of function", the clause "a code is not a treaty at all and binds only through the instrument that makes it mandatory" (withdrawn from the answer itself at 2.1 but left standing in the projection), and the clause "the means actually available being fixed by the instrument's own final clauses" were each replaced by their source-safe equivalents. The verbatim originals are preserved under "Preserved in full — the internal version-history provenance" below. No history was deleted.
- `version_history[2.3].reason`: an earlier draft of this job's own history entry described FINAL FIX 4 as withdrawing a statement that "the difference between the designations is one of function". Because `reason` is a rendered field, that restated the withdrawn phrase to a candidate under a withdrawal verb — the same defect the fix-label guard exists to prevent. It was rewritten to "A general taxonomic statement about how the designations differ from one another is withdrawn". Caught by the candidate-facing stale-phrase scan, not by a guard, because the guards correctly read it as non-assertive.

### FINAL FIX A..D — the withdrawn wording, verbatim

The fourth independent review of the version 2.3 text returned PASS_WITH_FIX:
the central legal correction PASSED again against Sources A–F, and four bounded
source-boundary overreaches remained. FINAL FIX D carried two distinct
propositions, so four fixes withdraw five formulations and five guards defend
them.

Held here and **not** on any candidate-facing surface. This is the inventory the
rendered version history deliberately does not repeat.

| Fix | Withdrawn wording (verbatim) | Replaced by | Guard |
|---|---|---|---|
| FINAL FIX A | "; adoption of the treaty text does not by itself establish a State's consent to be bound." | Deleted outright. The retained sentence stands alone: "A treaty binds only those States that have expressed consent to be bound by it." | G25 |
| FINAL FIX B | "The legal effect and operation of a particular convention depend on the terms of that instrument; they do not follow merely from the title **Convention**." — and, in the comparison table, the Convention "What it does" cell "Whatever the terms of that particular instrument provide - its legal effect and operation do not follow merely from the title" | "The title **Convention** does not itself create a legal rank." — in both places | G26 |
| FINAL FIX C | "Being called a protocol tells you nothing about the instrument's legal force." | "The title **Protocol** does not by itself make the instrument legally inferior or subordinate to a convention." The preceding Article 2(1)(a) sentences — that such a protocol **is itself a treaty**, and that no hierarchy arises from a title — are retained unchanged. | G27 |
| FINAL FIX D(i) | "and it absorbed the parent Convention" (answer); "it was the 1978 Protocol that absorbed it and brought the combined instrument into force" (`understand_first`) | Deleted. Retained: "Following the tanker accidents of 1976-77 the **1978 Protocol** was adopted, and the combined instrument entered into force on **2 October 1983**." | G28 |
| FINAL FIX D(ii) | "and the resulting combined regime is commonly referred to here as **MARPOL 73/78** rather than as MARPOL 1973" | Deleted. Source F carries no naming-practice proposition. | G29 |

Consequential sweeps made under the same four fixes, so that no candidate-facing
surface retained a withdrawn formulation while one block was corrected:

- `quick_revision.keywords`: the entry `"MARPOL 73/78"` removed. The short form existed on the page only to carry the withdrawn naming-practice claim.
- `quick_revision.critical_numbers`: "MARPOL - Convention adopted 2 November 1973, absorbed into the 1978 Protocol" → "…, not in force independently"; "MARPOL 73/78 - the combined instrument entered into force 2 October 1983" → "MARPOL - the combined instrument entered into force 2 October 1983".
- `authority_sources[3].source`: the clause "the 1978 Protocol absorbing the parent Convention;" removed from the Source F description, so the source note does not assert what the source does not carry.
- `authority_sources[3].checked`: "Relied on at versions 2.1 and 2.2 ONLY as the provenance of MARPOL 73/78" → "Relied on at versions 2.1 to 2.4 ONLY as MARPOL's own history".
- `version_history[2.0].authority`, a **rendered** field: "was absorbed by the 1978 Protocol, hence MARPOL 73/78" → "and the combined instrument entered into force on 2 October 1983".
- `version_history[2.1].reason`, a **rendered** field: "the adoption statement is narrowed to say only that adoption of the treaty text does not by itself establish a State's consent to be bound" → "the statement about the effect of adopting a treaty text is narrowed". The 2.1 provenance recited the FINAL FIX A sentence verbatim in a field the builder projects onto the candidate page.
- `version_history[2.2].reason`, a **rendered** field: "…is replaced by the narrower statement that the legal effect and operation of a particular instrument depend on that instrument's own terms and do not follow merely from its title" → "…is replaced by a narrower statement"; and "aligns the MARPOL provenance sentence" → "aligns the MARPOL history sentence".
- `version_history[2.4].reason`: the first draft of this job's own history entry described FINAL FIX B as replacing "a broad claim about the legal effect and operation of an instrument bearing one designation". G26 rejected it on the first run — the guard caught the withdrawal record reciting the withdrawn phrase on a rendered surface, which is exactly the leak the fix-label discipline exists to prevent. Rewritten to "a broad claim about how an instrument bearing one designation works in law". This is the second time a `reason` field has had to be scrubbed for this reason; the pattern is now the rule rather than the exception, and the 2.4 `authority_hold` records it as a declared consequential scrub.

The verbatim originals of every rendered-history field scrubbed above are
preserved under "Preserved in full — the internal version-history provenance"
below, and in `version_history[2.4].authority_hold`. **No history was deleted.**

### Exact remaining work — NONE

All three items the hold recorded are discharged.

1. **Independent review — OBTAINED.** The clean-context packet was given to a genuine independent reviewer at each
   of versions 2.5, 2.6 and 2.7, and every verdict was persisted rather than assumed. The final verdict is PASS.
2. **Material review fixes — APPLIED AND RE-VERIFIED.** Each PASS_WITH_FIX was applied canonically in the spec,
   never by hand-editing rendered HTML, then rebuilt through `tools/current_answers/build_current_answers.py` and
   re-gated. At version 2.7 the targeted validator reports 38/38, the targeted mutation suite 44/44 rejected with
   escapes, no-ops, crashes and misnamed all zero, the repository-wide current-answer gate 52/52 including
   `R-CA-NO-EXAMINER`, the owner-reader contract 14/14, and the library mutation suite 24/24. Projection freshness
   is proven by consecutive rebuilds reporting every output identical on the second run. Guards G35, G37 and G38
   and mutations M39, M39B, M39C, M41 and M42 stand unweakened.
3. **The `review_status` question — RESOLVED BY EVENT.** The dilemma was that `ca_model.RENDERABLE` is defined as
   authority plus an independent review that passed, and version 2.4 had the authority but not the review, so the
   honest label would have un-rendered the page and silently withdrawn the answer from all six live routes. Version
   2.7 now holds both halves, so the status is earned rather than downgraded or spent.

**One observation is carried forward deliberately, and it is not a defect in the reviewed answer.**
`study_guide.blocks[1].p` still contains the phrase "do not create a hierarchy". That surface was outside the
independently reviewed packet — a full sweep of the version 2.7 packet for "hierarchy", "ladder" and "rank" returns
zero matches — and outside the frozen correction boundary, so the external finding does not reach it. It was
therefore neither edited nor allowed to block this closure, because reopening the externally PASSed answer to reach
it would have invalidated the PASS. It is recorded as a source-boundary observation for later product-wide
consistency work. `understand_first` likewise retains title-limited wording previously adjudicated as source-safe
and left byte-frozen.

---

## Preserved in full — the original OPEN-G1-014 intake record

Reproduced verbatim from `meoclass1/oral-intelligence/examiner-audit/AUGUST2026_OPEN_ITEMS.json` as it stood before the status pointer replaced it. Nothing is summarised away; this is the record, moved, not rewritten.

```json
{
  "id": "OPEN-G1-014",
  "title": "CA-EM-0003, the CURRENT FRAMEWORK ANSWER on Treaty/Convention/Protocol, teaches that a protocol is subordinate to a parent convention - and now contradicts the corrected QB9_G#q6 head-on",
  "found_via": "CORR-DEFN-TREATY-20260825, by the bank-wide definition/legal-terminology audit run after QB9_G#q6 was corrected. Found by an INDEPENDENT clean-context consistency sweep, not by the producing pass, and every line was then re-verified directly against the file.",
  "evidence": "solvedQP/current/CA-EM-0003.html, verified line by line: L546 'A protocol is itself a treaty, subordinate to a parent convention'; L558 comparison-table row 'Protocol | A treaty subordinate to a parent convention'; L561 'Below all three sit the codes', completing a four-level ladder Treaty > Convention > Protocol > Code; L566 study guide 'Open with the hierarchy in one sentence'; L575 15-second recall 'Protocol = a treaty subordinate to a parent convention'. The section heading above L546 also narrows a protocol to 'the instrument that modifies or supplements a convention', omitting framework-implementing and optional protocols. The same text is in the regenerating source spec meoclass1/current-answers/specs/CA-EM-0003.json at lines 37, 50, 54, 60 and 66. VCLT 1969 Art.2(1)(a) makes an agreement a treaty 'whatever its particular designation', so there is no subordination by title; the page itself quotes that phrase at L575 while calling the protocol subordinate in the same block.",
  "candidate_impact": "HIGHEST of the five. This is the designated current framework answer for exactly the question QB9_G#q6 answers, registered at meoclass1/current-answers/registry.json and linked as the authoritative answer from six candidate-facing year pages: meoclass1/pastpapers/questions-2021.html (two links), questions-2022.html, solvedQP/questions-2021.html (two links), solvedQP/questions-2022.html, and solvedQP/current/CA-EM-0002.html. A candidate who follows the link from a year page now reads the opposite of the corrected QB9_G card, and the wrong position is in the 15-second recall, which is the surface that actually gets memorised.",
  "why_not_done_here": "The QB9_G correction was scoped to the Oral question bank, which is one governed pipeline with one manifest family, one validator set and one mutation suite. Each item below sits in a DIFFERENT governed pipeline with its own generator, spec source and derived surfaces. Spreading one correction event across four pipelines in one session is the exact shape that has produced guard expiry and undeclared drift here before. Each is registered with a verified line inventory so the closing session starts from evidence rather than from prose. Specifically: the current-answer library is governed by its own typed/limb ownership model (ca_model) with a --deliver / --publish discipline, and this repository has already recorded three readers mistaking a limb answer for a whole one. Editing the rendered HTML without going through the spec and the library's own gates would be reverted by the next regeneration.",
  "size": "One library answer plus its spec (two files), then regenerate and re-run the current-answer library gates. No other CA-EM answer carries the claim.",
  "status": "OPEN_HELD_PENDING_FURTHER_EVIDENCE",
  "verified": true,
  "predates_this_intake": true,
  "registration_note": "Registered 2026-08-25 by CORR-DEFN-TREATY-20260825. Highest priority of OPEN-G1-014..018: it is the only one that contradicts a card corrected in the same session, on the same question.",
  "hold_record": {
    "held_on": "2026-08-26",
    "held_by": "AC-000002 cycle 0",
    "why_not_closed": "The CONTENT correction is done and proven, but the finding may not be recorded as CLOSED_CORRECTED_AND_INDEPENDENTLY_REVIEWED because the 'INDEPENDENTLY_REVIEWED' half of that state was never earned. The executing environment had no independent-reviewer capability: both the subagent tool and the workflow tool were refused by the policy layer (rule TOOL_UNKNOWN, fail closed), so the clean-context review packet could not be given to any reviewer. Closing on a self-review would be the precise failure the current-answer gate exists to prevent - 'verified' spent on an unverified answer - so the hold is recorded instead.",
    "work_completed": [
      "CA-EM-0003 corrected at its canonical source meoclass1/current-answers/specs/CA-EM-0003.json. No rendered HTML was hand-edited.",
      "Every hierarchy teaching in the OPEN-G1-014 line inventory is withdrawn: title-subordination, the four-level ladder Treaty > Convention > Protocol > Code, the hierarchy-first study guidance, the comparison-table ranking, and the 15-second recall ranking.",
      "The legal model is now stated provision by provision: VCLT 1969 Art.2(1)(a) (treaty definition and 'whatever its particular designation', so a title confers no rank), Art.3 (scope qualification), Art.2(1)(b) (defines ratification, acceptance, approval, accession) and Art.11 (the means of expressing consent), with the Protocol of 1978 relating to MARPOL, Art.IV(1) as the instrument-specific worked example. No universal protocol-ratification rule remains anywhere.",
      "Version transition 1.0 -> 2.0 recorded through the library's own version_history mechanism, preserving the prior state and naming the old claims, the new claims, the reason, the authorities, the currentness and the review trigger.",
      "Projections regenerated with tools/current_answers/build_current_answers.py. Only CA-EM-0003.html and registry.json changed; the other seven entries rendered IDENTICAL. A second consecutive build reported every artefact IDENTICAL, which is the freshness proof.",
      "New targeted gate tools/current_answers/validate_open_g1_014.py: 12/12 definition invariants pass across the spec, the rendered page, the registry and the six route owners.",
      "New targeted harness tools/current_answers/test_open_g1_014_mutations.py: M01..M12 all rejected by the guard each was aimed at, with escapes=0, no-ops=0, crashes=0 and no guard credited for a collateral failure."
    ],
    "exact_remaining_work": [
      "Give the clean-context review packet (canonical question, the proposed candidate-facing answer, Sources A-F, and the AC13 rubric only) to a genuine independent reviewer, and persist the verdict in the entry's review_record.",
      "Apply any material review fix canonically in the spec, rebuild, and re-run validate_open_g1_014.py plus the M01..M12 harness as the second-pass verification.",
      "Resolve the review_status question this correction exposes, which needs a Founder/architect decision and not an executor one: ca_model.RENDERABLE is {CURRENT_ANSWER_VERIFIED} and that status is DEFINED as authority plus an independent review that passed. Version 2.0 has the authority but not yet the review, so the entry currently renders 'Independent review: PASS' from the version 1.0 review record against version 2.0 text. Downgrading the status to AUTHORITY_ESTABLISHED is the honest label but it un-renders the page and silently withdraws the answer from all six live routes. The interim disclosure is recorded in review_record.scope_of_this_review and in version_history 2.0 'independent_review'.",
      "Clear the pre-existing R-CA-NO-EXAMINER failure, which blocks the repository-wide mutation suite (tools/current_answers/test_current_answer_mutations.py aborts before mutating). It is not caused by this job: the rule forbids any CA-EM-#### id in the examiner/oral evidence layer, and commit 47aa3dd put CA-EM-0003 into THIS file when it registered OPEN-G1-014. Recording the closure of OPEN-G1-014 here cannot avoid re-stating that id, so the rule and the open-item register are in direct conflict and an architect must decide which gives."
    ],
    "invariants_held": "Only three CONTENT files changed in the working tree - meoclass1/current-answers/specs/CA-EM-0003.json, meoclass1/current-answers/registry.json and solvedQP/current/CA-EM-0003.html - plus this governance record and two new files under tools/current_answers/ carrying the targeted gate and its mutation harness. No QI recurrence/occurrence store, examiner-evidence store, oral card store or historical raw-occurrence store was written, so every one of those deltas is 0 by construction. No historical sitting-anchored answer was modified; historical pages were read for route verification only."
  }
}
```

The fourth item of `exact_remaining_work` above — the R-CA-NO-EXAMINER conflict that its author correctly identified as needing an architect's decision — is the item this record's placement resolves. The decision taken is that the *rule* gives nothing and the *placement* gives everything: the record moves to the ledger built for it, and the intake keeps a pointer.

---

## Preserved in full — the internal version-history provenance for 2.0, 2.1 and 2.2

`tools/current_answers/build_current_answers.py` renders exactly four fields of each `version_history` row into the candidate-facing "Version and review record" section: `version`, `date`, `reason` and `authority`. Those four are therefore **candidate-visible projection**, not internal provenance, and they are held to the same leakage and stale-wording discipline as the answer body. The remaining fields — `independent_review`, `authority_hold`, `version_rule`, `review_trigger`, `supersedes`, `currentness_as_of` — are never rendered and remain internal governance metadata.

The `reason` text that previously stood in the spec named the internal fix labels, the unsourced IMO instrument list and the withdrawn propositions in their own words. A candidate reading that table read the withdrawn wording, whatever the surrounding sentence said about it. The rendered `reason` fields were therefore replaced with candidate-safe substantive summaries that say what changed and why without re-stating the withdrawn text or the internal workflow vocabulary. **Nothing is summarised away here.** The complete prior text is preserved verbatim below, and this record — not the rendered table — is the audit surface for it.

### version_history[2.0].reason — verbatim, as it stood before the candidate-safe rewrite

> Correction of OPEN-G1-014, registered 2026-08-25 by CORR-DEFN-TREATY-20260825, whose record holds the verified line-by-line inventory of what was withdrawn. Version 1.0 presented the three instrument types as a LEGAL HIERARCHY, ranked a protocol below a convention by reason of its title, extended that ladder to a fourth rung for the codes, opened the study guidance on that ladder, carried the same ranking into the comparison table and the 15-second recall, defined a protocol narrowly as an instrument that modifies or supplements a convention, and treated consent to be bound as though four named acts were the only routes to it. All of that is withdrawn, and the withdrawn wording is recorded in the OPEN-G1-014 record rather than repeated here. WHAT VERSION 2.0 STATES INSTEAD: a protocol meeting the Article 2(1)(a) criteria is ITSELF A TREATY and is not a subordinate class; the difference between a convention and a protocol is one of FUNCTION and not of rank, because Article 2(1)(a) applies whatever the instrument's particular designation and a title therefore confers no rank; the codes differ in KIND rather than sitting on a further rung, because a code is not a treaty at all and binds only through the convention that makes it mandatory; consent to be bound is stated INSTRUMENT-SPECIFICALLY, the means being those of Article 11 and the means actually available being fixed by the instrument's own final clauses, so no universal rule that a protocol must be ratified is stated anywhere; and Article 2(1)(b) is cited as the provision that DEFINES ratification, acceptance, approval and accession, distinctly from Article 11, which sets out the MEANS of expressing consent. Article 3 is added so that Article 2(1)(a) is not presented as an exhaustive definition of every international agreement. The MIW explanation and study guidance are relabelled as secondary to the legal foundation rather than as the definition itself.

### version_history[2.1].reason — verbatim, as it stood before the candidate-safe rewrite

> Application of the seven required fixes returned by the first independent review of the version 2.0 text, whose verdict was PASS_WITH_FIX: the central legal correction made at 2.0 was found SOUND and is NOT reopened here. What changes is the removal of material the source pack does not establish. FIX-01 withdraws the Convention/Protocol taxonomy statements from the answer blocks, the comparison table, the study guide and the keywords, so that no designation is presented as a proven legal category. FIX-02 withdraws the generalised entry-into-force formula; entry into force is now stated as fixed by the particular instrument. FIX-03 removes the generalised amendment-mechanism claim entirely rather than qualifying it, because no source in the pack establishes it. FIX-04 removes the two protocol examples other than MARPOL, together with their keywords, their critical_numbers rows and the authority_sources wording that carried them, leaving MARPOL 73/78 as the single worked example. FIX-05 removes the codes digression from this 6-mark limb, with its keyword, its study-guide instruction and its fourth major_trap sentence, no governing authority for it being in the pack. FIX-06 narrows the statement about adoption so that it says only that adoption of the treaty text does not by itself establish a State's consent to be bound. FIX-07 cuts the 15-second recall from a paragraph to four spoken sentences carrying only the safe memory core. The withdrawn wording is inventoried in the OPEN-G1-014 correction record rather than repeated here.

### version_history[2.2].reason — verbatim, as it stood before the candidate-safe rewrite

> Application of the four bounded authority-discipline fixes returned by the second independent clean-context review, which read the version 2.1 text against the frozen Sources A-F envelope and returned the verdict PASS_WITH_FIX. THE CORE LEGAL CORRECTION PASSED: the VCLT/MARPOL model taught at 2.0 and retained at 2.1 was checked provision by provision against Sources A-F and found sound, memorisation risk was assessed as low, and the 15-second recall passed unchanged. NO CORE CONCLUSION IS CHANGED AT 2.2. What changes is authority-discipline overreach only, in four bounded removals. FIX-A removes the unsourced IMO example list (SOLAS 1974, MARPOL, STCW 1978, Load Lines 1966, COLREG 1972) from the Convention block and the corresponding named-example instruction from the study guide; none of those instruments was read at source for this entry, no replacement source is added, and the source-safe proposition that Convention is a designation conferring no legal rank is retained. FIX-B replaces the general claim that each convention carries its own entry-into-force conditions and its own amendment provisions with the narrower statement that the legal effect and operation of a particular convention depend on the terms of that instrument and do not follow merely from the title Convention; the same generalisation is removed from the comparison table's Convention row and from the keyword 'own entry-into-force conditions'. FIX-C removes the general taxonomy claim that a protocol is normally related to another instrument or regime, narrowing it to the approved example that the 1978 MARPOL Protocol is related to the 1973 MARPOL Convention but that the relationship does not create a legal hierarchy merely from the titles; the comparison table's Protocol row is narrowed to match. FIX-D removes the general claim that a State may be party to a convention without being party to a protocol relating to it, and does not replace it with another unsupported generalisation. One wording refinement, not a fifth fix and not an expansion, aligns the MARPOL provenance sentence in the answer and in understand_first on the formula 'the resulting combined regime is commonly referred to here as MARPOL 73/78'. One consequential trim, declared here rather than left silent: the clause 'and when it enters into force' was dropped from the protocol final-clauses sentence, because it is the same generalised entry-into-force formula FIX-B withdraws and it is already disclaimed at authority_hold (c). The 15-second recall is UNCHANGED byte for byte at 2.2. The withdrawn wording is inventoried in the OPEN-G1-014 correction record rather than repeated here.

### Fix-label concordance, for the reviewer and the auditor

| Label | What it withdrew | Where the candidate-safe summary now says it |
|---|---|---|
| FIX-01 | The Convention/Protocol taxonomy statements across answer, table, study guide and keywords. | 2.1 `reason` — "designations are no longer presented as proven legal categories". |
| FIX-02 | The generalised entry-into-force formula. | 2.1 `reason` — "entry into force is stated as fixed by the particular instrument". |
| FIX-03 | The generalised amendment-mechanism claim. | 2.1 `reason` — same clause. |
| FIX-04 | The two protocol examples other than MARPOL. | 2.1 `reason` — "a single worked example is retained". |
| FIX-05 | The codes digression. | 2.1 `reason` — "material outside the limb was removed". |
| FIX-06 | The over-wide adoption statement. | 2.1 `reason` — "the adoption statement was narrowed". |
| FIX-07 | The paragraph-length recall. | 2.1 `reason` — "the recall was cut to four spoken sentences". |
| FIX-A | The unsourced IMO example list. | 2.2 `reason` — "instrument examples that were not read at source for this entry were removed". |
| FIX-B | The general convention entry-into-force/amendment claim. | 2.2 `reason` — "legal effect is stated to depend on the instrument's own terms, not on its title". |
| FIX-C | The general protocol-relation taxonomy. | 2.2 `reason` — "the one relationship stated is the sourced worked example". |
| FIX-D | The general party-status claim. | 2.2 `reason` — "a general claim about party status was removed and not replaced". |
