# Known Traps & Standing Corrections — Past Written Papers

Same purpose and format as `meoclass1/known_traps.md`: verified-correct facts that have
already been drafted wrong at least once in this series. Every new paper is checked
against this list before HTML is built — not recalled from memory.

Each entry carries a `GREP:` line. `known_traps_check.py` auto-scans only entries whose
`GREP:` gives a phrase that is unambiguous out of context and therefore safe to flag
wherever it appears. Where the wrong form uses words that are also legitimate in other
contexts, the entry is marked `GREP: SKIP` and stays manual-review-only — the checker
handles those, where it can, as a structural check against the spec instead.

Do not add brittle regex policing of nuanced legal prose. If a rule needs judgement,
mark it SKIP and leave it to the verification pass.

---

### 1. Bunkers Convention — liability is NOT confined to the registered owner
Article 1(3) defines "ship-owner" as the owner, **including the registered owner,
bareboat charterer, manager and operator**. Article 3 makes them liable jointly and
severally. Article 7(1) separately puts the **compulsory insurance** duty on the
**registered owner** alone, for ships over 1,000 GT. Liability and the insurance
obligation attach to different persons. Found in EM2607 Q2 v0.1 (red-team RT-07).
GREP: strict liability on the registered owner

### 2. Bunkers Convention — same error, other phrasings
GREP: Bunkers Convention imposes strict liability on the registered owner

### 3. CLC applicability must not be stated absolutely
CLC 1992 Art I(5) covers persistent oil "whether carried on board a ship as cargo **or in
the bunkers of such a ship**", and Bunkers Convention Art 4(1) excludes itself where the
damage is CLC pollution damage. So a bunker spill from a CLC ship IS CLC damage. Whether
CLC applies turns on two facts: is she a CLC ship, and is the oil persistent. Found in
EM2607 Q2 v0.1 (red-team RT-08).
GREP: CLC 1992 does not apply

### 4. CLC — same error, other phrasing
GREP: CLC does not apply to a bunker spill

### 5. Casualty Investigation Code is not engaged by every pollution incident
A **mandatory** marine safety investigation under Part II chapter 6 is required only for a
**very serious marine casualty** — total loss of the ship, a death, or severe damage to
the environment (§2.22). Marine casualties short of that, and marine incidents, fall under
Part III **recommended practice** (chapter 17). The environmental limb of §2.9.7 also
requires damage "brought about by the damage of a ship". A bunker overflow from an intact
ship is usually a **marine incident**. Found in EM2607 Q2 v0.1 (red-team RT-06).
GREP: SKIP

### 6. Iron ore pellets are not iron ore fines — and the split is not a clean binary
IRON ORE, IRON ORE FINES, IRON ORE PELLETS and DIRECT REDUCED IRON (B) are separate IMSBC
schedules in different Groups, and "pellets" appears in the DRI (B) schedule name too.
The fines schedule itself carries qualifying criteria (goethite content, particle size
distribution) under which fines may be carried as Group C. The declared Bulk Cargo
Shipping Name and its individual schedule govern — never the commodity name. Found in
EM2607 Q1 v0.1 (red-team RT-03).
GREP: SKIP

### 7. Do not state a TML for a Group C cargo
TML is a Group A concept. A Group C cargo does not have one; if a TML is being offered for
your cargo, question the classification rather than accept the figure.
GREP: SKIP

### 8. Indian marine insurance answers must cite the Marine Insurance Act, 1963
The examination is Indian. The governing statute is the **Marine Insurance Act, 1963** —
s.19 utmost good faith, s.20 disclosure, s.66 general average loss. The UK Marine
Insurance Act 1906 is its model but is **not** the operative statute, and the UK Insurance
Act 2015 reform of the avoidance remedy does **not** apply to Indian law. Note that
`meoclass1/QB9_C.html` attributes the principles to the 1906 Act — do not lift from it.
GREP: SKIP

### 9. Ammonia interim guidance is NOT a mandatory IGF Code amendment
MSC.1/Circ.1687 (26 February 2025), *Interim Guidelines for the Safety of Ships using
Ammonia as Fuel*, approved at MSC 109, is **non-mandatory**. The IGF Code's prescriptive
provisions were written for natural gas; approval proceeds through the alternative design
route in SOLAS II-1/55. Do not describe the interim guidelines as IGF Code text.
GREP: mandatory IGF Code requirements for ammonia

### 10. Ammonia is not a zero-emission fuel
No carbon in the molecule means no direct CO2. It does not mean zero emissions: N2O and
ammonia slip are emissions, and lifecycle GHG depends on the production pathway.
GREP: SKIP
NOTE: the phrase legitimately appears in study notes where the answer refutes it
("Is ammonia a zero-emission fuel? No."), so it fails this file's own
unambiguous-out-of-context rule. Structural check instead.

### 11. Merchant Shipping Act 2025 claims are time-sensitive
Act No. 24 of 2025, assent 18 August 2025, in force 15 March 2026 by S.O. 1244(E) of
10 March 2026. Repeals the MS Act 1958 (saving Part XIV, not s.411A) and the Coasting
Vessels Act 1838. The **scope** of commencement and any provision-level citation must
carry a re-verification flag until confirmed against the Gazette. Never invent section
numbers of the 2025 Act.
GREP: SKIP

### 12. HATC coaching notes are never a verification source
`Notes-for-written-answers/` is HATC material whose own footer states that certain
statements and figures were **intentionally made wrong**. Discovery and question-scope
evidence only. Never authority, never verification, never reproduced.
GREP: SKIP
NOTE: naming HATC in order to record that it was NOT used is correct and expected,
so a bare phrase match is wrong. Enforced structurally: no HATC reference may
appear in a question's `sources` list.

### 13. Source provenance must not be overstated
The held paper PDFs are aggregator-hosted copies, not official publications. Do not claim
an official DG Shipping or MMD source unless an independently authoritative copy has
actually been compared.
GREP: official DG Shipping PDF

### 14. Aggregator branding must never reach output
GREP: dieselship
SCOPE: html

### 15. Stale build-state terminology
Once a question's status moves on, "Pilot Built" must not survive in generated HTML.
Generated pages are rebuilt from the spec, so this only appears if someone hand-edited
output — which is itself the error.
GREP: Pilot Built
