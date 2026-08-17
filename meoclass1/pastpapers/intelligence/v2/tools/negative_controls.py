# -*- coding: utf-8 -*-
"""Negative controls for the QI-v2 similarity model.

Each control is a pair the classifier must place in a declared class. NC-2 through
NC-6 are false positives a topic-similarity engine would produce and the model must
refuse. Exit code 0 = every control holds.
"""
import re, sys

STOP = set("""a an the of to in on for and or with as at by from is are be been being
this that these those it its which what how why when where who whom you your as per
if under over into during shall will would should can could may might must also
give state explain list our their there each any all""".split())


def toks(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    out = []
    for t in s.split():
        if t in STOP or len(t) < 3:
            continue
        if len(t) > 4 and t.endswith('ies'):
            t = t[:-3] + 'y'
        elif len(t) > 4 and t.endswith('es') and not t.endswith('ses'):
            t = t[:-2]
        elif len(t) > 3 and t.endswith('s'):
            t = t[:-1]
        out.append(t)
    return out


def cont(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A) if A else 0.0


def cls(f, r):
    if f >= .85 and r >= .85: return 'EXACT_OR_NEAR_VERBATIM'
    if r >= .85: return 'ANCESTOR_ABSORBED_AND_EXTENDED'
    if f >= .85: return 'ANCESTOR_NARROWED'
    if max(f, r) >= .65: return 'SAME_CORE_ASK_CANDIDATE'
    if max(f, r) >= .45: return 'TOPIC_ONLY_CANDIDATE'
    return 'NO_MEANINGFUL_MATCH'


PAIRS = [
    ('NC-1 motivation family TRUE positive',
     'As Chief Engineer on board stress the issues you will address for lack of motivation, differences in attitude and to increase sense of competitiveness for better management and effective control?',
     'As chief engineer onboard, stress the issues you will address for lack of motivation, differences in attitude and to increase sense of competitiveness for better management and effective control?',
     'EXACT_OR_NEAR_VERBATIM'),
    ('NC-2 cargo abandonment vs abandonment of ship',
     'In what circumstances is cargo considered abandoned, and who carries liability for such cargo?',
     'When is a ship treated as a wreck and what constitutes abandonment of the ship by her owners?',
     'NO_MEANINGFUL_MATCH'),
    ('NC-3 motivation-as-topic vs motivation family',
     'As Chief Engineer on board stress the issues you will address for lack of motivation, differences in attitude and to increase sense of competitiveness for better management and effective control?',
     'With respect to engine room man management enlist the key issues you will address with proper justification in the following areas (a) Training programmes (b) Long term personnel development concept (c) Attitude and motivation development (d) Emergency response (e) Copying with stress',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY_CANDIDATE'),
    ('NC-4 dry dock coordination vs dry dock planning',
     'Your vessel where you are posted as Chief Engineer is about to enter a dry dock. State the coordination and exchange of information necessary with the Master of the vessel for entering the dock. Also, list the necessary preparations required along with the delegation of responsibilities to the engineers of the vessel. Enlist the inspections and co-operations you will make with the dry dock authorities for undocking of the vessel.',
     'Why is dry-docking referred to as a major event in the maintenance of a ship? As a Chief Engineer explain different steps that need consideration while planning a dry-docking project of a ship due for its first special survey.',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY_CANDIDATE'),
    ('NC-5 warranties short-note vs warranties differentiate',
     'Warranties',
     'Differentiate between express and implied warranties and give an example in each case with reference to a hull and machinery policy of insurance.',
     'ANCESTOR_NARROWED|SAME_CORE_ASK_CANDIDATE|TOPIC_ONLY_CANDIDATE|NO_MEANINGFUL_MATCH'),
    ('NC-6 lay-up reactivation vs lay-up preservation (inverse ask)',
     'A ship on which you have joined as Chief Engineer is scheduled to be put in active service after major lay-up and necessary repairs. State the preparation and trials you would conduct prior offering the ship to the surveying authorities for survey and inspection.',
     'Describe the preservation of machinery you would carry out as Chief Engineer when taking a vessel into a prolonged lay-up.',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY_CANDIDATE'),
]

print('%-52s %5s %5s  %-32s %s' % ('CONTROL', 'FWD', 'REV', 'CLASSIFIED', 'RESULT'))
print('-' * 118)
fails = 0
for name, a, b, expect in PAIRS:
    ta, tb = toks(a), toks(b)
    f, r = cont(ta, tb), cont(tb, ta)
    c = cls(f, r)
    ok = c in expect.split('|')
    fails += 0 if ok else 1
    print('%-52s %5.2f %5.2f  %-32s %s' % (name[:52], f, r, c, 'PASS' if ok else 'FAIL (want %s)' % expect))
print()
print('controls: %d  failures: %d' % (len(PAIRS), fails))
sys.exit(1 if fails else 0)
