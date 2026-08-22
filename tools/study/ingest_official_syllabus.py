#!/usr/bin/env python3
"""Ingest Annexure III of the final DGMA Circular 49 of 2026.

    circular 49 PDF  --(sha256 pin)-->  parse Annexure III  -->
        docs/study/official_syllabus.json

The PDF itself is never committed -- this repository is public and the source
is a Government of India instrument that is freely served from dgma.gov.in.
What is committed is the derived, governed extraction plus the digest that
proves which bytes it came from.

FAIL-CLOSED. If the digest does not match `official_syllabus.SOURCE_SHA256`
this refuses to write anything. A silent reversion to the superseded July
draft is the specific accident this prevents; the draft's digest is pinned
too, so that mistake is named rather than merely rejected.

Determinism: no clock is read. The instrument's own issue date is the temporal
anchor, so two runs over the same PDF are byte-identical.

Usage:
    python tools/study/ingest_official_syllabus.py                  # write
    python tools/study/ingest_official_syllabus.py --check          # verify
    python tools/study/ingest_official_syllabus.py --pdf PATH       # explicit
    python tools/study/ingest_official_syllabus.py --download       # fetch it
"""
import argparse, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import official_syllabus as OS_

DEFAULT_PDF = os.path.join(ROOT, 'docs', 'study', 'sources',
                           'dgma_circular_49_of_2026.pdf')
OUT = os.path.join(ROOT, 'docs', 'study', 'official_syllabus.json')


def resolve_pdf(path, download):
    if download and not os.path.exists(path):
        import urllib.request
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f'downloading {OS_.SOURCE_URL}')
        urllib.request.urlretrieve(OS_.SOURCE_URL, path)
    if not os.path.exists(path):
        print(f'FAIL R-SOURCE-PRESENT: source PDF not found at {path}')
        print('  the PDF is deliberately not committed; re-fetch it with')
        print('  python tools/study/ingest_official_syllabus.py --download')
        raise SystemExit(2)
    return path


def guard_digest(path):
    """The §40 final-source guard. Named failure, never a silent fallback."""
    got = OS_.sha256_file(path)
    if got == OS_.SOURCE_SHA256:
        return got
    if got == OS_.DRAFT_SHA256:
        print('FAIL R-FINAL-SOURCE: this is the SUPERSEDED 28-Jul-2026 DRAFT, '
              'not the final circular.')
        print(f'  the draft carries {OS_.DRAFT_NODES} syllabus items; the final '
              f'carries {OS_.EXPECTED_NODES}.')
    else:
        print('FAIL R-FINAL-SOURCE: source digest does not match the pinned '
              'final circular.')
    print(f'  expected {OS_.SOURCE_SHA256}')
    print(f'  got      {got}')
    raise SystemExit(2)


def build(pdf_path):
    digest = guard_digest(pdf_path)
    page_texts = OS_.pages(pdf_path)
    if len(page_texts) != OS_.SOURCE_PAGES:
        print(f'FAIL R-SOURCE-PAGES: expected {OS_.SOURCE_PAGES} pages, '
              f'got {len(page_texts)}')
        raise SystemExit(2)

    header, nodes = OS_.parse_annex(page_texts)
    if len(nodes) != OS_.EXPECTED_NODES:
        print(f'FAIL R-NODE-COUNT: expected {OS_.EXPECTED_NODES} official '
              f'nodes, parsed {len(nodes)}')
        raise SystemExit(2)

    for n in nodes:
        n['syllabus_version'] = OS_.SYLLABUS_VERSION_ADOPTED
        n['status'] = OS_.ADOPTED_STATUS
        n['effective_from'] = OS_.EFFECTIVE_FROM
        n['source_digest'] = digest

    return {
        'schema_version': '1.0',
        'generated_by': 'tools/study/ingest_official_syllabus.py',
        'authority': 'OFFICIAL. Verbatim from the final DGMA instrument.',
        'source': {
            'circular': OS_.CIRCULAR,
            'circular_number': OS_.CIRCULAR_NUMBER,
            'file_number': OS_.FILE_NUMBER,
            'issuer': OS_.ISSUER,
            'subject': OS_.SUBJECT,
            'issue_date': OS_.ISSUE_DATE,
            'url': OS_.SOURCE_URL,
            'listing': OS_.SOURCE_LISTING,
            'sha256': digest,
            'bytes': OS_.SOURCE_BYTES,
            'pages': OS_.SOURCE_PAGES,
            'acquired_on': OS_.ACQUIRED_ON,
        },
        'annex': {
            'annex_id': OS_.ANNEX_ID,
            'title': OS_.ANNEX_TITLE,
            'applies_to': 'MEO Class I',
            'page_first': OS_.ANNEX_PAGE_FIRST,
            'page_last': OS_.ANNEX_PAGE_LAST,
            'duration': OS_.ANNEX_DURATION,
            'objective': header,
        },
        'version_model': {
            'syllabus_version': OS_.SYLLABUS_VERSION_ADOPTED,
            'status': OS_.ADOPTED_STATUS,
            'issue_date': OS_.ISSUE_DATE,
            'effective_from': OS_.EFFECTIVE_FROM,
            'currently_operative_version': OS_.SYLLABUS_VERSION_CURRENT,
            'note': ('Final and adopted on 2026-08-15; the revised syllabus '
                     'only becomes operative on 2027-01-01. Until then no '
                     'public surface may present it as being in force.'),
        },
        'superseded_draft': {
            'date': OS_.DRAFT_DATE,
            'url': OS_.DRAFT_URL,
            'sha256': OS_.DRAFT_SHA256,
            'nodes': OS_.DRAFT_NODES,
            'status': OS_.DRAFT_STATUS,
        },
        'totals': {'official_nodes': len(nodes)},
        'nodes': nodes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', default=DEFAULT_PDF)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--download', action='store_true')
    args = ap.parse_args()

    if args.check and os.path.exists(OUT) and not os.path.exists(args.pdf):
        # The PDF is not committed, so --check in a clean clone verifies the
        # artefact's internal pin rather than silently passing.
        got = json.load(open(OUT, encoding='utf-8'))
        ok = got['source']['sha256'] == OS_.SOURCE_SHA256
        print('official syllabus -- source pin ' + ('OK' if ok else 'MISMATCH'))
        return 0 if ok else 1

    built = build(resolve_pdf(args.pdf, args.download))
    text = json.dumps(built, indent=2, ensure_ascii=False) + '\n'

    if args.check:
        if not os.path.exists(OUT):
            print('FAIL: docs/study/official_syllabus.json is missing')
            return 1
        if open(OUT, encoding='utf-8').read() != text:
            print('FAIL: docs/study/official_syllabus.json is stale')
            return 1
        print(f'official syllabus -- {len(built["nodes"])} nodes, up to date')
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print(f'wrote {os.path.relpath(OUT, ROOT)} -- '
          f'{len(built["nodes"])} official nodes from {OS_.CIRCULAR}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
