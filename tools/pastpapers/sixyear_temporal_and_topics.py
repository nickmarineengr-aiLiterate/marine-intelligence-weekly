"""Temporal-repeat watchlist + topic persistence ranking over the six-year map."""
import json, re, sys, os, collections

S = r'C:/Users/User/AppData/Local/Temp/claude/F--RulesApp/8fd949e3-b943-42c3-a2cf-25535f0b6e97/scratchpad'
fams = json.load(open(S + '/sixyear_families.json', encoding='utf-8'))
nodes = json.load(open(S + '/sixyear_nodes.json', encoding='utf-8'))

# Boundaries at which the REQUIRED ANSWER to a stable question changed.
# Each is a dated legal event, not a topic label.
BOUNDARIES = [
    ('2021-01-01', 'IMSBC amendment 05-19 mandatory',            r'bauxite|imsbc|solid bulk|liquefaction|group a'),
    ('2023-01-01', 'EEXI / operational CII apply; SEEMP Part III', r'eexi|cii|carbon intensity|seemp|energy efficiency'),
    ('2023-07-07', '2023 IMO GHG Strategy supersedes the 2018 Initial Strategy',
                                                                  r'ghg|greenhouse|decarbon|net.?zero|emission|alternative fuel|ammonia|methanol|lng'),
    ('2023-12-01', 'IMSBC amendment 06-21 enters into force',      r'imsbc|bauxite|solid bulk|dynamic separation'),
    ('2023-12-06', '33rd IMO Assembly (A.1185/1186/1187(33))',     r'survey|hssc|port state control|psc|iii code|instruments implementation|places of refuge'),
    ('2024-01-01', 'EU ETS extended to maritime transport',        r'ets|emission trading|carbon (price|cost)|eu '),
    ('2024-12-23', 'MLC 2006 as amended by the 2022 amendments',   r'mlc|maritime labour|seafarer|welfare|repatriation|human element|fatigue'),
    ('2025-06-26', 'Hong Kong Convention enters into force',       r'hong kong|recycl|ship recycling|green passport|inventory of hazardous'),
    ('2025-12-03', '34th IMO Assembly (A.1206/1207(34))',          r'survey|hssc|port state control|psc|iii code|instruments implementation'),
    ('2026-03-15', 'Merchant Shipping Act 2025 commences (repeals the 1958 Act)',
                                                                   r'merchant shipping act|indian flag|unseaworthy|detention|dg shipping|coastal'),
]


def key(ym):
    y, m = ym
    return y * 12 + m


def bkey(d):
    y, m, _ = d.split('-')
    return int(y) * 12 + int(m)


watch = []
for f in fams:
    if f['size'] < 2:
        continue
    ks = sorted(key((nodes[q]['year'], nodes[q]['month'])) for q in f['members'])
    stem = f['stem'].lower()
    crossed = []
    for d, label, rx in BOUNDARIES:
        b = bkey(d)
        if ks[0] < b <= ks[-1] and re.search(rx, stem):
            crossed.append((d, label))
    if crossed:
        watch.append({**f, 'boundaries': crossed})

print('=' * 78)
print('TEMPORAL REPEAT WATCHLIST  --  same/near question, REQUIRED ANSWER CHANGED')
print('=' * 78)
print(f'\n{len(watch)} families of {len([f for f in fams if f["size"]>1])} repeating families '
      f'cross at least one dated legal boundary.\n')
for w in sorted(watch, key=lambda x: (-len(x['boundaries']), -x['size'])):
    solved = [m for m in w['members'] if nodes[m]['status'] == 'SOLVED']
    intel = [m for m in w['members'] if nodes[m]['status'] != 'SOLVED']
    print(f"  x{w['size']}  {w['first_seen']} -> {w['last_seen']}  [{w['class']}]")
    print(f"      {w['stem'][:96]}")
    for d, label in w['boundaries']:
        print(f"      CROSSES {d}  {label}")
    print(f"      solved: {', '.join(solved) or '(none)'}")
    print(f"      intelligence-only: {', '.join(intel) or '(none)'}")
    print()

