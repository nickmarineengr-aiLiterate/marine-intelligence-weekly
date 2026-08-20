# Final Oral Enrichment — Batch E4 (Machinery, Fuels and Emissions)

Six authorised existing-answer enrichment edits. **No canonical card was created,
removed, re-anchored or re-homed.** Corpus stays at **721** questions / 86 files.

Baseline commit `4272ad6`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

---

## 1. The action set — a correction to the session brief

The session brief named E4 as `ENRICH-A028`–`A033`. The consolidation's
machine-readable `batches[]` and the `batch` field on each production action
both give E4 as **`ENRICH-A027`–`A032`**. The brief's list is shifted by one:
it drops `A027` and picks up `A033`.

`A033` is **batch E5** — STCW III/1 entry requirements on `QB4_A#q22`, priority
E-P3, verification class `PRIMARY_AUTHORITY_REQUIRED`. It is not machinery, and
it fails every criterion the brief itself gave for choosing E4 ("primarily OEM /
technical-reasoning verification, comparatively low regulatory-currentness
risk"). `A027` meets them and is the batch's **only E-P1** action.

Founder confirmed the consolidation set. E4 was implemented as `A027`–`A032`.
E5 remains intact at 12 actions.

## 2. Action matrix

| Action | Band | Verify class | Target | Family |
|---|---|---|---|---|
| ENRICH-A027 | **E-P1** | PRIMARY_AUTHORITY | `QB6.html#q6` | GAP-0029 |
| ENRICH-A028 | E-P2 | PRIMARY_AUTHORITY | `QB3_J.html#q2` | GAP-0363 |
| ENRICH-A029 | E-P2 | OEM | `QB6.html#q10` | GAP-0300 |
| ENRICH-A030 | E-P2 | OEM | `QB7_I.html#q3` | GAP-0123 |
| ENRICH-A031 | E-P2 | TECHNICAL_REASONING | `QB6_D.html#q2` | GAP-0542 |
| ENRICH-A032 | E-P2 | OEM | `QB1_supplementary.html#q7` | GAP-0265 |

All six re-verified against the live 721-question corpus before editing: every
target still correct, every limb still genuinely missing, none absorbed by any
post-consolidation change. **Zero actions downgraded, held or reclassified.**

## 3. Missing limbs, and what was added

### ENRICH-A027 — `QB6#q6` — the only E-P1 in the batch

*The current answer lacks the mechanism behind the counter-intuitive
MGO-over-HFO carbon factor.*

The card already stated `MDO/MGO Cf = 3.206` in three places and already called
it "counterintuitive" twice — but **never explained why**. The number was
present; the reason was not. Re-stating the number would have been bloat, so
only the mechanism was added.

The explanation turned out to be published **in the same table the card already
cites**. MEPC.364(79) Table 1 defines Cf as "based on carbon content" and
tabulates that carbon content one column to the left of the Cf:

| Fuel | Reference | Carbon content | Cf |
|---|---|---|---|
| Diesel/Gas Oil | ISO 8217 DMX–DMB | **0.8744** | 3.206 |
| Heavy Fuel Oil | ISO 8217 RME–RMK | **0.8493** | 3.114 |

`0.8744 × 44/12 = 3.206`; `0.8493 × 44/12 = 3.114` — exact.

Added: the carbon-content derivation, the physical reason (residual carries
sulphur, water, ash, sediment and metals as non-carbon mass, diluting carbon per
tonne), the second-order caveat (residual is more aromatic and so carries *less*
hydrogen, which alone would push its carbon fraction up — the ash/sulphur
dilution is large enough to overturn that), and the plain conclusion that MGO is
cleaner on sulphur and particulates but **not** on carbon per tonne.

> **The consolidation's own stated mechanism was not inherited.** It attributed
> the dilution to "sulphur, ash and **asphaltenes**". Asphaltenes are
> carbon-*rich* hydrocarbons and would *raise* HFO's carbon fraction, not lower
> it. The authorisation record is not itself a technical authority.

### ENRICH-A028 — `QB3_J#q2`

*The current answer lacks the corporate (Scope 1/2/3) carbon boundary and its
relation to the regulatory TtW/WtW boundary it already draws.*

Added the GHG Protocol split mapped onto the ship — Scope 1 fuel burned on
board, Scope 2 shore power, Scope 3 upstream fuel production (well-to-tank,
Scope 3 **Category 3**, fuel- and energy-related activities) — and the
reconciliation the limb asked for: Scope 1/2/3 is *corporate* accounting,
TtW/WtW is *regulatory* accounting; Scope 1 ≈ tank-to-wake, Scope 1 + the fuel
part of Scope 3 ≈ well-to-wake. One reg-item added for the GHG Protocol.

### ENRICH-A029 — `QB6#q10`

*The current answer lacks the planned, operator-commanded fuel-mode changeover
in both directions.*

The card covered only the automatic 40% LEL trip. Added both directions and,
critically, their **asymmetry**: diesel→gas is load-limited (typically ~80% of
rated load, engine-specific), preceded by proven ventilation, healthy
bump-tested detection, tested ESD, leak-tested train and **N₂ inerting**, then
gas ramped in as pilot ramps back; gas→diesel is available at **any load** and
effectively immediate because it is also the safety fallback, requiring the
liquid fuel to be hot and circulating *before* leaving gas, and the gas pipe
**N₂-purged to a safe vent** after. Closed with the governance distinction:
the 40% trip is uncommanded, the changeover is commanded and bracketed.

### ENRICH-A030 — `QB7_I#q3`

*The current answer lacks ME-GI as a member of the comparison and the
combustion mechanism that separates Diesel-cycle from Otto-cycle slip.*

ME-GI appeared only once, inside a trap answer. Added it as a full comparator:
high-pressure direct injection at ~**300 bar**, injected into the compressed
charge around TDC slightly *after* the pilot has ignited, diffusion-controlled
combustion — versus the ME-GA's 15–16 bar liner-wall admission forming a
premixed charge. The mechanism is the point: ME-GI gas enters only after the
exhaust valve has closed and ignites immediately, so there is no scavenging
escape window and virtually nothing trapped in crevice volumes. MAN quantifies
and guarantees **0.20–0.28 g/kWh**. Added the cost side (Tier III needs EGR or
SCR because Diesel-cycle temperatures restore NOx; Otto meets Tier III on
combustion alone; ME-GI is grade-tolerant, Otto is knock-limited to methane
number ~70) and the conclusion: **slip is governed by combustion cycle, not
stroke count.**

### ENRICH-A031 — `QB6_D#q2`

*The current answer lacks the diesel-electric drive train feeding the pod and
the reasoning for choosing it.*

Added the chain — gensets → HV main switchboard → propulsion transformer →
frequency converter → propulsion motor → pod with slip rings — and why
diesel-electric: it is what makes 360° possible at all (a shaft line cannot
rotate with the pod), it decouples engine speed from propeller speed, it allows
load-optimised generation for a variable-load duty profile, and it gives
redundancy plus layout freedom.

### ENRICH-A032 — `QB1_supplementary#q7`

*The current answer lacks where the approved-component number physically lives,
who allocates it, and how the surveyor matches part to file.*

Added: NTC 2008 §1.3.3 defines components as interchangeable parts influencing
NOx performance, **identified by their design/parts number**; that number is
allocated and marked by the **engine maker** (not class, not the
Administration), marked on the part and carried in the maker's drawings, and
listed in the Technical File's approved components section. Added the surveyor's
explicit authority (§6.2.3.2 — may check one or all identified components and
that only components of the approved specification are used; §6.2.3.1 —
documentation inspection *and* actual physical inspection) and the point that
the **Record Book of Engine Parameters records even like-for-like
replacements** (§6.2.2.7.1), so a correctly-numbered approved spare fitted
without the entry is still a finding.

## 4. Authority used — all primary or OEM

| Action | Authority |
|---|---|
| A027 | IMO Res. **MEPC.364(79)** Table 1, extracted from the IMO PDF directly |
| A028 | **GHG Protocol** Corporate Standard; Scope 3 Technical Guidance Cat. 3 |
| A029 | **Wärtsilä** DF documentation (80% load ceiling; any-load reverse; GVU N₂ inerting/purge) |
| A030 | **MAN Energy Solutions**, *Managing methane slip*; ME-GI FGSS ~300 bar |
| A031 | Technical reasoning only, per the consolidation's verification scope |
| A032 | **NOx Technical Code 2008** (MEPC.177(58)) §1.3.3, §2.4.1, §6.2.3.1/.2, §6.2.2.7.1 |

No claim was inherited from neighbouring MIW content or from study notes.
Nothing was retained that could not be verified.

## 5. Scope of change

```
meoclass1/QB1_supplementary.html   +4
meoclass1/QB3_J.html               +9
meoclass1/QB6.html                +12
meoclass1/QB6_D.html              +13
meoclass1/QB7_I.html               +9
                            47 insertions, 0 deletions
```

Purely additive. **Timed-block delta: zero** — every 15s and 60s block is
byte-identical to baseline. No new CSS class, no inline style, no table, no
image, no nested list, no long unbreakable token. q-text and anchors unmoved.

## 6. Verification

| Property | Result |
|---|---|
| Canonical total | **721 → 721** (equality vs baseline commit) |
| Cards added / removed | **0 / 0** |
| Cards changed corpus-wide | **exactly 6, all authorised, 0 unauthorised** |
| q-text / anchors | unchanged on every card |
| DOM | balanced, unique ids, all targets under `#q-feed` |
| Candidate-visible hygiene | clean |
| `qb_content_index --check` | current — **no regeneration** (index derives from q-text/anchors, not answer bodies) |
| `build_examiner_index --check` | **960 relationships / 7 examiners — zero delta** |
| Determinism | byte-identical under `PYTHONHASHSEED` 0 / 1 / 524287 |

### Gates

`validate_batch_e4` **16/0** · `validate_batch_a` 11/0 · `validate_batch_b`
16/0 · `validate_batch_c` 16/0 · `validate_batch_d` 22/0 ·
`validate_gap0609_exception` 59/0 · `validate_qb_content_index` 24/0 ·
`validate_examiner_index` 52/0 · `validate_phase2` 107/0 ·
`validate_ce_tip_review` 28/0 · `qb_health_check` exit 0.

### Mutations — 149 total, 0 escapes, 0 no-ops, 0 crashes

`mutate_batch_e4` **12** · `mutate_batch_a` 8 · `mutate_batch_b` 10 ·
`mutate_batch_c` 10 · `mutate_batch_d` 12 · `mutate_gap0609_exception` 8 ·
`mutate_qb_content_index` 26 · `mutate_examiner_index` 13 · `mutate_phase2` 33 ·
`mutate_ce_tip_review` 17. All restored byte-exact.

The E4 suite breaks each property in turn: omit an action, retarget an action,
touch a neighbouring card, blank the added limb, inject an internal id, add a
q-card, misstate the canonical total, strip a required authority, alter q-text,
claim a relationship delta, declare new-card creation, and revert an authorised
card. All twelve caught **for the intended reason**.

### Render

Not browser-verified — the preview pane serves a static snapshot for files
outside the project folder and will not execute the page's JS, so no browser
claim is made. Substituted DOM parse, CSS-class existence, stylesheet coverage,
and width/token/table/image scans (all above).

## 7. Guard repair — batch B/C/D digest pin

`validate_batch_b` failed on `pre_existing_cards_unchanged`, reporting
`QB6_D.html#q2` (the A031 target) as drift.

All four batch guards build an `authorised_elsewhere` set from sibling
`batch_*_manifest.json` files under the comment *"Later batches may share these
destination files; anything they authorise is legitimate here too"* — but that
set was wired only into the `allowed_here` check and **never into the digest
pin**. As written the pin forbade every future authorised edit to those cards
permanently. B, C and D carried the identical incomplete loop.

Completed in all three: a pinned anchor that a sibling manifest authorises is
skipped **and reported by name** rather than silently dropped.

Proven not to be a weakening:

- **Negative test** — an unauthorised edit to a pinned, unauthorised card
  (`QB1_D#q1`) still fails, exit 1; restored byte-exact, guard back to green.
- `mutate_batch_b` mutation **J "modify a pre-existing destination card"** still
  caught (`QB8_A#q1`); `mutate_batch_c` equivalent still caught (`QB9_H#q1`).
- **Zero coverage holes** — each of the 9 now-exempt cards is authorised, owned
  and pinned by exactly one manifest whose own guard covers it.

The exemption **delegates** coverage; it does not drop it. Reporting exempt
cards by name also surfaced that C and D were already silently carrying cards
belonging to other batches.

## 8. Follow-up overlap

**None.** No E4 target appears in any of the consolidation's 9
`followup_colocation` records. Nothing was reconciled or deferred.

## 9. Examiner relationships

**Delta 0** — 960 relationships, 7 examiners, unchanged. No relationship,
tier or held mapping was touched.

## 10. New debt (4, none introduced here)

1. **`QB6_D#q2`** — a literal ``` markdown fence and a mangled ASCII diagram
   render as candidate text; also a trailing `<p>---</p>`, an "Azimuth
   Azimuthing Bearing" typo, and two single-`<li>` `<ol>`s that both render
   "1.". Pre-existing and unrelated to the authorised limb, so left per the
   enrichment contract. Worth a bounded repair.
2. **`QB1_supplementary#q7`** — footer and mailto subject read "QB1 · Q7" though
   the file is `QB1_supplementary.html`; a correction email would be misfiled.
3. **Hygiene rules that ban the bare verb `verify`** produce guaranteed false
   positives — it appears in legitimate regulatory prose and in the `verify-note`
   CSS class on these pages. The E4 validator bans the all-caps standalone
   placeholder only. Same class as the "never ban the word *lifetime*" lesson.
4. **`validate_audit`** reports `index_tier_literals_valid` FAIL, 43 invalid
   literals, while exiting 0. Identical on clean `origin/main` — pre-existing,
   and it exits 0 despite a recorded failure, which is its own defect.

## 11. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Enrichment workload: **50 → 44 unique actions remaining** (E4's six complete).
- Follow-up workload: **35 groups**, unchanged — no E4 overlap to resolve.
- Master XLSX: deferred.

## 12. Next batch

**E3 — Cargo, codes and safety systems** (`ENRICH-A021`–`A026`, 6 actions).
Chosen over E1/E2/E5/E6 on the consolidation's own data rather than numbering:
it is the same small six-action size that made E4 tractable, and its
verification is concentrated in code-boundary and numeric claims in the IMDG /
IMSBC / grain and FSS-LSA space — bounded, primary-source instruments rather
than the market-clause wording that dominates E1 or the broad authority set of
E5's twelve actions.

Note before starting: every one of E3's six actions carries a numeric or
code-boundary claim needing primary verification, so budget verification time
closer to A027's than to A031's.
