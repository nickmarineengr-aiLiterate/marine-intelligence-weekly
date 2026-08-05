#!/usr/bin/env python3
"""Cross-check Parts 19-22 topics against:
  (a) uday-index-crossref.html — the curated A-Z book-index -> Parts 1-18 map
  (b) direct full-text grep of Parts 1-18 HTML bodies

Outputs a structured report per P19-22 topic: any Parts 1-18 hits, with the
matched Part/Topic, the crossref index note (if any), and a snippet of
surrounding text from the live file for judgement.

Usage: python audit_overlap.py
"""
import glob, io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
_real_print = print

ROOT = r'F:\marine-intelligence-weekly'
SPECS = os.path.join(ROOT, 'tools', 'notes', 'specs')
NOTES = os.path.join(ROOT, 'meoclass1', 'oralnotes')

STOP = {'and','the','of','a','to','in','for','on','or','with','by','at','from',
        'is','are','be','as','an','its','their','this','that','not','no'}

def load_new_topics():
    out = []
    for p in (19, 20, 21, 22):
        d = json.load(open(os.path.join(SPECS, 'p%d.json' % p), encoding='utf-8'))
        for t in d['topics']:
            out.append({'part': p, 'n': t['n'], 'title': t['title'],
                       'kw': [k.strip().lower() for k in t.get('kw', '').split(',') if k.strip()],
                       'examiner': t.get('examiner', '')})
    return out

def sig_terms(kw_list):
    """Keep multi-word / distinctive kw phrases; drop very generic single words."""
    out = []
    for k in kw_list:
        words = [w for w in re.split(r'\s+', k) if w]
        if len(words) >= 2 or (words and words[0] not in STOP and len(words[0]) > 5):
            out.append(k)
    return out

# ---- (a) parse the crossref index -----------------------------------------
def parse_crossref():
    h = open(os.path.join(NOTES, 'uday-index-crossref.html'), encoding='utf-8').read()
    rows = []
    for m in re.finditer(r'<(a|div) class="idx-row ([a-z\-]+)"(?:[^>]*?href="([^"]*)")?[^>]*data-kw="([^"]*)">(.*?)</\1>',
                         h, re.S):
        _tag, status, href, kw, body = m.groups()
        topic = re.search(r'idx-topic">([^<]*)</span>', body)
        page = re.search(r'idx-page">([^<]*)</span>', body)
        note = re.search(r'idx-note">([^<]*)</span>', body)
        stat = re.search(r'idx-status[^"]*">([^<]*)</span>', body)
        rows.append({
            'status': status, 'href': href, 'kw': kw,
            'topic': topic.group(1).strip() if topic else '',
            'page': page.group(1).strip() if page else '',
            'note': note.group(1).strip() if note else '',
            'stat_text': stat.group(1).strip() if stat else '',
        })
    return rows

def crossref_matches(term, rows):
    hits = []
    tl = term.lower()
    for r in rows:
        if tl in r['kw'] or tl in r['topic'].lower():
            hits.append(r)
    return hits

# ---- (b) direct grep of Parts 1-18 -----------------------------------------
def load_parts_1_18():
    files = {}
    for i in range(1, 19):
        p = os.path.join(NOTES, 'miw-notes-mgmt-p%d.html' % i)
        if os.path.exists(p):
            files[i] = open(p, encoding='utf-8').read()
    return files

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()

def grep_parts(term, parts):
    """Return list of (part_no, topic_id, topic_title, snippet) for each Part
    whose topic block contains the term (case-insensitive, word-ish boundary)."""
    hits = []
    pat = re.compile(re.escape(term), re.I)
    for pno, h in parts.items():
        for blk in re.split(r'(?=<div class="topic-block")', h)[1:]:
            if pat.search(blk):
                tid = re.search(r'id="([^"]+)"', blk)
                ttitle = re.search(r'<h2[^>]*>(.*?)</h2>', blk, re.S)
                m = pat.search(blk)
                s, e = max(0, m.start() - 90), min(len(blk), m.end() + 90)
                snippet = strip_tags(blk[s:e])
                hits.append((pno, tid.group(1) if tid else '?',
                            strip_tags(ttitle.group(1)) if ttitle else '?', snippet))
    return hits


def main():
    out_path = os.path.join(ROOT, 'tools', 'notes', '_overlap_report.txt')
    out = open(out_path, 'w', encoding='utf-8', newline='\n')
    def print(*a, **k):
        k['file'] = out
        _real_print(*a, **k)

    topics = load_new_topics()
    rows = parse_crossref()
    parts = load_parts_1_18()

    for t in topics:
        print('=' * 78)
        print('NEW: Part %d T%d — %s  (examiner: %s)' % (t['part'], t['n'], t['title'], t['examiner']))
        terms = sig_terms(t['kw'])[:14]  # cap for signal/noise
        seen_parts_direct = {}
        seen_crossref = []
        for term in terms:
            for r in crossref_matches(term, rows):
                if r['status'] in ('idx-matched',):
                    seen_crossref.append((term, r))
            for pno, tid, ttitle, snippet in grep_parts(term, parts):
                seen_parts_direct.setdefault((pno, tid, ttitle), set()).add(term)
        if seen_crossref:
            print('  [Book-index crossref hits — Parts 1-18]')
            uniq = {}
            for term, r in seen_crossref:
                uniq.setdefault((r['topic'], r['stat_text'], r['href']), []).append(term)
            for (topicname, stat, href), tms in uniq.items():
                print('    - "%s" -> %s  [%s]  matched on: %s' % (topicname, stat, href, ', '.join(sorted(set(tms)))))
        if seen_parts_direct:
            print('  [Direct full-text hits — Parts 1-18]')
            for (pno, tid, ttitle), tms in sorted(seen_parts_direct.items()):
                print('    - Part %d / %s / "%s"  matched on: %s' % (pno, tid, ttitle, ', '.join(sorted(tms))))
        if not seen_crossref and not seen_parts_direct:
            print('  (no hits in Parts 1-18)')
        print()
    out.close()
    _real_print('Wrote', out_path)

if __name__ == '__main__':
    main()
