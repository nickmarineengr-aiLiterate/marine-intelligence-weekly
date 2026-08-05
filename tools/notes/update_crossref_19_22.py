#!/usr/bin/env python3
"""Convert the 'planned' rows in uday-index-crossref.html that fall within
pages 451-550 (Parts 19-22, now built) into 'matched' rows pointing at the
real topic anchors, based on where the content actually landed (not the
original page-based guess, since my actual topic split differs from the
assumed even 3-per-Part plan). Two terms with no verified real match
(ZESIS / FEEBATE MECHANISM) are converted to 'gap' instead of falsely
matched. Recomputes the stat-strip counts at the end.

Usage: python update_crossref_19_22.py
"""
import re

PATH = r'F:\marine-intelligence-weekly\meoclass1\oralnotes\uday-index-crossref.html'

# TOPIC_NAME (as it appears in idx-topic, exact) -> (part, topic_n, note)
MATCH = {
    'CHARTER PARTY': (19, 3, 'Charterparty Frameworks, Off-Hire &amp; Commercial Ship Management'),
    'CONTRACT OF AFFREIGHTMENT': (19, 3, 'Covered within Charterparty Frameworks (COA vs individual voyage)'),
    'FREIGHT RATE CALC': (19, 4, 'Maritime Economics — Freight Structures, Incoterms 2020 &amp; Worldscale'),
    'HAGUE RULES': (19, 5, 'Carriage of Goods Regimes — the Hague Rules, Hague-Visby &amp; COGSA 2025'),
    'HAGUE VISBY RULES': (19, 5, 'Carriage of Goods Regimes — Hague-Visby limits, Art. IV r.5(a)'),
    'HAMBURG RULES': (19, 5, 'Comparison table: Hague-Visby vs Hamburg vs Rotterdam'),
    'INCOTERMS': (19, 4, 'Incoterms 2020 — the eleven rules, cost/risk transfer'),
    'SDR': (19, 5, 'Hague-Visby SDR limitation figures (see also Part 20 T1 for full mechanics)'),
    'WORLD SCALE': (19, 4, 'The Worldscale system — nominal standard vessel, WS100'),
    'ROTTERDAM RULES': (19, 5, 'Carriage regime comparison table — Rotterdam Rules (not in force)'),
    'CONTINUOUS SURVEY OF MACHINERY (CSM)': (20, 3, 'Continuous Machinery Survey and PMS Survey arrangements'),
    'HARMONISED SURVEY (HSSC)': (20, 3, 'HSSC survey hierarchy — see also Part 21 T1 for certification/validity'),
    'SAFETY EQUIPMENT SURVEY (SEQ)': (20, 3, 'Safety Equipment Survey and Form E'),
    'SURVEY TYPES': (20, 3, 'Initial / Annual / Intermediate / Renewal / Additional survey types'),
    'ANNIVERSARY DATE': (21, 1, 'Anniversary dates and SOLAS I/14 validity rules'),
    'AUDIT &amp; SURVEY': (21, 3, 'Administrative Audit vs Technical Survey — deep dive'),
    'CERTIFICATES': (21, 1, 'Statutory / commercially mandatory / classification certificate categories'),
    'CERTIFICATES (E)': (21, 1, 'Electronic certificates — FAL.5/Circ.39/Rev.2'),
    'ENHANCED SURVEY PROGRAM (ESP)': (21, 2, 'The ESP Code — A.1049(27), Annex A/B, the ESP File'),
    'CONDITION ASSESSMENT PROGRAM': (21, 2, 'CAP ratings — CAP-1 to CAP-4'),
    'CONDITION ASSESSMENT SCHEME': (21, 2, 'CAS — single-hull tanker phase-out (historical)'),
    'CONTINUOUS SYNOPSIS RECORD (CSR)': (21, 3, 'The CSR — SOLAS XI-1/5, 14 mandatory contents'),
    'CDI': (22, 1, 'CDI-Marine and the Marine Packed Cargo Audit Scheme'),
    'SIRE': (22, 1, 'SIRE 2.0 architecture — core/rotational/campaign questions'),
    'TMSA': (22, 1, 'TMSA-3 — 13 elements, maturity levels 1–4'),
    'KYOTO PROTOCOL': (22, 2, 'Kyoto Protocol — Art. 2(2), Annex A gases, market mechanisms'),
    'GREENHOUSE GAS': (22, 3, 'IMO GHG Strategy — 2018 vs 2023, EEDI/EEXI/CII'),
    'CLEAN DEVELOPMENT MECHANISM (CDM)': (22, 2, 'Kyoto Article 12 — CDM and Certified Emission Reductions'),
    'JOINT IMPLEMENTATION': (22, 2, 'Kyoto Article 6 — Joint Implementation and Emission Reduction Units'),
    'EMISSION CREDITS': (22, 2, 'CERs (CDM) and ERUs (Joint Implementation)'),
    'EMISSION TRADE': (22, 2, 'International Emissions Trading — Kyoto Article 17'),
    'PARIS AGREEMENT': (22, 2, 'The Paris Agreement — NDCs, and why shipping is not in them'),
    'CARBON FOOTPRINT': (22, 3, 'Tank-to-wake vs well-to-wake accounting'),
    'CARBON NEUTRAL': (22, 3, 'Net-zero by or around 2050 — the 2023 Revised Strategy'),
    'EEDI': (22, 3, 'Energy Efficiency Design Index — phases 0–3'),
    'EEXI': (22, 3, 'Energy Efficiency Existing Ship Index — power limitation'),
    'GHG STRATEGY': (22, 3, 'Initial (2018) vs Revised (2023) IMO GHG Strategy'),
}

