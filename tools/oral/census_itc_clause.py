#!/usr/bin/env python3
"""P1-A census: every occurrence of an ITC-Hulls clause citation in the repo.

Non-vacuity contract (brief section 2):
  * asserts the scanned-file set is non-empty and reports its exact count;
  * asserts the matched-site set is non-empty and reports its exact count;
  * every match carries file + anchor/site identity;
  * distinguishes ZERO TRUE MATCHES from ZERO INPUTS SCANNED by reporting both.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv'}
EXTS = {'.html', '.json', '.md', '.py', '.txt'}

# Any decimal clause-like token. Deliberately broad: classification happens later,
# so the census can never hide a site behind a narrow pattern.
TOKEN = re.compile(r'(?<![\d.])(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)(?![\d])')

# Context window used only for *display and classification*, never to find matches.
WIN = 260

ITC_CUES = re.compile(
    r'institute\s+time\s+clauses|itc[-\s]?hulls|\bitc\b|1/11/95', re.I)
NON_ITC_CUES = re.compile(
    r'\bMLC\b|maritime\s+labour|SOLAS|II-2/|III/|reg(?:ulation)?\.?\s*4\.2\b|'
    r'ISM|STCW|MARPOL|A4\.2|Std\s+A', re.I)


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in EXTS:
                yield os.path.join(dirpath, fn)


ANCHOR = re.compile(r'id\s*=\s*"(q\d+[^"]*)"', re.I)


def site_id(text, pos):
    """Nearest preceding question anchor - the site identity, not just the file."""
    best = None
    for m in ANCHOR.finditer(text, 0, pos):
        best = m.group(1)
    return best or '(no-anchor)'


def main():
    scanned = 0
    scanned_with_itc = 0
    rows = []
    for path in iter_files():
        try:
            text = open(path, encoding='utf-8').read()
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        flat = html.unescape(text)
        if not ITC_CUES.search(flat):
            continue
        scanned_with_itc += 1
        for m in TOKEN.finditer(flat):
            lo, hi = max(0, m.start() - WIN), min(len(flat), m.end() + WIN)
            ctx = re.sub(r'<[^>]+>', ' ', flat[lo:hi])
            ctx = re.sub(r'\s+', ' ', ctx).strip()
            # Only clause tokens whose OWN context is ITC-flavoured are sites.
            near = flat[max(0, m.start() - 120):m.end() + 40]
            if not ITC_CUES.search(re.sub(r'<[^>]+>', ' ', near)):
                continue
            rows.append({
                'file': os.path.relpath(path, ROOT).replace(chr(92), '/'),
                'clause': m.group(1),
                'offset': m.start(),
                'site': site_id(text, m.start()),
                'context': ctx,
            })

    # ---- non-vacuity assertions -------------------------------------------
    problems = []
    if scanned == 0:
        problems.append('ZERO INPUTS SCANNED - the walk resolved no files')
    if scanned_with_itc == 0:
        problems.append('ZERO ITC-BEARING FILES - the cue regex resolved nothing')
    if not rows:
        problems.append('ZERO SITES - no clause token in any ITC context')

    out = {
        'files_scanned': scanned,
        'files_with_itc_cue': scanned_with_itc,
        'sites': len(rows),
        'files_with_sites': len(sorted({r['file'] for r in rows})),
        'non_vacuity_problems': problems,
        'rows': rows,
    }
    dest = sys.argv[1] if len(sys.argv) > 1 else None
    blob = json.dumps(out, indent=2, ensure_ascii=False)
    if dest:
        open(dest, 'w', encoding='utf-8').write(blob)
        print('census written to', dest)
    else:
        sys.stdout.reconfigure(encoding='utf-8')
        print(blob)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
