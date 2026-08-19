"""Hand adjudications for the final Oral gap-family review.

One entry per GENUINE_GAP / NOTES_COVERED_GAP family. Every decision was made
by reading the ASK, the current live QB **answer bodies** (not question titles)
and the section-level Oral Notes evidence - in that order. Question-title
matching alone was already proved insufficient: the 788 matcher never found the
dedicated subrogation, BMP5, ERRM, mentoring or appraisal cards, because their
stems share almost no vocabulary with the examiner's wording.

Tuple: (decision, target, reason)
  target - ENRICH / MERGE / ALREADY_COVERED / FOLLOWUP: the canonical question
           id (or gap id, for MERGE) that owns the ask.
         - NOTES_TO_QB_PROMOTION: the Notes unit holding the material,
           written "file#anchor".
         - NEW_CANONICAL_QA: the recommended QB home file.

MATERIAL_PARTIAL families deliberately carry no entry. The matcher already
established that an existing answer covers part of the ask, so only the
materiality of the missing limb is open, and that is decided by rule in
adjudicate_final_gaps.py rather than one family at a time.
"""

NEW = "NEW_CANONICAL_QA"
ENRICH = "ENRICH_EXISTING_QB"
NOTES = "NOTES_TO_QB_PROMOTION"
FOLLOWUP = "FOLLOWUP_ONLY"
MERGE = "MERGE_WITH_EXISTING_FAMILY"
COVERED = "ALREADY_COVERED"
RELATIONSHIP = "RELATIONSHIP_ONLY"
AMBIG = "HUMAN_REVIEW_REQUIRED"
DEFER = "DEFER_LOW_VALUE"
NOT_A_GAP = "NOT_A_GAP"

HIGH, MED = "READY_HIGH_CONFIDENCE", "REVIEW_MEDIUM_CONFIDENCE"

# Confidence applies to NEW_CANONICAL_QA only. Only HIGH enters the headline
# count; MED items are real absences whose scope or value is still open.
CONFIDENCE = {
    "GAP-0080": HIGH, "GAP-0083": HIGH, "GAP-0113": HIGH, "GAP-0120": HIGH,
    "GAP-0124": HIGH, "GAP-0128": HIGH, "GAP-0159": HIGH, "GAP-0225": HIGH,
    "GAP-0262": HIGH, "GAP-0365": HIGH, "GAP-0376": HIGH, "GAP-0378": HIGH,
    "GAP-0412": HIGH, "GAP-0415": HIGH, "GAP-0418": HIGH, "GAP-0442": HIGH,
    "GAP-0465": HIGH, "GAP-0478": HIGH, "GAP-0558": HIGH, "GAP-0562": HIGH,
    "GAP-0619": HIGH, "GAP-0728": HIGH,
    "GAP-0239": MED, "GAP-0255": MED, "GAP-0354": MED, "GAP-0443": MED,
    "GAP-0516": MED, "GAP-0553": MED, "GAP-0672": MED,
}

# Batching for approved NEW cards. Transparent reasons only, no numeric score.
BATCH = {
    # P1-A - a current regulation, or a statutory/safety duty a CE is expected
    # to hold outright and cannot bluff.
    "GAP-0415": "P1-A", "GAP-0262": "P1-A", "GAP-0465": "P1-A",
    "GAP-0378": "P1-A", "GAP-0478": "P1-A", "GAP-0225": "P1-A",
    "GAP-0080": "P1-A", "GAP-0619": "P1-A",
    # P1-B - solid engineering or commercial asks, lower recurrence.
    "GAP-0120": "P1-B", "GAP-0124": "P1-B", "GAP-0128": "P1-B",
    "GAP-0083": "P1-B", "GAP-0365": "P1-B", "GAP-0412": "P1-B",
    "GAP-0418": "P1-B", "GAP-0442": "P1-B", "GAP-0113": "P1-B",
    "GAP-0728": "P1-B",
    # P2 - useful long tail.
    "GAP-0159": "P2", "GAP-0376": "P2", "GAP-0558": "P2", "GAP-0562": "P2",
}