# ---- topic persistence ------------------------------------------------------
TOPICS = [
    ('Classification societies / RO / survey & certification', r'classification societ|recognized organization|\bro\b|harmoni[sz]ed survey|annual survey|periodical survey|esp\b|iacs'),
    ('Marine insurance / general & particular average',        r'marine insurance|general average|particular average|uberrimae|york.?antwerp|average adjust|perils of the sea'),
    ('GHG / decarbonisation / alternative fuels',              r'ghg|decarbon|greenhouse|net.?zero|ammonia|methanol|alternative fuel|carbon intensity|eexi|cii|eedi'),
    ('Merchant Shipping Act / Indian statute / casualty',      r'merchant shipping act|indian flag|unseaworthy|detention|collision off|dg shipping'),
    ('MLC / human element / fatigue / manning',                r'mlc|maritime labour|human element|fatigue|seafarer|stcw|welfare'),
    ('Liability conventions (CLC / Bunkers / HNS / LLMC)',     r'\bclc\b|bunker convention|bunker oil pollution|hns|limitation of liability|llmc|civil liability'),
    ('Salvage / LOF / wreck / places of refuge',               r'salvage|lloyd.s open form|\blof\b|wreck|places of refuge|scopic'),
    ('Propulsion efficiency / propeller / hull',               r'propeller|propulsion|rudder|wake|hull (and|&) propeller|energy saving device|slow steaming'),
    ('Port State Control / III Code / implementation',         r'port state control|\bpsc\b|iii code|instruments implementation|clear grounds|detention'),
    ('Safety management / ISM / FSA / risk',                   r'\bism\b|safety management|formal safety assessment|\bfsa\b|risk assessment|fault tree'),
    ('Ballast water / biofouling / invasive species',          r'ballast water|biofouling|invasive|\bbwm\b|cybutryne|anti.?fouling'),
    ('Cyber risk / digitalisation / autonomous',               r'cyber|digital|autonomous|\bmass\b|data analytic'),
    ('Ship recycling / Hong Kong Convention',                  r'recycl|hong kong convention|green passport|inventory of hazardous'),
    ('MARPOL annexes / pollution prevention',                  r'marpol|annex vi|annex i\b|oil record book|garbage|sewage|scrubber|sox|nox'),
    ('Naval architecture / stability / resistance',            r'stability|resistance|damage stability|trim|squat|directional stabil|manoeuvr'),
]

rows = []
for name, rx in TOPICS:
    qs = [q for q in nodes if re.search(rx, nodes[q]['stem'], re.I)]
    yrs = sorted({nodes[q]['year'] for q in qs})
    sits = len({(nodes[q]['year'], nodes[q]['month']) for q in qs})
    famct = len({f['family_id'] for f in fams if any(m in qs for m in f['members'])})
    rep = sum(1 for f in fams if f['size'] > 1 and any(m in qs for m in f['members']))
    rows.append((name, len(qs), sits, len(yrs), yrs, famct, rep))

print('=' * 78)
print('TOPIC PERSISTENCE  2021-2026')
print('=' * 78)
print(f"\n{'topic':56s} {'Qs':>4s} {'sit':>4s} {'yrs':>4s} {'fam':>4s} {'rep':>4s}")
for r in sorted(rows, key=lambda x: (-x[3], -x[1])):
    print(f'  {r[0]:54s} {r[1]:>4d} {r[2]:>4d} {r[3]:>4d} {r[5]:>4d} {r[6]:>4d}')
print('\n  Qs=questions matching  sit=distinct sittings  yrs=distinct years')
print('  fam=families touched   rep=families that repeat')
json.dump([{'topic': r[0], 'questions': r[1], 'sittings': r[2], 'years': r[3],
            'year_list': r[4], 'families': r[5], 'repeating_families': r[6]} for r in rows],
          open(S + '/sixyear_topics.json', 'w', encoding='utf-8', newline='
'), indent=1, ensure_ascii=False)
json.dump(watch, open(S + '/sixyear_temporal_watch.json', 'w', encoding='utf-8', newline='
'),
          indent=1, ensure_ascii=False)
