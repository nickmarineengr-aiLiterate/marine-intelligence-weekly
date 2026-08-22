#!/usr/bin/env python3
"""The official DGMA MEO Class I syllabus -- source pin and extraction.

This module is the *only* place that knows what the official instrument is.
Everything downstream (crosswalk, mappings, study packs, XLSX) reads the
generated `docs/study/official_syllabus.json`, never the PDF.

    DGMA EAC Branch Circular No.49 of 2026  (15-Aug-2026)
        Annexure I    MEO Class IV preparatory course syllabus
        Annexure II   MEO Class II  preparatory course syllabus
        Annexure III  MEO Class I   preparatory course syllabus   <-- ours
        Annexure IV   ETO           preparatory course syllabus

Two dates govern and must never be collapsed into one:

  * ISSUE_DATE (15-Aug-2026) -- the circular is FINAL and ADOPTED from here.
  * EFFECTIVE_FROM (01-Jan-2027) -- the revised syllabus only bites from here.

Between them the revised syllabus is adopted but *not yet operative*, which is
why `SYLLABUS_VERSION_ADOPTED` and `SYLLABUS_VERSION_CURRENT` are distinct and
why no public surface may describe the 2027 syllabus as already in force.

FINAL-SOURCE GUARD
------------------
`SOURCE_SHA256` pins the exact bytes of the final circular. Ingestion verifies
it and *fails closed* on any mismatch. That is what stops this system silently
reverting to the 28-Jul-2026 draft, whose Annexure III is a materially
different document: it carried 23 items, not 25, and lacked casualty
investigation and underwater noise entirely.
"""

# --- the final instrument -------------------------------------------------
CIRCULAR          = 'DGMA EAC Branch Circular No.49 of 2026'
CIRCULAR_NUMBER   = '49 of 2026'
FILE_NUMBER       = 'F.No. 13-11028/1/2026-ENGG-DGS'
ISSUER            = 'Directorate General of Maritime Administration, Mumbai'
SUBJECT           = ('Preparatory courses for MEO and ETO grade of CoC '
                     'examinations, reg.')
ISSUE_DATE        = '2026-08-15'
EFFECTIVE_FROM    = '2027-01-01'
SOURCE_URL        = ('https://dgma.gov.in/download/1787368075_6a89128b56069_1-'
                     'eac-branch-circular-no-49-of-2026-on-preparatory-courses-'
                     'for-meo-eto-grade-of-coc-examinations.pdf')
SOURCE_LISTING    = ('https://dgma.gov.in/engineering-wing/'
                     'ew-dgs-eac-circulars-orders-notices-engineering')
SOURCE_SHA256     = '07170f572c99064fad25eedb0fe985886248a81a49b4eb5d4711fd38d186f44d'
SOURCE_BYTES      = 1298819
SOURCE_PAGES      = 33
ACQUIRED_ON       = '2026-08-22'

# --- the annex we consume -------------------------------------------------
ANNEX_ID          = 'Annexure III'
ANNEX_TITLE       = 'Syllabus for MEO Class I Preparatory Course'
ANNEX_PAGE_FIRST  = 24          # 1-indexed pages of the source PDF
ANNEX_PAGE_LAST   = 30
ANNEX_DURATION    = 'Two months (8 weeks, 40 working days, 240 contact hours)'
EXPECTED_NODES    = 25

# --- version model --------------------------------------------------------
SYLLABUS_VERSION_ADOPTED = 'DGMA-C49-2026-ANNEX3'   # in force 01-Jan-2027
SYLLABUS_VERSION_CURRENT = 'MIW-DERIVED-1.0'        # what governs today
ADOPTED_STATUS           = 'FINAL_ADOPTED_NOT_YET_EFFECTIVE'

# --- the superseded draft, recorded so it can never be mistaken for final --
DRAFT_URL    = ('https://dgma.gov.in/download/1785231454_6a68785e08d0e_'
                'draft-eac-circular-on-meo-eto-preparatory-courses.pdf')
DRAFT_SHA256 = 'b6365d2205428f34283b9e259c8a130b4b4dfd2072f52cd1d96141348a21d09c'
DRAFT_DATE   = '2026-07-28'
DRAFT_NODES  = 23
DRAFT_STATUS = 'SUPERSEDED_HISTORICAL_ONLY'