DECISIONS = {
    # ---- NEW ------------------------------------------------------------
    "GAP-0080": (NEW, "QB1_C", "Post-renewal weld verification as CE. NDT vocabulary exists corpus-wide only inside the tail-shaft survey and the watertight/weathertight test card; no answer walks a CE through accepting a side-shell renewal."),
    "GAP-0083": (NEW, "QB8_A", "P/V breaker and mast riser appear once each across 688 answers, both in passing. Construction, position and working of the tank-venting safety chain has no home."),
    "GAP-0113": (NEW, "QB1_D", "Fresh Water Allowance returns zero hits corpus-wide. The Loadline survey card lists documents; it never derives FWA or dock water allowance."),
    "GAP-0120": (NEW, "QB7_C", "Miller and Atkinson cycles return zero hits corpus-wide. The ME-GA card names the Otto cycle but never contrasts the cycles or draws them."),
    "GAP-0124": (NEW, "QB2_H", "Flammability diagram appears only as an incidental phrase. Why the air line slopes rather than standing vertical at 21 percent oxygen is a distinct mechanism ask."),
    "GAP-0128": (NEW, "QB7_C", "Adaptive cylinder-oil control and feed rate against fuel sulphur content is absent. The lube-oil-analysis card covers analysis, not dosing strategy."),
    "GAP-0159": (NEW, "QB9_H", "Capital, voyage and operating cost decomposition has no card. The liner-consortium and general-average cards use the words incidentally."),
    "GAP-0225": (NEW, "QB2_E", "Hydrostatic release and float-free arrangement appear once, inside the SEQ survey checklist. Why a forward liferaft differs and may be carried without an HRU is unanswered."),
    "GAP-0262": (NEW, "QB6_D", "Onboard demonstration of NOx compliance - direct measurement, simplified measurement, parameter check - appears once corpus-wide. The SCR and EGR cards cover reduction, not verification."),
    "GAP-0365": (NEW, "QB6_D", "Cavitation is named in passing beside propeller slip. Mechanism, NPSH in a centrifugal pump and propeller cavitation types have no answer."),
    "GAP-0376": (NEW, "QB4_G", "Stowaway handling - attempted stowaway, refusal of landing, who bears the cost, documentation. Six passing mentions, all inside P&I cards. Merges GAP-0379."),
    "GAP-0378": (NEW, "QB3_B", "SOLAS II-1/29 steering-gear requirements and the pre-departure test routine return three weak hits. A CE is expected to hold this outright."),
    "GAP-0412": (NEW, "QB7_D", "Wake-equalising duct and pre-swirl energy-saving devices return one incidental hit. The owner-payback limb is the examiner's real demand."),
    "GAP-0415": (NEW, "QB10_B", "MASS: the MASS Code is named only inside the amendments-overview card. Degrees of autonomy, the regulatory scoping exercise and IMO instrument readiness have no answer."),
    "GAP-0418": (NEW, "QB6_H", "Electric shock physiology - V=IR, let-go current, ventricular fibrillation threshold - returns one weak hit. The HV card covers isolation, not the human injury mechanism."),
    "GAP-0442": (NEW, "QB5_A", "Behaviour-based safety returns zero hits corpus-wide despite a large human-element section."),
    "GAP-0465": (NEW, "QB3_F", "Bunker ordering for quantity and quality, dispute resolution, the sample set and retention periods. Bunker-delivery-note vocabulary is scattered over 29 answers with no owning card."),
    "GAP-0478": (NEW, "QB4_G", "SAR Convention, COSPAS-SARSAT and INDSAR return zero hits corpus-wide."),
    "GAP-0558": (NEW, "QB5_I", "Owner-case comparison of a motor ship against a steam turbine ship. The engine-technology card covers retrofits, not the propulsion-plant business case."),
    "GAP-0562": (NEW, "QB9_H", "Ship broker returns zero hits corpus-wide; the chartering cards never define the intermediary."),
    "GAP-0619": (NEW, "QB9_B", "Medical evacuation and voyage diversion. Medevac, telemedical and ship hospital return three weak hits. Merges GAP-0624 (hospital arrangements, who bears the cost)."),
    "GAP-0728": (NEW, "QB1_D", "Type B-60 and B-100 ships return zero hits corpus-wide; the freeboard-reduction regime is unanswered."),
    "GAP-0239": (NEW, "QB9_A", "Warranty against guarantee in a marine-insurance sense is absent, but the insurance-principles card is adjacent and the scope of a separate answer is unclear."),
    "GAP-0255": (NEW, "QB7_B", "Shale gas returns zero hits. Relevance to a MEO Class I oral is arguable - it arose as an examiner tangent."),
    "GAP-0354": (NEW, "QB10_A", "VALEMAX - one incidental hit under high-density cargo. The meaning is clear (Vale VLOC), but a one-token prompt gives no scope."),
    "GAP-0443": (NEW, "QB5_A", "Personality development onboard returns six weak hits across leadership cards; whether this warrants a card or a leadership-card limb is a judgement call."),
    "GAP-0516": (NEW, "QB4_G", "Drydock budgeting and job prioritisation. Merges GAP-0517 and GAP-0519. Budget vocabulary is scattered; the manpower card is adjacent but not the same ask."),
    "GAP-0553": (NEW, "QB6_F", "The UN telecommunications body (ITU) is reached only through the MMSI and call-sign cards; a standalone answer may be over-scoped for one terse ask."),
    "GAP-0672": (NEW, "QB1_E", "Pre-repair checks before a shore workshop touches a lifeboat davit. Davit appears six times, none about controlling third-party repair."),

    # ---- NOTES PROMOTION -------------------------------------------------
    "GAP-0180": (NOTES, "miw-notes-mgmt-p9.html#topic-40", "Notes carry a dedicated 'Intervention Convention 1969 & OPRC 1990' section; the QB holds zero hits. Absorbs GAP-0241 as the dispute-settlement limb."),
    "GAP-0218": (NOTES, "simon-notes-p1.html#n22", "Notes section 'Free-Fall Lifeboat - Requirements' is complete; the QB mentions freefall only inside the amendments overview."),
    "GAP-0231": (NOTES, "miw-notes-mgmt-p16.html#topic-p16-6", "Bonjean returns zero QB hits; the Notes stability section carries the curve. Governed verdict already NOTES_COMPLETE_SUPPORT."),
    "GAP-0334": (NOTES, "miw-notes-mgmt-p13.html#topic-p13-3", "Great circle returns zero QB hits; the Notes carry the passage-planning material. Governed verdict NOTES_COMPLETE_SUPPORT."),
    "GAP-0342": (NOTES, "miw-notes-mgmt-p10.html#topic-44", "Notes section 'Hull Corrosion Dynamics: SACP, ICCP and Marine Growth' holds the galvanic series and anode material; the QB carries it only inside the in-water survey card."),
    "GAP-0355": (NOTES, "simon-notes-p2.html#n10", "Notes section 'Caustic Embrittlement in Boilers' is complete; every QB embrittlement hit is a hydrogen-fuel card."),
    "GAP-0534": (NOTES, "simon-notes-p4.html#n22", "Notes section 'SID - Seafarers Identity Document' answers the CDC-against-SID ask directly; the QB holds one unrelated hit."),
    "GAP-0621": (NOTES, "miw-notes-mgmt-p19.html#topic-p19-4", "Incoterms return zero QB hits; the Notes maritime-economics section carries them. Governed verdict NOTES_COMPLETE_SUPPORT."),
    "GAP-0065": (NOTES, "simon-notes-p8.html#n8", "Notes section 'IMO vs USCG BWTS Requirements' plus the AMS material is complete. Promote rather than enrich the new QB3_J#q6, which is scoped to UV technology."),
    "GAP-0151": (NOTES, "miw-notes-mgmt-p8.html#topic-36", "Notes carry a dedicated P&I Blue Card section. COFR is the US analogue and belongs with it; every QB blue-card hit is a CLC or Bunker Convention card."),

    # ---- ALREADY COVERED (answer bodies overturn the title match) --------
    "GAP-0115": (COVERED, "QB1_supplementary#q2", "The IS Code criteria card states all numerical values including the 0.055 m.rad area the examiner was driving at."),
    "GAP-0131": (COVERED, "QB7_I#q2", "ME-LGI and methanol vocabulary appears 55 times in this card and 30 times in QB6#q11."),
    "GAP-0141": (COVERED, "QB5_I#q3", "The major-accident contact chain and the shore emergency response contact are answered here."),
    "GAP-0148": (COVERED, "QB9_G#q3", "Accession and accede appear nine times in the convention-adoption card."),
    "GAP-0191": (COVERED, "QB1_A#q30", "The MEPC 84 outcomes card plus QB6#q7 carry the GHG strategy checkpoints."),
    "GAP-0195": (COVERED, "QB5_B#q7", "Fitness for duty and watchkeeping qualification are answered across QB5_B#q7 and QB4_B#q12."),
    "GAP-0205": (COVERED, "QB4_B#q12", "Competent against skilled labour under STCW answers the junior-engineer-to-OICW competency ask."),
    "GAP-0209": (COVERED, "QB1_F#q2", "All MARPOL-related documents for the vessel type are enumerated here."),
    "GAP-0216": (COVERED, "QB1_A#q31", "The new BWM card answers at 0.80 answer coverage; which BWMS needs most CE attention is a limb of it."),
    "GAP-0235": (COVERED, "QB1_B#q20", "Two dedicated subrogation cards exist - QB1_B#q20 and QB1_A#q28, 27 and 25 mentions. The 788 matcher missed both on title vocabulary."),
    "GAP-0243": (COVERED, "QB9_A#q1", "P&I against H&M is the explicit subject of this card."),
    "GAP-0254": (COVERED, "QB9_E#q6", "Two Blue Economy cards exist - QB9_E#q6 and QB9_E#q10. Overrides the NOTES_STRONG verdict: the QB already asks it."),
    "GAP-0307": (COVERED, "QB1_B#q8", "The MLC and RPSL linkage is the explicit subject of this card."),
    "GAP-0309": (COVERED, "QB4_E#q15", "Cyber security management card, 26 mentions, plus QB6_H#q1."),
    "GAP-0329": (COVERED, "QB4_B#q16", "Three dedicated BMP5 cards exist - QB4_B#q16, QB4_H#q2 and QB4_H#q11."),
    "GAP-0337": (COVERED, "QB1_A#q31", "Currentness: the P0 BWM card answers G7/G8/G9 at 1.00 question and answer coverage. This was a genuine gap until 2026-08-19."),
    "GAP-0352": (COVERED, "QB1_supplementary#q7", "NOx tiers and limit values are carried by the NOx Technical File card and by QB6_D#q1 and q3. Overrides NOTES_COMPLETE_SUPPORT."),
    "GAP-0408": (COVERED, "QB7_I#q4", "Ammonia as the chosen latest technology is answered here (32 mentions) and in QB7_D#q6."),
    "GAP-0416": (COVERED, "QB5_B#q6", "The fatigue causes and mitigation card (42 mentions) covers rough weather, distance from home and heat."),
    "GAP-0420": (COVERED, "QB5_A#q2", "Engine Room Resource Management has a dedicated card, plus QB5_C_B#q6."),
    "GAP-0425": (COVERED, "QB5_D#q3", "Currentness: the P0 harassment and bullying card answers this in full."),
    "GAP-0426": (COVERED, "QB5_A#q8", "The decision-making tools card, 20 mentions, plus QB5_D#q1."),
    "GAP-0449": (COVERED, "QB7_I#q2", "Currentness: ME-GI against ME-GA differences are the subject of QB7_I#q2 and QB7_I#q3."),
    "GAP-0460": (COVERED, "QB5_A#q13", "Dedicated junior-engineer appraisal card, 43 mentions, plus QB9_H#q5."),
    "GAP-0463": (COVERED, "QB5_A#q15", "Dedicated mentoring card, 51 mentions, plus QB5_C_B#q1 which contrasts it with training."),
    "GAP-0495": (COVERED, "QB3_D#q1", "The HKC recycling sequence, IRRC, SRP and IHM are answered across QB3_D#q1 and QB3_H#q5."),
    "GAP-0496": (COVERED, "QB3_D#q1", "The Indian recycling authority and the Recycling of Ships Act 2019 are answered in QB3_G#q3 and QB3_D#q1."),
    "GAP-0502": (COVERED, "QB9_H#q11", "Casualty definitions under the MS Act, plus the Casualty Investigation Code card QB1_A#q24."),
    "GAP-0510": (COVERED, "QB4_C#q12", "NC against MNC (QB4_C#q10) and additional verification under ISM (QB4_C#q12) answer the PSC-deficiency route."),
    "GAP-0536": (COVERED, "QB9_A#q5", "Admiralty law, maritime liens and Indian jurisdiction, 34 mentions, plus QB1_A#q7."),
    "GAP-0540": (COVERED, "QB9_E#q1", "The TMSA card plus QB4_G#q9 carry SIRE, TMSA and the grading system."),
    "GAP-0547": (COVERED, "QB3_A#q13", "Ballast tank inspection is answered twice - QB3_A#q13 and QB3_B#q3 are a live duplicate pair, logged separately as duplicate-home debt."),
    "GAP-0565": (COVERED, "QB5_A#q11", "The risk assessment card plus QB5_A#q10 carry the hazard, risk, incident and casualty definitions."),
    "GAP-0572": (COVERED, "QB1_I#q4", "HSSC appears across 31 answers including the anniversary-date and survey-type cards."),
    "GAP-0576": (COVERED, "QB3_B#q11", "Annual, intermediate and renewal survey requirements, 27 mentions."),
    "GAP-0590": (COVERED, "QB1_supplementary#q4", "The CMS scope card plus QB1_F#q14 and QB1_G#q40 answer why CSM is done and who decides. Overrides NOTES_STRONG_SUPPORT."),
    "GAP-0595": (COVERED, "QB2_B#q7", "The liner / NVOCC / VOCC model card; tramp is the residual limb only."),
    "GAP-0599": (COVERED, "QB2_C#q4", "Water mist lance and monitor are answered by QB2_C#q4 and QB2_F#q5 - a live duplicate pair, logged separately as duplicate-home debt."),
    "GAP-0601": (COVERED, "QB8_B#q2", "The CSC container test, plate contents and inspection scheme card."),
    "GAP-0604": (COVERED, "QB9_A#q1", "Why H&M is taken and how it differs from P&I is the subject of this card."),
    "GAP-0629": (COVERED, "QB7_A#q3", "The EU ETS allowance (EUA) is answered here, 27 mentions, and in QB6#q14."),
    "GAP-0632": (COVERED, "QB6#q2", "CII, AER and the rating bands are answered here, 52 mentions, and in QB6_E#q3."),
    "GAP-0653": (COVERED, "QB3_A#q17", "The class quarterly listing and survey status card is exactly the on-joining ask."),
    "GAP-0689": (COVERED, "QB3_J#q6", "Currentness: the P0 BWTS card answers the USCG type-approval alternative (AMS) at 0.77 answer coverage."),
    "GAP-0692": (COVERED, "QB4_E#q14", "Safe manning across conventions is answered by QB4_E#q14 and QB4_J#q1."),
    "GAP-0708": (COVERED, "QB3_F#q4", "The Annex V record-book card enumerates what may not be incinerated. Overrides NOTES_COMPLETE_SUPPORT."),

    # ---- ENRICH ----------------------------------------------------------
    "GAP-0089": (ENRICH, "QB2_H#q1", "The FSS/FTP card holds A-60 but never contrasts an A class division with an A-60 division."),
    "GAP-0112": (ENRICH, "QB4_E#q3", "MLC accommodation is covered; sill and coaming heights and berth dimensions are the missing numeric limb."),
    "GAP-0123": (ENRICH, "QB7_I#q3", "How combustion proceeds in the ME-GA relative to the flammability envelope is a limb of the methane-slip comparison card."),
    "GAP-0144": (ENRICH, "QB4_I#q4", "The III Code card carries IMSAS; India's audit status and who conducts the audit are the missing limbs."),
    "GAP-0157": (ENRICH, "QB9_H#q9", "The Contract of Affreightment card exists; market-risk allocation is the missing limb."),
    "GAP-0165": (ENRICH, "QB9_G#q3", "Rules against regulations against conventions belongs as a definitional limb of the instrument-adoption card. Absorbs GAP-0485."),
    "GAP-0196": (ENRICH, "QB4_H#q7", "The CoC against CoP card exists; issuance criteria and the DC route are the missing limbs."),
    "GAP-0206": (ENRICH, "QB5_A#q16", "The TEAP card exists; the III/16 qualifying sea-service limb is missing."),
    "GAP-0207": (ENRICH, "QB4_A#q22", "The P0 STCW progression card is the natural home for the III/1 750 kW supervised sea-service limb."),
    "GAP-0220": (ENRICH, "QB2_A#q7", "The Li-ion fire card exists; AVD foam composition and application are the missing limb. Merges GAP-0223 (alternative chemistries, plasma)."),
    "GAP-0222": (ENRICH, "QB2_I#q4", "The CO2 pressure-testing card exists; the weighing method and the leak-alarm pressure are the missing limbs."),
    "GAP-0232": (ENRICH, "QB2_G#q1", "The timber deck cargo card exists; the 33 percent and reckoning-point numbers are the missing limb."),
    "GAP-0234": (ENRICH, "QB1_B#q1", "The HNS card names the SDR; what drives the SDR basket and its revision cycle is missing."),
    "GAP-0237": (ENRICH, "QB1_A#q9", "The General Average card names the average adjuster; the qualification and appointment limb is missing."),
    "GAP-0265": (ENRICH, "QB1_supplementary#q7", "The NOx Technical File card exists; component ID location on the liner and who issues it are missing."),
    "GAP-0270": (ENRICH, "QB2_B#q2", "The container securing card exists; the tier-height limit and its bay-plan derivation are missing."),
    "GAP-0300": (ENRICH, "QB6#q10", "The P0 dual and tri-fuel card is the home for the gas-mode changeover procedure limb."),
    "GAP-0332": (ENRICH, "QB9_D#q6", "The MS Act and RPSL card exists; the section 95 Seamen's Employment Office citation is the missing limb."),
    "GAP-0363": (ENRICH, "QB3_J#q2", "The carbon-footprint card exists; the Scope 1/2/3 decomposition is the missing limb."),
    "GAP-0377": (ENRICH, "QB5_D#q3", "The P0 conflict card is the home for the counselling, disciplinary action and training escalation ladder."),
    "GAP-0381": (ENRICH, "QB5_B#q16", "The human-element casualty card exists; closing the loop from an injury report to a preventive control is the missing limb."),
    "GAP-0382": (ENRICH, "QB9_B#q2", "The SOPEP card exists; whether an oil-spill drill is a strategic or a tactical action is the missing limb."),
    "GAP-0384": (ENRICH, "QB2_A#q15", "The ICOF card exists; the supplements beyond the cargo list are the missing limb."),
    "GAP-0399": (ENRICH, "QB4_A#q5", "The PSC card exists; the ship risk profile and how targeting data reaches the MoU are missing. Merges GAP-0402 and GAP-0404."),
    "GAP-0447": (ENRICH, "QB5_J#q1", "The LCV card exists; carbon intensity per unit energy and the owner case are missing."),
    "GAP-0448": (ENRICH, "QB8_G#q2", "The IGC card exists; which code governs a fossil-to-methane retrofit, and the IGC/IGF boundary, are missing."),
    "GAP-0455": (ENRICH, "QB3_J#q6", "The P0 BWTS card answers UV; the explicit IMO-against-USCG intensity and D-2 comparison is the missing limb."),
    "GAP-0466": (ENRICH, "QB4_B#q2", "The CE takeover card exists; taking over from a different management for one intended voyage is the missing limb."),
    "GAP-0480": (ENRICH, "QB1_A#q18", "The FAL card exists; which FAL form reports lost containers is the missing limb."),
    "GAP-0482": (ENRICH, "QB4_E#q3", "The young seafarer card exists; MLC certificate issuance, audit scope and grievance redressal are missing limbs."),
    "GAP-0490": (ENRICH, "QB3_A#q8", "The loading instrument card exists; SOLAS XII item-by-item scope and post-flooding criteria are missing limbs."),
    "GAP-0521": (ENRICH, "QB3_J#q5", "The NOS-DCP card exists; the MS Act section number and the national reporting centre are missing limbs."),
    "GAP-0530": (ENRICH, "QB1_F#q12", "The seafarer welfare card exists; the Provident Fund and the COVID-era relief limb are missing. Merges GAP-0533."),
    "GAP-0542": (ENRICH, "QB6_D#q2", "The azimuth propeller card exists; the electric-propulsion drive train is the missing limb."),
    "GAP-0560": (ENRICH, "QB4_B#q3", "The SMS planned-maintenance card exists; maintenance types and the completion-record set are missing limbs."),
    "GAP-0574": (ENRICH, "QB3_A#q6", "The ESP card exists; the Condition Evaluation Report, the thickness-measurement report and the SOLAS chapter citation are missing limbs."),
    "GAP-0609": (ENRICH, "QB5_B#q9", "The collision card exists; the watertight-integrity survey, the reporting chain and the document set are missing limbs."),
    "GAP-0610": (ENRICH, "QB1_G#q29", "The legal-committee amendment card exists; recent security incidents and their insurance effect are the missing limb."),
    "GAP-0616": (ENRICH, "QB1_A#q12", "The Institute Time Clauses card exists; the 3/4ths running-down clause and the residual quarter are the missing limb."),
    "GAP-0626": (ENRICH, "QB9_H#q9", "The charter cards carry bareboat; the bareboat-cum-demise distinction and its hire mechanics are missing."),
    "GAP-0646": (ENRICH, "QB1_supplementary#q3", "The damage stability card exists; why immersion is permitted only to the margin line is the missing limb."),
    "GAP-0668": (ENRICH, "QB1_B#q7", "The RO criteria card exists; what a single RO may and may not do under a given flag delegation is the missing limb."),
    "GAP-0684": (ENRICH, "QB9_A#q2", "The CLC card exists; the 1969-against-1992 protocol differences are the missing limb."),
    "GAP-0690": (ENRICH, "QB3_H#q6", "The Annex II card exists; where onboard to find the permitted cargo list for the ship is the missing limb."),
    "GAP-0701": (ENRICH, "QB9_H#q4", "The grievance card exists; who the Designated Grievance Redressal Officer is under the Indian regime is the missing limb."),
    "GAP-0703": (ENRICH, "QB5_D#q3", "The P0 card carries owner duty in outline; where MLC Title 4 and the MS Act state it is the missing limb."),

    # ---- FOLLOW-UP ONLY --------------------------------------------------
    "GAP-0126": (FOLLOWUP, "QB3_I#q4", "Why barnacles cannot attach is the mechanism the hydrogel card already sets up - an expected-detail follow-up, not a card."),
    "GAP-0607": (FOLLOWUP, "QB9_C#q5", "Marine against motor insurance is a framing contrast, best carried as an opening follow-up on the insurance-principles card."),
    "GAP-0620": (FOLLOWUP, "QB1_A#q9", "Ever Given as a worked general-average example belongs as an examiner-chain follow-up on the GA card."),
    "GAP-0190": (FOLLOWUP, "QB5_E#q5", "The sitting Secretary-General is a currency detail, not an answer. Carry as a trap or expected detail."),

    # ---- MERGE -----------------------------------------------------------
    "GAP-0241": (MERGE, "GAP-0180", "Conciliation is the dispute-settlement limb of the Intervention Convention ask, from the same examiner and the same source page."),
    "GAP-0223": (MERGE, "GAP-0220", "Li-ion hazards and alternative chemistries are the same production family as the AVD firefighting ask."),
    "GAP-0379": (MERGE, "GAP-0376", "Same examiner, same incident, same canonical stowaway answer."),
    "GAP-0402": (MERGE, "GAP-0399", "PSC preparation on notice is the same PSC family."),
    "GAP-0404": (MERGE, "GAP-0399", "PSC selection, interval and documents is the same PSC family."),
    "GAP-0533": (MERGE, "GAP-0530", "Seafarer welfare and provident fund are one ask."),
    "GAP-0517": (MERGE, "GAP-0516", "Drydock cost estimation is the same budgeting family."),
    "GAP-0519": (MERGE, "GAP-0516", "Drydock frequency and job selection is the same drydock-planning family."),
    "GAP-0624": (MERGE, "GAP-0619", "Hospital arrangements and who bears the cost is the same medical-diversion family."),
    "GAP-0485": (MERGE, "GAP-0165", "The examiner's real demand was the instrument taxonomy, which the rules-against-regulations enrichment covers."),

    # ---- P0-demoted residue (referred out of the pre-24-August batch) ----
    "GAP-0009": (AMBIG, None, "'STCW 7, 8' does not establish whether STCW chapters VII and VIII, regulations III/7 and III/8, or Manila amendment items are meant. The corpus answers chapter VIII (QB5_B#q7) but not the other readings; forcing one would guess."),
    "GAP-0093": (ENRICH, "QB4_H#q9", "The WHO/medical certificate card exists; the current amendment position on the seafarer medical certificate beyond the transgender change is the missing limb."),
    "GAP-0494": (COVERED, "QB3_D#q1", "The Green Passport / IHM card carries the IHM parts I-III in 62 mentions, and QB3_H#q5 carries the recycling survey sequence."),

    # ---- AMBIGUOUS / NOT A GAP -------------------------------------------
    "GAP-0118": (AMBIG, None, "FTIR: Fourier-transform infrared analysis of lube or fuel oil is the likely reading, but a one-token prompt does not exclude a fixed gas-detection reading. Not forced."),
    "GAP-0291": (AMBIG, None, "'Navigational Equipments' is a topic label, not an ask. No scope can be derived from it."),
    "GAP-0335": (AMBIG, None, "'Metos (study of measurement)' - metocean, metrology and a mis-transcription are all plausible."),
    "GAP-0338": (AMBIG, None, "ICCT/ICT: the International Council on Clean Transportation and information and communication technology are both live readings in this corpus."),
    "GAP-0508": (AMBIG, None, "The candidate recorded that he did not know what was being asked. Several joint IMO/ILO instruments fit; forcing one would guess on the candidate's behalf."),
    "GAP-0563": (AMBIG, None, "'Djibuti' most likely means the Djibouti Code of Conduct, but the bare place name does not establish the ask."),
    "GAP-0372": (NOT_A_GAP, None, "MERI magazine is a question about a publication the candidate reads, not an examinable technical or regulatory ask."),
}
