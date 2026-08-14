#!/usr/bin/env python3
"""Question-only extractor for the historical (intelligence-only) QP source copies.

WHY THIS FILE EXISTS
--------------------
The six-year intelligence layer needs printed question wording for the sittings
MIW holds a source copy of but has not solved. That wording was originally
produced by a one-shot script living in a Claude session's scratchpad
directory, which meant the durable store could not be regenerated once the
session ended -- and, worse, that the scratchpad copy and the committed copy
drifted apart without anything noticing. This file already existed as a governed tool but only ever covered the 2021-2022
window, emitted a bare list rather than the store document, and had no default
output path -- so the committed store was still assembled by hand around it. It
now produces the store itself, for the whole window, with its inputs and outputs
named.

    meoclass1/pastpapers/docs/QP2[123]*.pdf   (local, gitignored)
        --> meoclass1/pastpapers/intelligence/historical_qp_intelligence.json

The PDFs are third-party source copies and stay out of git by standing policy
(see .gitignore). They are therefore a LOCAL input: this tool refreshes the
store when a new source copy is acquired. Everything downstream reads the
committed JSON, so a clean checkout regenerates the intelligence layer without
needing a single PDF.

DELIBERATELY NO ANSWER CONTENT
------------------------------
Nothing here reads, infers or writes a model answer. The records this produces
are printed question wording and printed rubric metadata, and the schema says
so in prose so that a future reader cannot mistake the store for a product
manifest.

THE STORE IS NOT FILTERED BY SOLVED STATUS
------------------------------------------
Every held sitting in the window is extracted, including one that has since
been solved. Graduation -- excluding a paper that now has a canonical solved
spec -- is applied by the CONSUMER (build_sixyear_intelligence.py), not here.
Keeping the shelf record complete and the filter in one place is what makes the
exclusion testable; the alternative, deleting a paper from the store by hand
when it graduates, is the defect this whole change exists to end.

DETERMINISM
-----------
No clock is read and no random value is used, so re-running on unchanged PDFs
reproduces the file byte for byte. A `generated` date would make the store
differ every day for no reason and would defeat the determinism test.
"""
import glob
import json
import os
import re
import sys

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

SOURCE_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'docs', 'QP2[123]*.pdf')
OUT_PATH = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'intelligence',
                        'historical_qp_intelligence.json')

SCHEMA = 'miw.pastpapers.historical_qp_intelligence.v2'

WHAT_THIS_IS = (
    'Question-only records for sittings MIW holds a source copy of. These papers carry printed '
    'question wording and printed rubric metadata and nothing else. No model answer, Understand, '
    'Exam Plan, Study Guide or Recall content exists for them here, and none may be authored '
    'without a separate Founder decision.'
)

WHAT_THIS_IS_NOT = (
    'This file is NOT the solved-product manifest. solvedQP/solvedqp_content_index.json remains '
    'the single source for solved counts, paid inventory and availability. Nothing here counts as '
    'solved, renders a paid page, appears as AVAILABLE, or creates a customer-facing Added update. '
    'These records participate in recurrence and lineage intelligence only. A sitting listed here '
    'MAY also have a canonical solved spec: consumers exclude it by rule rather than this file '
    'dropping it, so that the exclusion can be tested.'
)

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')

# The third-party host prints its own backward recurrence annotations INSIDE the
# question text, e.g. "2018/AUG 2018/OCT" or "2019/JUL/Q3". They are captured to
# their own field and removed from the stem, for two independent reasons:
#
#   1. Equality. `recurrence_model.normalise_stem` compares printed stems to
#      decide whether two sittings set the same task. A solved spec's stem is
#      transcribed clean, so leaving the host's annotation in a historical stem
#      makes an identical question compare UNEQUAL and silently demotes an
#      EXACT_REPEAT to a NEAR_REPEAT or to nothing at all.
#   2. Leakage. The annotation names a third party's product. It is DISCOVERY
#      ONLY (CURRENT_STATUS section 20) and must never reach a built artefact.
HOST_HINT_RX = re.compile(
    # The question number after the month is written BOTH ways -- "2019/JUL/Q3"
    # and "2023/MAR/4". Requiring the Q matched the first form, stripped
    # "2023/MAR" out of the second, and left a bare "/4" sitting in the stem,
    # which is how QP2303-Q4 came to differ from its own source copy.
    r'\b(?:19|20)\d{2}\s*/\s*[A-Z]{3}(?:\s*/\s*Q?\d+)?\b'
    r'|\b(?:19|20)\d{2}/SR\d+\b'
)

# The host's marketing and watermark lines. Never transcribed.
HOST_BRANDING_RX = re.compile(
    r'DIESELSHIP|WWW\.|dsguides|please click here|purchase our original|'
    r'maritime publishing|CAD DRAWING|15 YEARS|'
    # The host's imprint, printed alone on one bare word. Anchored to the whole
    # line so a question genuinely about publishing is untouched.
    r'^PUBLISHING$', re.I)

# The host's "works on all your devices" blurb. It sits INSIDE a question's span,
# so it was transcribed into the printed stem of 13 questions across 9 papers.
# It is matched on the ASSEMBLED stem rather than line by line because it wraps
# unpredictably: on QP2303 it occupies one line, on QP2310 and QP2311 it breaks
# after "phones," and a line filter removed only the first half, leaving
# "computers, mobiles, tablets etc." sitting in the question.
HOST_BLURB_RX = re.compile(
    r'\s*(?:that runs on\s*)?windows\s*\|\s*iOS.*?tablets\s*etc\.?', re.I | re.S)


def page_text(path):
    doc = fitz.open(path)
    try:
        return doc.page_count, ''.join(p.get_text() for p in doc)
    finally:
        doc.close()


