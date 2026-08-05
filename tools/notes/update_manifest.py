import json, collections
PATH = r'F:\marine-intelligence-weekly\meoclass1\oralnotes\notes_content_index.json'
d = json.load(open(PATH, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

d['generated'] = '2026-08-05'
d['generated_by'] = ('Claude - added Parts 19-22 of Engineering Management Notes (General Average/YAR 2016, '
                     'Bills of Lading/e-BL, Charterparties/Off-Hire, Maritime Economics/Incoterms/Worldscale, '
                     'Hague-Visby/COGSA 2025, Cargo Liability in Operation, HSSC Surveys/CSM/SEQ, HSSC Certification/'
                     'e-Certificates, ESP/CAS/CAP, CSR/ISM Auditing, SIRE 2.0/CDI/TMSA-3, Kyoto/Paris, IMO GHG Strategy/'
                     'EEDI/EEXI/CII/Net-Zero Framework; cross-checked by Claude against primary IMO/MARPOL/SOLAS/'
                     'indiacode.nic.in sources, overlap-audited against Parts 1-18 via uday-index-crossref.html, '
                     'health-checked, gated, nav-chain fixed p18->19->20->21->22)')
d['total_files'] = d['total_files'] + 4

mg = d['series']['engineering-management-notes']
mg['status'] = 'live - Parts 1-2, 11-22 gated; Parts 3-10 gated (synced 2026-08-05)'

new_entries = collections.OrderedDict()

new_entries['miw-notes-mgmt-p19.html'] = collections.OrderedDict([
    ('part', 19),
    ('page_range', '451-475 of 768'),
    ('topic_count', 5),
    ('summary', 'General Average and the York-Antwerp Rules 2016 (lien on cargo, four security mechanisms, the '
     'Average Adjuster, Rule VII machinery damage, Rule XXIII time bar), Bills of Lading (triple function, '
     'operational typologies, the electronic B/L under MLETR-based law, Bills of Lading Act 2025), Charterparty '
     'Frameworks and Off-Hire (voyage/time/bareboat, laytime/demurrage/laycan, speed and consumption warranty, '
     'BARECON history), Maritime Economics (freight structure, Incoterms 2020, the Worldscale system), and Carriage '
     'of Goods Regimes (Hague/Hague-Visby/Hamburg/Rotterdam comparison, due diligence, Carriage of Goods by Sea Act '
     '2025 — India now Hague-Visby basis).'),
    ('topics', ['General Average & YAR 2016', 'Bills of Lading & the e-B/L', 'Charterparty Frameworks & Off-Hire',
               'Maritime Economics — Incoterms & Worldscale', 'Hague & Hague-Visby Carriage Regimes']),
    ('status', 'gated - live'),
    ('last_verified', '2026-08-05'),
    ('gating_note', 'Built ungated, cross-checked by Claude against primary sources (IMO, CMI, ICC, indiacode.nic.in) '
     'across two verification passes. Corrections: YAR Rule XXIII time bar (absent from YAR 1994, present in 2004/2016); '
     'Bills of Lading Act 2025 (not "Bill") and Carriage of Goods by Sea Act 2025 dates (India now Hague-Visby basis); '
     'BARECON A/B history (no BARECON C exists); Hague-Visby signature vs in-force dates; inverted air-freight '
     'volumetric ratio. Overlap-audited against Parts 1-18: General Average (Part 18 T4) confirmed complementary, not '
     'duplicate. Gated this session with the standard content-protection stack. Nav-chain: Part 18 sidebar updated '
     'with a Part 19 forward link.'),
])

new_entries['miw-notes-mgmt-p20.html'] = collections.OrderedDict([
    ('part', 20),
    ('page_range', '476-500 of 768'),
    ('topic_count', 3),
    ('summary', 'Cargo Liability Regimes in Operation (Clause Paramount, tackle-to-tackle scope, SDR limitation '
     'mechanics under Art. IV r.5(a), Art. IV bis, the due diligence evidence file), Bills of Lading and Charter '
     'Party Operational Management (on-hire/off-hire surveys, bunker ROB quantity disputes and the ASTM 54B volume '
     'correction sequence, bareboat handover), and Marine Survey Regimes (HSSC survey hierarchy, drydocking vs '
     'in-water survey, Continuous Machinery Survey, Safety Equipment Survey and Form E).'),
    ('topics', ['Cargo Liability Regimes in Operation', 'B/L & Charter Party Operational Management',
               'HSSC Surveys, CSM & SEQ']),
    ('status', 'gated - live'),
    ('last_verified', '2026-08-05'),
    ('gating_note', 'Built ungated, cross-checked by Claude against primary sources. Corrections: 666.67/2 SDR limits '
     'reattributed from "Article IV bis" to the correct Article IV r.5(a); "ship\'s rail" liability boundary corrected '
     'to Art. I(e) loading-on/discharging-from; HSSC resolution updated from A.1156(32)/A.1186(33) to current '
     'A.1207(34); SOLAS I/14 certificate-invalidity language corrected (ceases to be valid, not automatic re-survey). '
     'Overlap-audited against Parts 1-18: HSSC survey mechanics cross-referenced to Part 3 T13 (IOPP-specific) and '
     'Part 11 T48 (Load-Line-specific) — both now carry a back-link to this Part\'s general treatment. Gated with the '
     'standard content-protection stack.'),
])

new_entries['miw-notes-mgmt-p21.html'] = collections.OrderedDict([
    ('part', 21),
    ('page_range', '501-525 of 768'),
    ('topic_count', 3),
    ('summary', 'The HSSC Certification Framework (three-way statutory/commercially-mandatory/classification '
     'certificate categorisation, anniversary dates, the three SOLAS I/14 renewal dating rules, the three extension '
     'mechanisms, electronic certificates under FAL.5/Circ.39/Rev.2), Enhanced Structural Inspection Regimes (the ESP '
     'Code — resolution A.1049(27), substantial corrosion and suspect areas, CAS single-hull phase-out as history, '
     'CAP ratings), and Statutory Documentation and Operational Auditing (the Continuous Synopsis Record, ISM DOC/SMC '
     'certification, the downgrade-vs-close-out non-conformity procedure, audit vs survey).'),
    ('topics', ['HSSC Certification Framework & e-Certificates', 'ESP, CAS & CAP',
               'CSR, ISM Certification & Auditing']),
    ('status', 'gated - live'),
    ('last_verified', '2026-08-05'),
    ('gating_note', 'Built ungated, cross-checked by Claude against primary sources including direct SOLAS I/14 text '
     'verification (5/3/1-month extension figures confirmed) and the ESP Code resolution citation (A.1049(27), 30 Nov '
     '2011, mandatory via SOLAS XI-1/2 from 1 Jan 2014). Corrections: A.883(21) mischaracterised as the HSSC founding '
     'instrument (it is implementation guidance; the 1988 Protocols are the actual founding instruments); wrong '
     'issuing regulation for several certificates (SOLAS I/12, not the chapters describing their subject matter); '
     '"ESP Code 2017" corrected to the real citation; ISPS "Form A" corrected (Form A/B belong to the IOPP '
     'Certificate under MARPOL Annex I, a different instrument). Overlap-audited against Parts 1-18: Topic 1 '
     'substantially duplicates Part 11 T48\'s certificate-extension mechanics (both now cross-linked; this Part\'s '
     'distinct contribution is the general cross-certificate treatment plus e-Certificates); Topic 3 substantially '
     'duplicates Part 13 T2 (ISM DOC/SMC) and Part 15 T1 (CSR) (both now cross-linked; this Part\'s distinct '
     'contribution is the downgrade-vs-close-out distinction and the bareboat-handover sequencing walkthrough). '
     'Gated with the standard content-protection stack.'),
])

new_entries['miw-notes-mgmt-p22.html'] = collections.OrderedDict([
    ('part', 22),
    ('page_range', '526-550 of 768'),
    ('topic_count', 3),
    ('summary', 'Commercial Vetting Frameworks (SIRE 2.0\'s core/rotational/campaign question architecture and the '
     'Human/Process/Hardware/Photograph graded-response model, CDI-Marine, TMSA-3\'s 13 elements), Global Climate '
     'Accords and the Legal Genesis of Maritime Decarbonisation (Kyoto Protocol Article 2(2) as the origin of the '
     'IMO\'s GHG mandate, Annex A gases, CDM/JI/Emissions Trading, the Paris Agreement and why shipping sits outside '
     'NDCs), and the IMO GHG Strategy, Market-Based Measures and Technical Energy Efficiency (2018 vs 2023 Strategy, '
     'EEDI/EEXI/SEEMP/CII currently in force, tank-to-wake vs well-to-wake, and the IMO Net-Zero Framework\'s current '
     'adoption status).'),
    ('topics', ['SIRE 2.0, CDI & TMSA-3', 'Kyoto, Paris & the Legal Genesis', 'IMO GHG Strategy, MBMs & EEDI']),
    ('status', 'gated - live'),
    ('last_verified', '2026-08-05'),
    ('gating_note', 'Built ungated, cross-checked by Claude against primary sources including a live re-verification '
     'of the IMO Net-Zero Framework status after MEPC 84 (27 Apr-1 May 2026, no final agreement) — Topic 3\'s original '
     '"reconvenes October 2026" framing (accurate when drafted, per the Oct 2025 MEPC/ES.2 adjournment announcement) '
     'was corrected throughout to the confirmed 4 December 2026 decision point (resumed MEPC/ES.2, immediately after '
     'MEPC 85, 30 Nov-3 Dec 2026). Kyoto Article 2(2) added as the missing legal link explaining IMO GHG jurisdiction; '
     'Doha Amendment entry-into-force date (31 Dec 2020) added. Overlap-audited against Parts 1-18: Topic 3 is '
     'complementary to (not a duplicate of) Part 2 T9\'s deeper NZF pricing-mechanics treatment — cross-linked both '
     'ways; Part 2 T9\'s own stale NZF date was also found and corrected in this session (six occurrences: verify '
     'note, timeline, reg box, Q&A, memory box, revision table). Gated with the standard content-protection stack.'),
])

mg['files'].update(new_entries)

with open(PATH, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

print('OK — total_files now', d['total_files'], '| mgmt files now', len(mg['files']))
