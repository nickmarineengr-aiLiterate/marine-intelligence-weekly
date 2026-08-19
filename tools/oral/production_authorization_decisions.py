"""Laptop independent-review decisions over the final Oral gap adjudication.

This module is EVIDENCE, not arithmetic. Every entry records a decision the
review reached by reading live QB answer bodies, together with the evidence that
forced it. The generator turns these into production actions; it never invents
one. A family absent from OVERRIDES keeps its adjudicated disposition.

The review's governing principle was to attack the count rather than defend it:
for every proposed new card, try existing coverage, enrichment, Notes promotion,
follow-up and merge first. Two adjudicated dispositions did not survive that
attack, and one deliberately-uncounted medium candidate did.
"""
from __future__ import annotations

# Families whose disposition the laptop review CHANGED, with the evidence.
# family_id -> (decision, target, reason)
OVERRIDES = {
    "GAP-0595": (
        "ENRICH_EXISTING_QB", "QB2_B#q7",
        "Filed ALREADY_COVERED against QB2_B#q7, but that card is the "
        "Liner/NVOCC/VOCC operational model and the word tramp occurs exactly "
        "once in it. The ask is the liner-against-tramp commercial contrast. The "
        "adjudicated reason itself concedes that tramp is the residual limb "
        "only, which is the definition of an enrichment, not of coverage."),
    "GAP-0065": (
        "ALREADY_COVERED", "QB3_J#q6",
        "Filed NOTES_TO_QB_PROMOTION on the ground that QB3_J#q6 is scoped to UV "
        "technology. It is not: limb 3 of that card is explicitly the "
        "IMO-against-USCG approval comparison, and it addresses the Alternate "
        "Management System by name, 46 CFR Part 162, VIDA, and G8/G9. The same "
        "dataset files the near-identical GAP-0689 as ALREADY_COVERED against "
        "this very card, so the pair was internally inconsistent."),
    "GAP-0516": (
        "NEW_CANONICAL_QA", None,
        "Held as medium-confidence and left uncounted, but it is the only medium "
        "candidate carrying multi-family mass: it absorbs GAP-0517 (cost "
        "estimation method) and GAP-0519 (drydock frequency and job scope). A "
        "corpus sweep for budget, cost-estimation, job-list and tender "
        "vocabulary returns no owning card - the only dense tender hit is "
        "QB1_C#q3, the tender-against-stiff-ship stability card, a false match. "
        "Drydock budgeting and job prioritisation is a core CE ask."),
    "GAP-0239": (
        "ENRICH_EXISTING_QB", "QB1_B#q19",
        "Warranty against guarantee is a marine-insurance principles limb. The "
        "adjacent card is the correct home; a standalone card would be scoped "
        "below the size of a canonical answer."),
    "GAP-0443": (
        "ENRICH_EXISTING_QB", "QB5_A#q6",
        "Personality development onboard is a limb of the leadership-development "
        "answer, not a separate ask. Six weak hits already sit across the "
        "leadership cards."),
    "GAP-0553": (
        "ENRICH_EXISTING_QB", "QB2_A#q5",
        "The UN telecommunications body is reached through the MMSI and "
        "call-sign card. Naming ITU and its role is one limb there; a standalone "
        "card is over-scoped for a single terse ask."),
    "GAP-0672": (
        "ENRICH_EXISTING_QB", "QB10_B#q1",
        "Controlling a shore workshop repair of a lifeboat davit is a limb of "
        "the SEQ/LSA survey answer that already scores 0.60. The third-party "
        "repair-control angle is real but does not carry a card alone."),
    "GAP-0255": (
        "DEFER_LOW_VALUE", None,
        "Shale gas and its extraction method arose as an examiner tangent. It "
        "has no MEO Class I syllabus anchor and no CE decision attaches to it."),
    "GAP-0354": (
        "HUMAN_REVIEW_REQUIRED", None,
        "VALEMAX is a one-token prompt. The referent is clear (the Vale very "
        "large ore carriers) but the ask is not - design, stability, the "
        "Brazil-China iron-ore trade and the 2011 loss are all plausible. Scope "
        "cannot be derived, so it joins the ambiguous residue rather than being "
        "forced onto a target."),
}

