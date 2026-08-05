import json, re

ROOT = r'F:\marine-intelligence-weekly'
qb = json.load(open(ROOT + r'\meoclass1\qb_content_index.json', encoding='utf-8'))
qb_files = qb['files']
notes = json.load(open(ROOT + r'\meoclass1\oralnotes\notes_content_index.json', encoding='utf-8'))
mg_files = notes['series']['engineering-management-notes']['files']

h = open(ROOT + r'\meoclass1\oralnotes\notes-master-index.html', encoding='utf-8').read()

OUT = open(ROOT + r'\tools\notes\_master_index_audit.txt', 'w', encoding='utf-8')
def p(*a):
    print(*a, file=OUT)

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s).strip()

# Parse part sections
parts = {}
for sec_m in re.finditer(r'<section class="part-section" id="(p\d)">(.*?)</section>', h, re.S):
    pk, body = sec_m.groups()
    rows = []
    for row_m in re.finditer(r'<div class="note-row (row-matched|row-gap)">(.*?)</div>\s*</div>', body, re.S):
        status, rbody = row_m.groups()
        nid = re.search(r'note-id">(n\d+)<', rbody)
        title = re.search(r'note-title-txt">(.*?)</div>', rbody, re.S)
        href = re.search(r'href="([^"]+)"', rbody)
        rows.append({
            'status': status, 'id': nid.group(1) if nid else '?',
            'title': strip_tags(title.group(1)) if title else '?',
            'href': href.group(1) if href else None,
        })
    parts[pk] = rows

total = sum(len(v) for v in parts.values())
p('TOTAL ROWS PARSED:', total)
for pk in sorted(parts):
    p(' ', pk, len(parts[pk]), 'rows')

# ---- Check matched-row links ----
p()
p('=' * 70)
p('BROKEN / SUSPECT MATCHED LINKS')
p('=' * 70)
broken = 0
NOTES_DIR = ROOT + r'\meoclass1\oralnotes\\'
for pk, rows in parts.items():
    for r in rows:
        if r['status'] != 'row-matched':
            continue
        href = r['href'] or ''
        m_qb = re.search(r'/meoclass1/([^#]+\.html)#q(\d+)', href)
        m_notes = re.match(r'(miw-notes-mgmt-p\d+\.html)#([a-z0-9\-]+)', href)
        if m_qb:
            fname, qnum = m_qb.group(1), int(m_qb.group(2))
            if fname not in qb_files:
                p(pk, r['id'], r['title'], '-> FILE NOT IN QB MANIFEST:', fname)
                broken += 1
                continue
            meta = qb_files[fname]
            qcount = meta.get('question_count', len(meta.get('questions', [])))
            qnums = [q['qnum'] for q in meta.get('questions', [])]
            if qnum not in qnums:
                p(pk, r['id'], r['title'], '-> Q%d NOT FOUND in %s (file has %d questions, qnums=%s)' % (qnum, fname, qcount, qnums))
                broken += 1
        elif m_notes:
            fname, anchor = m_notes.groups()
            try:
                fh = open(NOTES_DIR + fname, encoding='utf-8').read()
            except FileNotFoundError:
                p(pk, r['id'], r['title'], '-> NOTES FILE NOT FOUND:', fname)
                broken += 1
                continue
            if ('id="%s"' % anchor) not in fh:
                p(pk, r['id'], r['title'], '-> ANCHOR NOT FOUND:', anchor, 'in', fname)
                broken += 1
        else:
            p(pk, r['id'], r['title'], '-> UNPARSEABLE HREF:', href)
            broken += 1
p('TOTAL BROKEN:', broken, 'out of', sum(1 for rows in parts.values() for r in rows if r['status']=='row-matched'), 'matched rows')
OUT.close()
