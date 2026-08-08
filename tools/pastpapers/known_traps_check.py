#!/usr/bin/env python3
"""Known-traps check for the Past Written Papers series.

Usage:
  python known_traps_check.py [--self-test]

Two layers, mirroring meoclass1/known_traps.md + qb_health_check.py precedent:

  1. GREP layer. Parses meoclass1/pastpapers/known_traps.md and scans every
     generated page and every spec for the exact wrong phrases marked with a
     `GREP:` line. Entries marked `GREP: SKIP` are manual-review-only and are
     reported as such, never auto-flagged.

  2. STRUCTURAL layer. Encodes the traps that cannot be reduced to a safe phrase
     match, as assertions against the spec -- e.g. "the Q7 Merchant Shipping Act
     claims must carry a re-verification flag". These check that the *right*
     thing is present, rather than policing prose.

Deliberately NOT included: brittle regex over nuanced legal wording. Where a rule
needs judgement it stays in known_traps.md as SKIP and is handled by the
verification pass.

--self-test injects each detectable trap into a copy of the real content and
asserts the checker fires. A trap check that never fires is worse than none.

Exit 1 on any FAIL.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
TRAPS_MD = os.path.join(PP, 'known_traps.md')

# Phrases that legitimately appear in our own machinery and must not self-trip.
# The known_traps.md file itself quotes every wrong phrase by design, and the
# verification records quote them when recording the correction.
EXEMPT_PATHS = ('known_traps.md',)
EXEMPT_DIRS = ('verification',)


def parse_traps(path):
    """Return [(number, title, grep_or_None)] from the markdown."""
    text = io.open(path, encoding='utf-8').read()
    out = []
    for block in re.split(r'\n### ', text)[1:]:
        head = block.splitlines()[0].strip()
        m = re.match(r'(\d+)\.\s*(.*)', head)
        num, title = (m.group(1), m.group(2)) if m else ('?', head)
        g = re.search(r'^GREP:\s*(.+)$', block, re.M)
        val = g.group(1).strip() if g else None
        sc = re.search(r'^SCOPE:\s*(.+)$', block, re.M)
        scope = sc.group(1).strip().lower() if sc else 'all'
        out.append((num, title,
                    None if (val is None or val.upper() == 'SKIP') else val, scope))
    return out


def scannable_files():
    files = []
    for p in sorted(glob.glob(os.path.join(PP, '*.html'))):
        files.append(p)
    for p in sorted(glob.glob(os.path.join(PP, 'specs', '*.json'))):
        files.append(p)
    files.append(os.path.join(PP, 'pastpapers_content_index.json'))
    return [f for f in files if os.path.exists(f)
            and os.path.basename(f) not in EXEMPT_PATHS
            and not any(('%s%s%s' % (os.sep, d, os.sep)) in f for d in EXEMPT_DIRS)]


def grep_layer(traps, extra_text=None):
    fails, checked = [], 0
    corpus = []
    for f in scannable_files():
        corpus.append((os.path.relpath(f, REPO_ROOT).replace('\\', '/'),
                       io.open(f, encoding='utf-8', errors='replace').read().lower()))
    if extra_text is not None:
        corpus.append(('<injected>', extra_text.lower()))
    for num, title, phrase, scope in traps:
        if not phrase:
            continue
        checked += 1
        needle = phrase.lower()
        for name, body in corpus:
            # SCOPE: html limits a trap to generated pages, for traps that are
            # genuinely about rendered output. Brand traces are NOT such a trap:
            # the repository is public, so specs and the manifest are scanned too.
            if scope == 'html' and not name.endswith('.html') and name != '<injected>':
                continue
            if needle in body:
                fails.append('trap %s (%s): found %r in %s' % (num, title[:52], phrase, name))
    return fails, checked


def structural_layer(specs):
    """Traps that must be checked against structure, not prose."""
    fails, checked = [], 0

    for d in specs:
        pid = d['paper_id']
        Q = {q['q_no']: q for q in d['questions']}

        def rv_text(q):
            return ' '.join(
                (r.get('claim', '') + ' ' + r.get('why', '') + ' ' + r.get('class', ''))
                for r in (q.get('reverify_before_publication') or [])
            ).lower() + ' ' + ' '.join(q.get('unresolved') or []).lower()

        # T11: Merchant Shipping Act 2025 claims must carry a re-verification flag.
        checked += 1
        msa = [q for q in d['questions']
               if 'merchant shipping act 2025' in ' '.join(q.get('regulations') or []).lower()
               or 'Merchant Shipping Act 2025' in (q.get('short_title') or '')]
        for q in msa:
            if q.get('model_answer') and not (q.get('reverify_before_publication') or []):
                fails.append('%s %s: Merchant Shipping Act 2025 content with no '
                             'reverify_before_publication entry (trap 11)' % (pid, q['q_no']))

        # T9: ammonia content must record the interim guidance as time-sensitive.
        checked += 1
        amm = [q for q in d['questions']
               if 'MSC.1/Circ.1687' in ' '.join(q.get('regulations') or [])]
        for q in amm:
            if q.get('model_answer') and 'msc.1/circ.1687' not in rv_text(q):
                fails.append('%s %s: ammonia interim guidance is not flagged for '
                             're-verification (trap 9)' % (pid, q['q_no']))

        # T6: iron ore cargo-group content must not be recorded as primary-verified.
        checked += 1
        for q in d['questions']:
            al = ' '.join(q.get('search_aliases') or []).lower()
            if 'iron ore pellets' in al and q.get('model_answer'):
                if 'group c' not in rv_text(q):
                    fails.append('%s %s: iron ore Group classification is not flagged for '
                                 're-verification (trap 6)' % (pid, q['q_no']))

        # T8: Indian marine insurance questions must cite the 1963 Act, not 1906.
        checked += 1
        for q in d['questions']:
            regs = ' '.join(q.get('regulations') or [])
            if 'uberrimae' in ' '.join(q.get('search_aliases') or []).lower() and q.get('model_answer'):
                if '1963' not in regs:
                    fails.append('%s %s: marine insurance question does not cite the Marine '
                                 'Insurance Act 1963 in regulations (trap 8)' % (pid, q['q_no']))
                if re.search(r'\b1906\b', regs) and '1963' not in regs:
                    fails.append('%s %s: cites the UK 1906 Act as governing (trap 8)'
                                 % (pid, q['q_no']))

        # T12: HATC must never appear as a source for any question.
        checked += 1
        for q in d['questions']:
            for src in (q.get('sources') or []):
                if 'hatc' in src.lower() and 'not used' not in src.lower():
                    fails.append('%s %s: HATC appears in sources (trap 12)' % (pid, q['q_no']))

        # T10: ammonia content must not be recorded as zero-emission.
        checked += 1
        for q in d['questions']:
            al = ' '.join(q.get('search_aliases') or []).lower()
            if 'ammonia' in al and q.get('model_answer'):
                qr = q.get('quick_revision') or {}
                blob = (qr.get('recall_15s', '') + ' ' + qr.get('major_trap', '')).lower()
                if 'n2o' not in blob and 'slip' not in blob:
                    fails.append('%s %s: ammonia quick-revision names neither N2O nor slip, so the '
                                 'zero-emission qualification may be missing (trap 10)'
                                 % (pid, q['q_no']))

        # T13: provenance must not claim official verification.
        checked += 1
        if d.get('official_source_verified') is True and not d.get('official_source_verification_note'):
            fails.append('%s: official_source_verified true with no note (trap 13)' % pid)

    return fails, checked


def self_test(traps, specs):
    """Positive control: inject each grep trap and assert the checker fires."""
    print('  self-test: injecting each auto-scannable trap phrase')
    bad = []
    for num, title, phrase, scope in traps:
        if not phrase:
            continue
        f, _ = grep_layer([(num, title, phrase, scope)],
                          extra_text='lorem ipsum %s dolor sit amet' % phrase)
        if not f:
            bad.append('trap %s (%s) did NOT fire on an injected copy' % (num, title[:50]))
    # structural positive control: strip Q7's reverify list and expect a failure
    import copy
    s2 = copy.deepcopy(specs)
    hit = False
    for d in s2:
        for q in d['questions']:
            if 'Merchant Shipping Act 2025' in (q.get('short_title') or ''):
                q['reverify_before_publication'] = []
                hit = True
    if hit:
        f, _ = structural_layer(s2)
        if not any('trap 11' in x for x in f):
            bad.append('structural trap 11 did NOT fire when the reverify list was emptied')
    for b in bad:
        print('  [SELFTEST FAIL] %s' % b)
    print('  self-test: %s' % ('FAILED' if bad else 'all injected traps fired'))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    if not os.path.exists(TRAPS_MD):
        print('[ERROR] known_traps.md not found at %s' % TRAPS_MD)
        sys.exit(1)

    traps = parse_traps(TRAPS_MD)
    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))]

    auto = [t for t in traps if t[2]]
    manual = [t for t in traps if not t[2]]

    gf, gc = grep_layer(traps)
    sf, sc = structural_layer(specs)

    print('KNOWN TRAPS -- Past Written Papers')
    print('  %d trap(s) recorded: %d auto-scanned, %d manual-review-only (GREP: SKIP)'
          % (len(traps), len(auto), len(manual)))
    print('  scanned %d file(s); %d structural assertion group(s)'
          % (len(scannable_files()), sc))
    for num, title, _, _s in manual:
        print('  [manual] trap %s: %s' % (num, title[:80]))

    st_fail = self_test(traps, specs) if args.self_test else []

    fails = gf + sf + st_fail
    print()
    for f in fails:
        print('  [FAIL ] %s' % f)
    print('known traps: %d check(s), %d failure(s)' % (gc + sc, len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
