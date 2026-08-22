#!/usr/bin/env python3
"""MEO Class I study spine -- the canonical DOMAIN -> TOPIC registry.

    written spec primary_category   -->  DOMAIN   (exact, governed)
    oral QB file / question text    -->  DOMAIN   (tiered, adjudicated)

This module is a REGISTRY plus TRANSFORMATION LOGIC. Like
tools/pastpapers/topic_taxonomy.py it holds no question ids and no counts:
build_study_spine.py recomputes every number from the canonical sources on
every call.

WHAT THIS IS NOT
----------------
This is NOT an official DGMA syllabus and must never be presented as one.
No DGMA EAC Branch Circular, no Annexure III and no official syllabus node
exists anywhere in this repository (see docs/study/SYLLABUS_SOURCE_STATUS.md).
Until an official instrument is obtained, `official_syllabus_nodes` is empty
on every domain and the spine is explicitly MIW-DERIVED. The field exists so
that official nodes can be hung off it later WITHOUT restructuring the model.

WHY A NEW MODULE AND NOT A SECOND TAXONOMY
------------------------------------------
topic_taxonomy.py already owns the Written projection (primary_category ->
domain, subject_tags -> study topic) and the Solved QP product depends on it
byte-for-byte. This module does NOT reclassify Written questions: it adopts
topic_taxonomy's output verbatim and adds only the layer that did not exist --
the Oral join. The Oral corpus carries topic signal per FILE, not per
question, so an Oral mapping cannot be as precise as a Written one and the
confidence tiers below say so honestly.
"""

# --------------------------------------------------------------------------- #
# DOMAINS -- the study spine roots.
#
# `written_categories` are matched EXACTLY against spec primary_category, so a
# renamed category fails the validator rather than silently emptying a domain.
# --------------------------------------------------------------------------- #
DOMAINS = [
    {
        'domain_id': 'D01',
        'name': 'Statutory Framework, Survey & Classification',
        'short': 'Statutory & Class',
        'written_categories': ['Statutory Framework & Class'],
        'prerequisites': [],
        'rationale': 'Certificates, surveys, class and the flag/port State '
                     'system that every other domain is enforced through.',
    },
    {
        'domain_id': 'D02',
        'name': 'Marine Insurance & Commercial Law',
        'short': 'Commercial Law',
        'written_categories': ['Marine Insurance & Commercial Law'],
        'prerequisites': ['D01'],
        'rationale': 'Liability, insurance and carriage of goods; presupposes '
                     'the statutory status of the ship.',
    },
    {
        'domain_id': 'D03',
        'name': 'Human Element, ISM & Management',
        'short': 'Human Element',
        'written_categories': ['Human Element & Management'],
        'prerequisites': ['D01'],
        'rationale': 'ISM/ISPS/MLC/STCW and shipboard management; the audit '
                     'regime sits on the statutory certification regime.',
    },
    {
        'domain_id': 'D04',
        'name': 'Pollution Prevention & Response',
        'short': 'MARPOL',
        'written_categories': ['Pollution Prevention & Response'],
        'prerequisites': ['D01'],
        'rationale': 'MARPOL annexes, ORB, BWM, AFS and response.',
    },
    {
        'domain_id': 'D05',
        'name': 'Alternative Fuels, GHG & Decarbonisation',
        'short': 'GHG & Fuels',
        'written_categories': ['Alternative Fuels & Decarbonisation'],
        'prerequisites': ['D01', 'D04'],
        'rationale': 'EEXI/CII/SEEMP, GFI and alternative fuels; the most '
                     'currentness-sensitive domain in the corpus.',
    },
    {
        'domain_id': 'D06',
        'name': 'Indian Maritime Legislation',
        'short': 'Indian Law',
        'written_categories': ['Indian Maritime Legislation'],
        'prerequisites': ['D01', 'D02'],
        'rationale': 'Merchant Shipping Act and the Indian administration.',
    },
    {
        'domain_id': 'D07',
        'name': 'Cargo Operations & Bulk Carriage',
        'short': 'Cargo',
        'written_categories': ['Cargo & Bulk Carriage'],
        'prerequisites': ['D01'],
        'rationale': 'IMSBC/IMDG/IGC, container and bulk cargo practice.',
    },
    # --------------------------------------------------------------------- #
    # D08 and D09 have NO written primary_category of their own. They exist
    # because the Oral corpus examines them heavily and the Written corpus
    # files them under other categories. A domain with no written category is
    # legal; the validator only requires that every WRITTEN category is
    # claimed by exactly one domain.
    # --------------------------------------------------------------------- #
    {
        'domain_id': 'D08',
        'name': 'Fire Safety, LSA & FSS',
        'short': 'Fire & LSA',
        'written_categories': [],
        'prerequisites': ['D01'],
        'rationale': 'SOLAS II-2 / III, FSS and LSA Codes -- Oral-heavy, and '
                     'not a written primary_category in the solved corpus.',
    },
    {
        'domain_id': 'D09',
        'name': 'Machinery, Electrical & Automation',
        'short': 'Machinery',
        'written_categories': [],
        'prerequisites': ['D01'],
        'rationale': 'Engine room practice, automation and new engine '
                     'technology -- Oral-heavy engineering practice.',
    },
    {
        'domain_id': 'D10',
        'name': 'Ship Construction, Stability & Naval Architecture',
        'short': 'Construction & Stability',
        'written_categories': [],
        'prerequisites': [],
        'rationale': 'Stability criteria, structural members and hull form. '
                     'Admitted as its own domain after review: the Oral corpus '
                     'examines it heavily, no written primary_category names '
                     'it, and folding it into D01 was polluting a statutory '
                     'domain with naval architecture.',
    },
]