import hashlib
import re


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def classify_digest(digest):
    """'FINAL' | 'SUPERSEDED_DRAFT' | 'UNKNOWN'.

    Split out from the ingester so the final-source guard can be tested
    without either PDF on disk. Naming the draft case is the whole point: a
    bare "digest mismatch" would not tell anyone that the system had just been
    handed a syllabus with two subjects missing.
    """
    if digest == SOURCE_SHA256:
        return 'FINAL'
    if digest == DRAFT_SHA256:
        return 'SUPERSEDED_DRAFT'
    return 'UNKNOWN'


def pages(pdf_path):
    """Return the PDF's pages as text, list position 0 = page 1.

    PyMuPDF, not pypdf: on this circular pypdf returns the annex pages with
    their reading order scrambled and the first two syllabus items missing
    entirely, which the node-count guard catches but cannot repair.
    """
    import fitz
    with fitz.open(pdf_path) as doc:
        return [page.get_text() for page in doc]


_PAGENO = re.compile(r'^\s*\d{1,3}\s*$')
_ITEM = re.compile(r'\n\s*(\d{1,2})\.\s+')


def _strip_page_numbers(text):
    return '\n'.join(l for l in text.split('\n') if not _PAGENO.match(l))


def _normalise(text):
    """Repair two artefacts of the PDF's own typesetting.

    The running annex title is a graphic heading whose text lands mid-page in
    reading order -- left alone it is absorbed into the body of item 2. And
    the bullets inside item 21 are Symbol-font private-use glyphs (U+F0B7)
    that are not bullets to anything downstream.

    Both are presentation, not wording: no official words are added, removed
    or reordered here.
    """
    return text.replace(ANNEX_TITLE, ' ').replace('', '•')


def parse_annex(page_texts):
    """Parse Annexure III into ordered official nodes.

    Returns (header, [{official_node_id, official_order, official_text}, ...]).

    The annex is a flat list of 25 numbered items -- there is no sub-numbering
    in the official text, so `official_parent` is null for every node. We keep
    the field rather than inventing a hierarchy the circular does not have.
    """
    kept = [_normalise(_strip_page_numbers(t))
            for t in page_texts[ANNEX_PAGE_FIRST - 1:ANNEX_PAGE_LAST]]
    body = '\n'.join(kept)

    # Offset of each annex page within `body`, so every node can cite the
    # source page it actually starts on rather than the annex's first page.
    starts, at = [], 0
    for i, t in enumerate(kept):
        starts.append((at, ANNEX_PAGE_FIRST + i))
        at += len(t) + 1

    def page_of(offset):
        page = ANNEX_PAGE_FIRST
        for begin, number in starts:
            if offset >= begin:
                page = number
        return page

    # Anchor on the annex id, not its title: the title is set as a graphic
    # heading in this PDF and is absent from the text layer altogether.
    start = body.find(ANNEX_ID)
    if start < 0:
        raise SystemExit(f'FAIL: annex anchor not found: {ANNEX_ID!r}')

    first = _ITEM.search(body, start)
    if not first:
        raise SystemExit('FAIL: no numbered items found in Annexure III')
    header = re.sub(r'\s+', ' ', body[start + len(ANNEX_ID):first.start()])
    header = header.strip()

    tail = body[first.start():]
    chunks = _ITEM.split(tail)
    nodes, cursor = [], first.start()
    for i in range(1, len(chunks) - 1, 2):
        number = int(chunks[i])
        raw = chunks[i + 1]
        cursor = body.find(raw, cursor)
        text = re.sub(r'[ \t]+', ' ', raw)
        text = re.sub(r'\s*\n\s*', ' ', text).strip()
        nodes.append({
            'official_node_id': f'C49-A3-{number:02d}',
            'official_number': number,
            'official_order': len(nodes) + 1,
            'official_parent': None,
            'source_page': page_of(cursor),
            'official_text': text,
        })
        cursor += len(raw)

    numbers = [n['official_number'] for n in nodes]
    if numbers != list(range(1, len(nodes) + 1)):
        raise SystemExit(f'FAIL: item numbering is not 1..n contiguous: {numbers}')
    return header, nodes