# Notes promotions classified by what they PRODUCE. The adjudicated dataset
# recorded only the Notes SOURCE anchor, never the QB destination, so the
# new-card half of the promotion workload was invisible to every count.
# GAP-0065 is absent: the laptop review resolved it to ALREADY_COVERED.
PROMOTION_KIND = {
    "GAP-0151": ("NEW_CARD",
                 "COFR has zero QB hits; every blue-card hit is a CLC or Bunker "
                 "Convention card."),
    "GAP-0180": ("NEW_CARD",
                 "Intervention Convention has zero QB hits. Scope the card to "
                 "intervention and conciliation - OPRC already appears 96 times "
                 "across four files and must not be restated."),
    "GAP-0218": ("NEW_CARD",
                 "Free-fall lifeboat certification and launch height appear only "
                 "inside the amendments overview."),
    "GAP-0231": ("NEW_CARD", "Bonjean returns zero QB hits."),
    "GAP-0334": ("NEW_CARD", "Great circle returns zero QB hits."),
    "GAP-0342": ("NEW_CARD",
                 "Galvanic series has zero QB hits. Do NOT promote into "
                 "QB3_B#q3: that anchor is half of the known QB3_A#q13 and "
                 "QB3_B#q3 duplicate pair, so enriching it would deepen live "
                 "duplicate debt."),
    "GAP-0355": ("NEW_CARD",
                 "Caustic embrittlement has zero QB hits; every embrittlement "
                 "hit is a hydrogen-fuel card."),
    "GAP-0534": ("NEW_CARD",
                 "The CDC-against-SID distinction is unanswered; the four QB "
                 "hits sit in QB1_F#q19, the Indian maritime administration "
                 "card, which names BSID only in passing."),
    "GAP-0621": ("NEW_CARD", "Incoterms return zero QB hits."),
}

# Reason-text corrections. The disposition stands; the stated justification was
# factually wrong and would mislead whoever writes the answer.
REASON_CORRECTIONS = {
    "GAP-0120": (
        "The claim that Miller and Atkinson cycles return zero hits corpus-wide "
        "is false. Miller occurs 8 times in QB7_I - but every occurrence is "
        "VVT/Miller cycling as a methane-slip mitigation lever, never the cycle "
        "explained, drawn or contrasted with Diesel and Otto. Atkinson is "
        "genuinely zero."),
    "GAP-0378": (
        "The claim of three weak hits is false: steering gear occurs 109 times "
        "across 10 cards. The substance holds - no card owns SOLAS II-1/29 - but "
        "the pre-departure-test limb is ALREADY housed: QB1_K carries SOLAS V/26 "
        "(test within 12 hours before departure, second power unit in restricted "
        "waters) and QB4_C#q9 carries steering-gear drill frequency. Scope the "
        "new card to the II-1/29 capability requirements and cross-link the test "
        "limb, or it becomes a third duplicate home."),
    "GAP-0465": (
        "Bunker delivery note and BDN are not absent - 43 and 61 hits. QB4_I#q2 "
        "genuinely holds BDN plus MARPOL sample tracking inside an ISM-audit "
        "frame. The gap is ordering for quantity and quality, dispute resolution "
        "and the sample set with its retention periods. Cross-link QB4_I#q2."),
}

# Co-location advisories: distinct asks that one author should write together so
# the pair does not restate one another.
COLOCATION = [
    ("GAP-0159", "GAP-0558",
     "Cost decomposition and the motor-against-turbine owner case share the "
     "capital/voyage/operating taxonomy. Author GAP-0558 to reference the "
     "GAP-0159 taxonomy rather than restating it."),
    ("GAP-0225", "GAP-0218",
     "Forward liferaft with HRU, and free-fall lifeboat requirements, are "
     "adjacent LSA arrangement asks. Write them in one sitting so the float-free "
     "and stowage vocabulary stays consistent."),
]

# Technical verification scope required before any answer is published. Keyed by
# the trigger the reviewer identified, applied by the generator.
TECH_SCOPE = {
    "CURRENT_REG_VERIFY_REQUIRED": [
        "GAP-0378", "GAP-0415", "GAP-0262", "GAP-0225", "GAP-0478", "GAP-0728",
        "GAP-0113", "GAP-0218", "GAP-0180", "GAP-0151", "GAP-0534", "GAP-0465",
    ],
    "PRIMARY_AUTHORITY_REQUIRED": [
        "GAP-0378", "GAP-0225", "GAP-0478", "GAP-0728", "GAP-0113", "GAP-0415",
        "GAP-0218", "GAP-0180",
    ],
    "TECH_VERIFY_REQUIRED": [
        "GAP-0080", "GAP-0083", "GAP-0120", "GAP-0124", "GAP-0128", "GAP-0262",
        "GAP-0365", "GAP-0412", "GAP-0418", "GAP-0231", "GAP-0342", "GAP-0355",
        "GAP-0334",
    ],
}