DOMAIN_IDS = [d['domain_id'] for d in DOMAINS]

# --------------------------------------------------------------------------- #
# ORAL FILE -> DOMAIN, tier HIGH.
#
# Assigned ONLY where the file's own title names one domain unambiguously.
# A file whose title advertises a mix ("Statutory, MARPOL, ISM & Survey Mix")
# is deliberately ABSENT here and falls through to per-question adjudication.
# --------------------------------------------------------------------------- #
ORAL_FILE_DOMAIN = {
    # -- D01 statutory / survey / class -------------------------------------
    # NOTE: every QB1 file whose title reads "Engine Construction, Stability &
    # Surveys" names THREE domains and is therefore NOT listed here -- it is a
    # mixed file, adjudicated per question. Only files whose title resolves to
    # one domain are HIGH confidence.
    'QB3_D.html': 'D01',   # IHM / Green Passport -- survey-issued document
    # -- D02 commercial law --------------------------------------------------
    'QB1_A.html': 'D02', 'QB1_B.html': 'D02',
    'QB9_A.html': 'D02', 'QB9_B.html': 'D02', 'QB9_C.html': 'D02',
    'QB9_D.html': 'D02', 'QB9_E.html': 'D02', 'QB9_F.html': 'D02',
    'QB9_G.html': 'D02', 'QB9_H.html': 'D02',
    # -- D03 human element / ISM --------------------------------------------
    'QB4_A.html': 'D03', 'QB4_B.html': 'D03', 'QB4_C.html': 'D03',
    'QB4_D.html': 'D03', 'QB4_E.html': 'D03', 'QB4_F.html': 'D03',
    'QB4_G.html': 'D03', 'QB4_H.html': 'D03', 'QB4_I.html': 'D03',
    'QB4_J.html': 'D03',
    'QB5_A.html': 'D03', 'QB5_B.html': 'D03', 'QB5_C_A.html': 'D03',
    'QB5_C_B.html': 'D03', 'QB5_D.html': 'D03', 'QB5_E.html': 'D03',
    'QB5_F.html': 'D03', 'QB5_G.html': 'D03', 'QB5_H.html': 'D03',
    'QB5_I.html': 'D03',
    # -- D04 MARPOL ----------------------------------------------------------
    'QB3_C.html': 'D04', 'QB3_E.html': 'D04', 'QB3_F.html': 'D04',
    'QB3_G.html': 'D04', 'QB3_H.html': 'D04', 'QB3_I.html': 'D04',
    'QB3_J.html': 'D04', 'QB3_A.html': 'D04',
    # -- D05 GHG / fuels -----------------------------------------------------
    'QB6.html': 'D05', 'QB6_E.html': 'D05',
    'QB7_A.html': 'D05', 'QB7_B.html': 'D05', 'QB7_C.html': 'D05',
    'QB7_D.html': 'D05', 'QB7_E.html': 'D05', 'QB7_F.html': 'D05',
    'QB7_G.html': 'D05', 'QB7_H.html': 'D05', 'QB7_I.html': 'D05',
    # -- D07 cargo -----------------------------------------------------------
    'QB2_A.html': 'D07', 'QB2_B.html': 'D07',
    'QB8_A.html': 'D07', 'QB8_B.html': 'D07', 'QB8_C.html': 'D07',
    'QB8_D.html': 'D07', 'QB8_E.html': 'D07', 'QB8_F.html': 'D07',
    'QB8_G.html': 'D07', 'QB8_H.html': 'D07',
    # -- D08 fire / LSA ------------------------------------------------------
    'QB2_C.html': 'D08', 'QB2_D.html': 'D08', 'QB2_E.html': 'D08',
    'QB2_F.html': 'D08', 'QB2_G.html': 'D08', 'QB2_H.html': 'D08',
    'QB2_I.html': 'D08',
    # -- D09 machinery / automation -----------------------------------------
    'QB5_J.html': 'D09',
    'QB6_C.html': 'D09', 'QB6_D.html': 'D09', 'QB6_F.html': 'D09',
    'QB6_G.html': 'D09', 'QB6_H.html': 'D09',
}