# Terms in the built range with NO verified match — convert planned -> gap
NO_MATCH_GAP = {'ZESIS', 'FEEBATE MECHANISM (ZESIS)'}

TITLES = {
    19: 'General Average &amp; YAR 2016, Bills of Lading, Charterparties, Maritime Economics &amp; the Hague Rules',
    20: 'Cargo Liability Regimes in Operation, Charter Party Operational Management, HSSC Surveys, CSM &amp; SEQ',
    21: 'HSSC Certification Framework &amp; e-Certificates, ESP/CAS/CAP, CSR &amp; Operational Auditing',
    22: 'SIRE 2.0/CDI/TMSA-3, Kyoto &amp; Paris, IMO GHG Strategy/EEDI/EEXI/CII/NZF',
}


def main():
    h = open(PATH, encoding='utf-8').read()
    converted, gapped = 0, 0

    def repl(m):
        nonlocal converted, gapped
        full, kw, body = m.group(0), m.group(1), m.group(2)
        topic_m = re.search(r'idx-topic">([^<]*)</span>', body)
        if not topic_m:
            return full
        topic_name = topic_m.group(1).strip()
        note_m = re.search(r'idx-note">([^<]*)</span>', body)
        if not (note_m and re.search(r'Est\. Part (19|20|21|22)\b', note_m.group(1))):
            return full  # not in our built range, leave untouched

        if topic_name in NO_MATCH_GAP:
            gapped += 1
            new_body = re.sub(
                r'<span class="idx-status idx-status-planned">📋 Planned</span>',
                '<span class="idx-status idx-status-gap">⚠ Gap</span>', body)
            new_body = re.sub(
                r'<span class="idx-note">[^<]*</span>',
                '<span class="idx-note">In built range (Part 22) but no verified MIW Notes match found — genuine gap, flagged 2026-08-05</span>',
                new_body)
            return '<div class="idx-row idx-gap" data-kw="%s">%s</div>' % (kw, new_body)

        if topic_name not in MATCH:
            return full  # in range but not one we've mapped -- leave as planned, don't guess

        part, tn, note = MATCH[topic_name]
        converted += 1
        href = 'miw-notes-mgmt-p%d.html#topic-p%d-%d' % (part, part, tn)
        new_body = re.sub(
            r'<span class="idx-status idx-status-planned">📋 Planned</span>',
            '<span class="idx-status idx-status-live">✅ Part %d · T%d</span>' % (part, tn), body)
        new_body = re.sub(
            r'<span class="idx-note">[^<]*</span>',
            '<span class="idx-note">%s</span>' % note, new_body)
        return '<a class="idx-row idx-matched" href="%s" data-kw="%s">%s</a>' % (href, kw, new_body)

    h2 = re.sub(r'<div class="idx-row idx-planned"[^>]*data-kw="([^"]*)">(.*?)</div>', repl, h, flags=re.S)

    # recompute stats
    matched = len(re.findall(r'class="idx-row idx-matched"', h2))
    gap = len(re.findall(r'class="idx-row idx-gap"', h2))
    planned = len(re.findall(r'class="idx-row idx-planned"', h2))
    total = matched + gap + planned

    def set_stat(html, cls, value):
        return re.sub(
            r'(<div class="stat-card%s"><div class="stat-num">)\d+(</div>)' % (' ' + cls if cls else ''),
            r'\g<1>%d\g<2>' % value, html)

    h2 = set_stat(h2, 'sc-matched', matched)
    h2 = set_stat(h2, 'sc-gap', gap)
    h2 = set_stat(h2, 'sc-planned', planned)
    h2 = re.sub(r'(<div class="stat-card"><div class="stat-num">)\d+(</div><div class="stat-label">Total Book Topics)',
               r'\g<1>%d\g<2>' % total, h2)

    open(PATH, 'w', encoding='utf-8', newline='\n').write(h2)
    print('Converted to matched:', converted)
    print('Converted to gap:', gapped)
    print('New stats -> matched=%d gap=%d planned=%d total=%d' % (matched, gap, planned, total))


if __name__ == '__main__':
    main()
