"""Sweep the official DG Shipping MEO CL-I bank against the whole solved corpus.

Reports BOTH directions of containment:
  fwd = how much of the modern text is present in the bank item
  rev = how much of the bank item is present in the modern text  (ancestor absorbed)
"""
import re, json, glob, sys, collections

BANK = r'D:\MIW-Historical-QP-Intake\dgshipping\dgs_meo_cl1_bank_items.json'
SPECS = r'D:\Marine-Intelligence-Weekly\meoclass1\pastpapers\specs'

STOP = set("""a an the of to in on for and or with as at by from is are be been being
this that these those it its which what how why when where who whom you your as per
if under over into during shall will would should can could may might must also
give state explain list our their there each any all""".split())


def toks(s):
    s = (s or '').lower()
    for a, b in [('\u201c', '"'), ('\u201d', '"'), ('\u2018', "'"), ('\u2019', "'")]:
        s = s.replace(a, b)
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


def cont(sub, sup):
    A, B = set(sub), set(sup)
    return len(A & B) / len(A) if A else 0.0


def classify(fwd, rev):
    if fwd >= 0.85 and rev >= 0.85:
        return 'EXACT_OR_NEAR_VERBATIM'
    if rev >= 0.85 and fwd < 0.85:
        return 'ANCESTOR_ABSORBED_AND_EXTENDED'
    if fwd >= 0.85 and rev < 0.85:
        return 'ANCESTOR_NARROWED'
    if max(fwd, rev) >= 0.65:
        return 'SAME_CORE_ASK_CANDIDATE'
    if max(fwd, rev) >= 0.45:
        return 'TOPIC_ONLY_CANDIDATE'
    return 'NO_MEANINGFUL_MATCH'


bank = {int(k): v for k, v in json.load(open(BANK, encoding='utf-8'))['items'].items()}
bank_t = {n: toks(v) for n, v in bank.items()}

hits = []
per_paper = collections.defaultdict(list)
for f in sorted(glob.glob(SPECS + r'\*.json')):
    spec = json.load(open(f, encoding='utf-8'))
    pid = spec['paper_id']
    for q in spec['questions']:
        qid = q['question_id']
        rows = [('__WHOLE__', q.get('total_marks'), q.get('text_verbatim'))]
        for sp in (q.get('subparts') or []):
            if sp.get('label'):
                rows.append((sp['label'], sp.get('marks'), sp['text']))
        for lab, marks, text in rows:
            tt = toks(text)
            if len(set(tt)) < 4:
                continue
            best = None
            for n in bank:
                fwd, rev = cont(tt, bank_t[n]), cont(bank_t[n], tt)
                sc = max(fwd, rev)
                if best is None or sc > best[0]:
                    best = (sc, fwd, rev, n)
            sc, fwd, rev, n = best
            cls = classify(fwd, rev)
            if cls != 'NO_MEANINGFUL_MATCH':
                rec = dict(paper=pid, question=qid, limb=lab, marks=marks,
                           bank_item=n, fwd=round(fwd, 2), rev=round(rev, 2), cls=cls)
                hits.append(rec)
                per_paper[pid].append(rec)

strong = [h for h in hits if h['cls'] in
          ('EXACT_OR_NEAR_VERBATIM', 'ANCESTOR_ABSORBED_AND_EXTENDED', 'ANCESTOR_NARROWED')]
print('total non-null matches: %d   strong: %d' % (len(hits), len(strong)))
print()
print('=== STRONG MATCHES ACROSS THE CORPUS ===')
print('%-9s %-14s %-10s %5s %-8s %5s %5s  %s' % ('PAPER', 'QUESTION', 'LIMB', 'MK', 'BANK', 'FWD', 'REV', 'CLASS'))
for h in sorted(strong, key=lambda x: (x['paper'], x['question'])):
    print('%-9s %-14s %-10s %5s BANK-%-4s %5.2f %5.2f  %s' % (
        h['paper'], h['question'], h['limb'], h['marks'], h['bank_item'], h['fwd'], h['rev'], h['cls']))

print()
print('=== PAPERS BY STRONG-MATCH COUNT ===')
cnt = collections.Counter(h['paper'] for h in strong)
for p, c in cnt.most_common():
    print('  %s  %d' % (p, c))

print()
print('=== BANK ITEMS REUSED MOST ===')
bc = collections.Counter(h['bank_item'] for h in strong)
for n, c in bc.most_common(15):
    print('  BANK-%-4s x%d  %s' % (n, c, bank[n][:120]))

json.dump(hits, open(sys.argv[1], 'w', encoding='utf-8'), indent=1) if len(sys.argv) > 1 else None