# Files deliberately left to per-question adjudication (tier MEDIUM/UNRESOLVED).
ORAL_MIXED_FILES = [
    'QB1_C.html', 'QB1_D.html', 'QB1_E.html', 'QB1_H.html', 'QB1_I.html',
    'QB1_J.html', 'QB1_K.html', 'QB1_supplementary.html',
                    # all titled "Engine Construction, Stability & Surveys"
    'QB1_F.html',   # "Additional Questions (Statutory, MARPOL, ISM & Survey Mix)"
    'QB1_G.html',   # "Additional Questions (Class, GHG, Tanker & Structural Mix)"
    'QB3_B.html',   # "Hull Surveys, Ship Construction, Inert Gas & MARPOL"
    'QB10_A.html',  # "Maritime Industry, Policy & Current Affairs"
    'QB10_B.html',  # ditto
]

# --------------------------------------------------------------------------- #
# Per-question domain cues, applied ONLY inside ORAL_MIXED_FILES, in order.
# First match wins; a question matching nothing goes to the review queue.
# Tier MEDIUM: the cue is a real domain marker, but it is a text cue and not a
# governed field, so it is reviewable rather than authoritative.
# --------------------------------------------------------------------------- #
QUESTION_CUES = [
    ('D01', r'\bsurvey|certificat|class(?:ification)?\b|\bIACS\b|\bCSM\b|\bCSR\b|'
            r'port state|flag state|\bPSC\b|load ?line|\bESP\b|dry ?dock|'
            r'in water survey|condition of class|registrat'),
    ('D05', r'\bGHG\b|\bCII\b|\bEEXI\b|\bSEEMP\b|decarbon|alternative fuel|'
            r'ammonia|methanol|hydrogen|carbon|net.?zero|\bGFI\b'),
    ('D04', r'\bMARPOL\b|\bORB\b|\bIOPP\b|sewage|garbage|ballast water|\bBWM\b|'
            r'\bAFS\b|scrubber|\bNOx\b|\bSOx\b|pollution|recycl'),
    ('D03', r'\bISM\b|\bISPS\b|\bMLC\b|\bSTCW\b|audit|leadership|fatigue|'
            r'crew|manning|human element|training'),
    ('D08', r'\bLSA\b|\bFSS\b|fire|lifeboat|life ?raft|extinguish|\bCO2\b'),
    ('D07', r'\bcargo\b|container|\bIMDG\b|\bIMSBC\b|\bIGC\b|\bBLU\b|tanker|'
            r'bulk carrier|\bCSC\b|inert gas|\bIG\b system|\bVGM\b'),
    ('D02', r'insurance|\bP&I\b|charter|\bB/?L\b|bill of lading|salvage|'
            r'general average|liability|lien|arrest|claim'),
    ('D10', r'stabilit|\bGZ\b|\bGM\b|buoyanc|inclin|subdivision|bulkhead|'
            r'shell expansion|frame number|\bknee\b|structural|hull structure|'
            r'bonjean|angle of loll|free surface|\bKN\b curve|metacentr|'
            r'propeller|pitch ratio|rudder|block coefficient|tender vs|'
            r'corrosion|\bGRT\b|\bDWT\b|lightweight|freeboard'),
    ('D09', r'automation|electrical|turbocharger|main engine|generator|'
            r'\bUMS\b|blackout|propulsion|machinery|high voltage|breaker'),
]

# Study-priority weights (§25). Transparent and additive -- no opaque score.
PRIORITY_WEIGHTS = {
    'oral_questions':      0.26,   # breadth of oral examination
    'examiner_evidence':   0.22,   # confirmed examiner relationships
    'written_questions':   0.17,   # written examination load
    'written_recurrence':  0.13,   # repeat families -- what comes back
    'foundation':          0.09,   # how many domains depend on this one
    'official_scope':      0.13,   # PRIMARY Annexure III nodes this topic owns
}
# `official_scope` was added once the DGMA syllabus was ingested: how much of
# the examinable syllabus a topic actually owns is a priority signal that
# corpus counts alone cannot see. The five original weights were scaled down
# proportionally rather than re-tuned, so the addition cannot be mistaken for
# a re-ranking exercise. It did move the order: D01 rose above D02 (rank 3 ->
# 2) because D01 owns six PRIMARY Annexure III nodes to D02's two, which is
# exactly the signal the corpus counts were blind to. D03 remains rank 1.
#
# The model stays deliberately transparent: every component publishes its raw
# input, its weight and its scaled contribution. There is no opaque score.
