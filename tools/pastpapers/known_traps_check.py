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
#
# WORKFLOW_LESSONS.md is exempt for the same reason and no more: it is a
# registry, not product prose, and a lesson ABOUT a trap has to be able to name
# the wrong phrase. It records, for instance, why trap 1 was kept at full
# strength after QP2601 Q4 hit it on a correct statement -- which cannot be
# written without quoting it. Neither file is ever served to a candidate.
EXEMPT_PATHS = ('known_traps.md', 'WORKFLOW_LESSONS.md')
EXEMPT_DIRS = ('verification',)


# trap 18. `ISM` as a whole uppercase token, an optional `Code`, then a numbered
# reg in any spelling. Case-sensitive on ISM by design: lowercasing would let
# "mechanism regulates 3 valves" through the same gate.
ISM_WRONG_UNIT = re.compile(
    r'\bISM\b(?:\s+Code)?\s*,?\s*\b[Rr]eg(?:ulations?|s)?\b\.?\s*[0-9]')


# trap 19. A.1184(33) attributed to the ISM Code.
#
# A.1184(33) is the Guidelines on places of refuge for ships in need of
# assistance. The 33rd Assembly's ISM implementation guidance is A.1188(33),
# which revoked A.1118(30). Both were adopted on 6 December 2023, four digits
# apart, and the corpus amendment register files the places-of-refuge PDF under
# the ISM Code -- which is how the wrong attribution reached two papers.
#
# This cannot be a phrase match in either direction: A.1184(33) is CORRECT in
# five other papers, and the sentences that correct the defect have to name the
# ISM Code in order to deny it. The discriminator is therefore contextual --
# an ISM marker near the citation, with no places-of-refuge marker to disarm it.
A1184 = re.compile(r'A\.1184\(33\)')
A1184_ISM_MARKER = re.compile(r'\bISM\b|safety management', re.I)
# Hyphenated because the house forms are both "places of refuge" and the
# adjectival "places-of-refuge guidelines".
A1184_POR_MARKER = re.compile(r'places?[-\s]of[-\s]refuge', re.I)
# Wide enough that a correcting passage may put the denial and the true subject
# in separate sentences, which every corrected occurrence in the corpus does.
A1184_WINDOW = 300


