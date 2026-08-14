"""Question-only extractor for historical (intelligence-only) QP source copies.

Deliberately does NOT read or produce any answer content.
"""
import fitz, re, json, sys, os, glob, hashlib

MON = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June',
       '07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

def page_text(f):
    d = fitz.open(f)
    return d.page_count, ''.join(p.get_text() for p in d)

def clean(t):
    # drop the host's marketing / branding lines; they are never transcribed
    out = []
    for ln in t.split('\n'):
        s = ln.strip()
        if not s:
            continue
        if re.search(r'DIESELSHIP|WWW\.|dsguides|please click here|purchase our original|'
                     r'maritime publishing|CAD DRAWING|15 YEARS', s, re.I):
            continue
        out.append(s)
    return out

def segment(lines):
    """Return {qno: [lines]} using a marker that tolerates a missing 'Q' prefix and
    a missing space after the point -- both are known source-copy artefacts."""
    # the rubric block is numbered 1..4; questions begin after it
    start = 0
    for i, s in enumerate(lines):
        if re.match(r'^4\.\s*Blank pages', s, re.I):
            start = i + 1
            break
    # Marker tolerance, every clause of which exists because a real source copy
    # broke the previous one:
    #   Q6.Recent   -- no space after the point        (QP2304)
    #   Q7).        -- a closing paren instead         (QP2107-S2)
    #   Q9 A.       -- NO point at all after the digit (QP2107-S2)
    #   5. a) ...   -- the 'Q' prefix dropped entirely (QP2210)
    # A bare "<n>." is only accepted in sequence, so the numbered rubric and any
    # numbered list inside an answer stem cannot be mistaken for a question.
    marks = []
    for i in range(start, len(lines)):
        # After the digit, absorb any run of '.' and ')' then require the stem to
        # begin with a letter or bracket. That rejects "Q6 & Q8 are same", which
        # is an annotation on QP2107-S2 and not a question.
        m = re.match(r'^(Q)\s?\.?\s?([1-9])\s*[\.\):]*\s*(?=[A-Za-z(]|$)', lines[i]) \
            or re.match(r'^()([1-9])\s*[\.\)]\s*(?=[A-Za-z(])', lines[i])
        if m:
            n = int(m.group(2))
            if not marks or n == marks[-1][1] + 1:
                marks.append((i, n))
    seg = {}
    for j, (i, n) in enumerate(marks):
        end = marks[j+1][0] if j+1 < len(marks) else len(lines)
        seg[n] = lines[i:end]
    return seg

def parse(f):
    pages, raw = page_text(f)
    lines = clean(raw)
    flat = re.sub(r'\s+', ' ', ' '.join(lines))
    qid = os.path.basename(f)[:-4]
    m = re.match(r'QP(\d{2})(\d{2})(-S2)?$', qid)
    yy, mm, s2 = m.group(1), m.group(2), m.group(3) or ''
    ser = re.search(r'\b(\d{4})\s*EM\b', flat)
    total = re.search(r'Total Marks\s*[–\-:]?\s*(\d+)', flat, re.I)
    time_a = re.search(r'TIME ALLOWED\s*[–\-:]?\s*([^\n]{0,20}?HOURS)', flat, re.I)
    seg = segment(lines)
    qs = []
    for n in sorted(seg):
        body = ' '.join(seg[n])
        # Strip the marker using the same tolerance the segmenter used, or the
        # stem inherits a stray '.' from "Q7)." or the whole "Q9 " from "Q9 A.".
        body = re.sub(r'^Q?\s?\.?\s?\d\s*[\.\):]*\s*', '', body).strip()
        # host's own backward recurrence annotations, e.g. 2019/JUL/Q3 -- captured, never published
        hints = re.findall(r'\b(?:19|20)\d{2}\s*/\s*[A-Z]{3}\s*/\s*Q\d+\b|\b(?:19|20)\d{2}/SR\d+\b', body)
        body = re.sub(r'\b(?:19|20)\d{2}\s*/\s*[A-Z]{3}\s*/\s*Q\d+\b|\b(?:19|20)\d{2}/SR\d+\b', '', body)
        body = re.sub(r'\s+', ' ', body).strip()
        limbs = re.findall(r'\(?([a-dA-D])\)\s', body)
        pm = re.findall(r'\((\d{1,2})\)', body)
        qs.append({
            'q_no': f'Q{n}',
            'question_id': f'{qid}-Q{n}',
            'text_verbatim': body,
            'printed_limbs': sorted(set(l.lower() for l in limbs)),
            'printed_marks': [int(x) for x in pm],
            'host_recurrence_hint': hints,
        })
    return {
        'paper_id': qid,
        'status': 'INTELLIGENCE_ONLY',
        'year': int('20'+yy), 'month': int(mm), 'month_name': MON[mm],
        'sitting': f'{MON[mm]} 20{yy}',
        'second_sitting': bool(s2),
        'printed_serial': ser.group(0) if ser else None,
        'source_pages': pages,
        'total_marks': int(total.group(1)) if total else None,
        'time_allowed': time_a.group(1).strip() if time_a else None,
        'question_count': len(qs),
        'questions': qs,
    }

if __name__ == '__main__':
    out = [parse(f) for f in sorted(glob.glob('meoclass1/pastpapers/docs/QP2[12]*.pdf'))]
    json.dump(out, open(sys.argv[1], 'w', encoding='utf-8', newline='
'), indent=1, ensure_ascii=False)
    for p in out:
        bad = '' if p['question_count'] == 9 else '  <-- CHECK'
        print(f"{p['paper_id']:11s} {p['sitting']:16s} ser={str(p['printed_serial']):9s} "
              f"pages={p['source_pages']} marks={p['total_marks']} Qs={p['question_count']}{bad}")