def clean(text):
    return [s for s in (ln.strip() for ln in text.split('\n'))
            if s and not HOST_BRANDING_RX.search(s)]


def segment(lines):
    """Return {q_no: [lines]} for the printed questions.

    Every clause of the marker below exists because a real source copy broke the
    previous one:

        Q6.Recent   -- no space after the point            (QP2304)
        Q7).        -- a closing paren instead of a point  (QP2107-S2)
        Q9 A.       -- no point at all after the digit     (QP2107-S2)
        5. a) ...   -- the 'Q' prefix dropped entirely     (QP2210)

    A bare "<n>." is accepted only IN SEQUENCE, so the numbered rubric block and
    a numbered list inside a question stem cannot be mistaken for a question.
    """
    start = 0
    for i, s in enumerate(lines):
        if re.match(r'^4\.\s*Blank pages', s, re.I):
            start = i + 1
            break

    marks = []
    for i in range(start, len(lines)):
        # After the digit, absorb any run of '.' and ')' then require the stem to
        # begin with a letter or bracket. That rejects "Q6 & Q8 are same", which
        # is an annotation on QP2107-S2 and not a question.
        m = (re.match(r'^(Q)\s?\.?\s?([1-9])\s*[\.\):]*\s*(?=[A-Za-z(]|$)', lines[i])
             or re.match(r'^()([1-9])\s*[\.\)]\s*(?=[A-Za-z(])', lines[i]))
        if m:
            n = int(m.group(2))
            if not marks or n == marks[-1][1] + 1:
                marks.append((i, n))

    seg = {}
    for j, (i, n) in enumerate(marks):
        end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
        seg[n] = lines[i:end]
    return seg


def parse(path):
    pages, raw = page_text(path)
    lines = clean(raw)
    flat = re.sub(r'\s+', ' ', ' '.join(lines))

    paper_id = os.path.basename(path)[:-4]
    m = re.match(r'QP(\d{2})(\d{2})(-S2)?$', paper_id)
    if not m:
        raise SystemExit(f'unrecognised source filename: {path}')
    yy, mm, s2 = m.group(1), m.group(2), m.group(3) or ''
    month_num = int(mm)

    serial = re.search(r'\b(\d{4})\s*EM\b', flat)
    total = re.search(r'Total Marks\s*[-–:]?\s*(\d+)', flat, re.I)
    time_a = re.search(r'TIME ALLOWED\s*[-–:]?\s*([^\n]{0,20}?HOURS)', flat, re.I)

    questions = []
    seg = segment(lines)
    for n in sorted(seg):
        body = ' '.join(seg[n])
        # Strip the marker with the same tolerance the segmenter used, or the
        # stem inherits a stray '.' from "Q7)." or the whole "Q9 " from "Q9 A.".
        body = re.sub(r'^Q?\s?\.?\s?\d\s*[\.\):]*\s*', '', body).strip()

        body = HOST_BLURB_RX.sub(' ', body)
        hints = HOST_HINT_RX.findall(body)
        body = HOST_HINT_RX.sub('', body)
        body = re.sub(r'\s+', ' ', body).strip()

        questions.append({
            'question_id': f'{paper_id}-Q{n}',
            'q_no': f'Q{n}',
            'text_verbatim': body,
            'printed_limbs': sorted({l.lower() for l in re.findall(r'\(?([a-dA-D])\)\s', body)}),
            'printed_marks': [int(x) for x in re.findall(r'\((\d{1,2})\)', body)],
            'host_recurrence_hint': hints,
        })

    return {
        'paper_id': paper_id,
        'status': 'INTELLIGENCE_ONLY',
        'year': 2000 + int(yy),
        # A month NAME, not a number: build_solvedqp_home.load_intelligence looks
        # this value up in recurrence_model.MONTH_NUM to place the sitting on the
        # examination-history matrix.
        'month': MONTHS[month_num - 1],
        'month_num': month_num,
        'sitting': f'{MONTHS[month_num - 1]} {2000 + int(yy)}',
        'second_sitting': bool(s2),
        'printed_serial': serial.group(0) if serial else None,
        'source_pages': pages,
        'total_marks': int(total.group(1)) if total else None,
        'time_allowed': time_a.group(1).strip() if time_a else None,
        'question_count': len(questions),
        'questions': questions,
    }


def build(source_glob=SOURCE_GLOB):
    papers = [parse(f) for f in sorted(glob.glob(source_glob))]
    return {
        'schema': SCHEMA,
        'status_enum': 'INTELLIGENCE_ONLY',
        'what_this_is': WHAT_THIS_IS,
        'what_this_is_not': WHAT_THIS_IS_NOT,
        'regenerate_with': 'python tools/pastpapers/extract_historical_questions.py',
        'source_window': 'QP2[123]* -- the 2021-2023 sittings MIW holds a source copy of',
        'papers': papers,
        'paper_count': len(papers),
        'question_count': sum(p['question_count'] for p in papers),
    }


def main(argv):
    out_path = argv[1] if len(argv) > 1 else OUT_PATH
    doc = build()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    print(f'{doc["paper_count"]} papers  {doc["question_count"]} questions  -> {out_path}')
    for p in doc['papers']:
        flag = '' if p['question_count'] == 9 else '   <-- CHECK'
        hints = sum(len(q['host_recurrence_hint']) for q in p['questions'])
        print(f'  {p["paper_id"]:11s} {p["sitting"]:16s} ser={str(p["printed_serial"]):9s} '
              f'pages={p["source_pages"]} marks={p["total_marks"]} '
              f'Qs={p["question_count"]} hints={hints}{flag}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