def _strings(obj, path=''):
    """Yield (json path, string) for every string anywhere under obj."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            for r in _strings(v, '%s.%s' % (path, k)):
                yield r
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for r in _strings(v, '%s[%d]' % (path, i)):
                yield r
    elif isinstance(obj, str):
        yield path.lstrip('.'), obj


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
    # Committed documentation under docs/, for trap 14 in particular. The scan
    # used to stop at pages, specs and the manifest, and a tracked design draft
    # under docs/ named the source-copy host twice in ordinary prose -- a
    # published brand trace in a public repository that nothing was looking for.
    # The source PDFs themselves live in the same directory and are git-ignored;
    # they are excluded here because scanning a file that can never be committed
    # would fail the build for a file nobody can fix.
    for p in sorted(glob.glob(os.path.join(PP, 'docs', '*.md'))):
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
            # SCOPE narrows a trap to the surfaces it is actually about.
            #
            #   html      generated pages only
            #   product   pages, specs and the manifest -- everything a student
            #             can fetch, but not design documentation. A doc that
            #             DISCUSSES a wrong formulation in order to forbid it is
            #             not committing it, which is the same reasoning that
            #             already exempts known_traps.md itself.
            #   all       (default) every scanned file. Brand traces are this:
            #             the repository is public, so a host name is a published
            #             trace wherever it sits.
            if name != '<injected>':
                if scope == 'html' and not name.endswith('.html'):
                    continue
                if scope == 'product' and name.endswith('.md'):
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
        #
        # Match HATC as a WORD, not as a substring. A bare `'hatc' in src` also
        # fires on 'hatches' -- unavoidable the moment a question quotes
        # York-Antwerp Rule II ("water which goes down a ship's hatches opened
        # for the purpose of making a jettison"). QP2403 Q3 tripped it exactly
        # that way. The word-boundary form still catches every genuine
        # reference -- "HATC", "HATC's", "HATC-sourced" -- because the boundary
        # falls on a non-word character in each case.
        checked += 1
        for q in d['questions']:
            for src in (q.get('sources') or []):
                if re.search(r'\bHATC\b', src, re.I) and 'not used' not in src.lower():
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

        # T18: the ISM Code is cited in elements and paragraphs, never regulations.
        #
        # The grep layer already owns the `ISM Code reg...` prefix, which is safe
        # as a literal because no English word ends in "ISM Code". This covers the
        # form a literal cannot: the un-prefixed `ISM reg 9`, where a bare
        # `ism reg` substring would fire on "mechanism regulates". QP2310-Q9 shipped
        # exactly that abbreviation for a week after its prefixed occurrences were
        # purged, so the abbreviation is the form that actually survives a fix.
        #
        # ISM must be a whole UPPERCASE token, followed only by an optional "Code"
        # and then a numbered reg. No other instrument's citation can satisfy that,
        # and `SOLAS regulation XI-1/6` cannot -- it carries no ISM and its number
        # is not a digit.
        checked += 1
        for q in d['questions']:
            for path, s in _strings(q):
                m = ISM_WRONG_UNIT.search(s)
                if m:
                    fails.append('%s %s: %r at %s -- the ISM Code has elements and '
                                 'paragraphs, not regulations (trap 18)'
                                 % (pid, q['q_no'], m.group(0), path))

        # T19: A.1184(33) is places of refuge, never ISM guidance.
        checked += 1
        for q in d['questions']:
            for path, s in _strings(q):
                for m in A1184.finditer(s):
                    w = s[max(0, m.start() - A1184_WINDOW):m.end() + A1184_WINDOW]
                    if A1184_ISM_MARKER.search(w) and not A1184_POR_MARKER.search(w):
                        fails.append('%s %s: A.1184(33) in an ISM context at %s -- '
                                     'A.1184(33) is the Guidelines on places of refuge; '
                                     'the ISM implementation guidance is A.1188(33), '
                                     'which revoked A.1118(30) (trap 19)'
                                     % (pid, q['q_no'], path))

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

    # structural positive control for trap 18: inject the abbreviated form the
    # grep layer cannot see, and the legitimate SOLAS citation beside it. The
    # first must fire; the second must not, or the trap would purge correct law.
    s3 = copy.deepcopy(specs)
    s3[0]['questions'][0]['short_title'] = 'ISM reg 9 and SOLAS regulation XI-1/6'
    f, _ = structural_layer(s3)
    if not any('trap 18' in x for x in f):
        bad.append('structural trap 18 did NOT fire on an injected "ISM reg 9"')
    s4 = copy.deepcopy(specs)
    s4[0]['questions'][0]['short_title'] = (
        'SOLAS regulation XI-1/6, MARPOL Annex VI regulation 22, and the '
        'mechanism regulating 3 valves')
    f, _ = structural_layer(s4)
    if any('trap 18' in x for x in f):
        bad.append('structural trap 18 fired on legitimate SOLAS/MARPOL regulation text')

    # Trap 19 controls, both taken verbatim from real corpus text rather than
    # invented, so the guard is proved against the wording that actually shipped
    # and against the wording that must survive it.
    #
    # POSITIVE: QP2502-Q3's shipped model answer, live for weeks.
    s5 = copy.deepcopy(specs)
    s5[0]['questions'][0]['short_title'] = (
        'the flag Administration verifies and certifies, following the Revised '
        'Guidelines on implementation of the ISM Code by Administrations, '
        'resolution A.1184(33)')
    f, _ = structural_layer(s5)
    if not any('trap 19' in x for x in f):
        bad.append('structural trap 19 did NOT fire on the shipped ISM attribution '
                   'of A.1184(33)')
    # NEGATIVE: QP2507-Q9's correct places-of-refuge citation, which must not be
    # disturbed, and a correcting sentence that has to name the ISM Code to deny it.
    s6 = copy.deepcopy(specs)
    s6[0]['questions'][0]['short_title'] = (
        'decide refuge under A.1184(33), Guidelines on places of refuge for ships '
        'in need of assistance, adopted 6 December 2023 and revoking A.949(23)')
    s6[0]['questions'][1]['short_title'] = (
        'A.1184(33), which the corpus register files against the ISM Code, is in '
        'fact the Guidelines on places of refuge and is not cited here')
    f, _ = structural_layer(s6)
    if any('trap 19' in x for x in f):
        bad.append('structural trap 19 fired on a legitimate places-of-refuge '
                   'citation or on a sentence correcting the defect')
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
