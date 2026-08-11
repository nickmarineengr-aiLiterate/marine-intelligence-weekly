"""Deterministic tests for the True Source consumer adapter.

Positive AND negative controls, because the dangerous failures here are silent
ones: a wrong chapter that resolves anyway, a structural label rendered as if it
were the regulation, an uncleared instrument leaking text, or a bulk-export path
nobody noticed was reachable.

Skips cleanly when the private corpus is not on the machine -- the corpus is a
separate private repository and is deliberately absent from deployment hosts.

    python tools/corpus/consumer_adapter_test.py
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import consumer_adapter as ca  # noqa: E402

FAIL = []
RUN = [0]


def check(name, cond, detail=''):
    RUN[0] += 1
    if cond:
        print('  PASS  %s' % name)
    else:
        print('  FAIL  %s   %s' % (name, detail))
        FAIL.append(name)


def main():
    if not ca.available():
        print('True Source corpus not present (%s unset and no default root).'
              % ca.ENV_ROOT)
        print('SKIP -- nothing to test. This is not a failure.')
        return 0

    root = ca.corpus_root()
    print('corpus root: %s' % root)

    # -- Frozen source must not be mutated by anything we do -------------------
    lsa_path = os.path.join(root, ca.LSA_REL)
    fss_path = os.path.join(root, ca.FSS_REL)
    before = {p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
              for p in (lsa_path, fss_path)}

    print('\n-- LSA: cleared, frozen, text-bearing --')
    r = ca.resolve('LSA-1.1.1')
    check('LSA-1.1.1 resolves', r['resolution'] == ca.RESOLVED, r['resolution'])
    check('LSA-1.1.1 rights cleared', r['rights_cleared'])
    check('LSA-1.1.1 text available', r['text_available'])
    check('LSA-1.1.1 text adequate', r['text_adequate'])
    check('LSA-1.1.1 quotable', r['quotable'], r['why_not_quotable'] or '')
    check('LSA-1.1.1 carries wording', 'Convention' in (r['text'] or ''))
    check('LSA-1.1.1 in chapter context', r['chapter'] == 'I', str(r['chapter']))
    check('LSA-1.1.1 has next (prev/next navigation)', r['next'] is not None)
    check('LSA-1.1.1 carries source provenance', bool(r['source_pages']))
    check('LSA-1.1.1 carries non-official notice',
          'not an official IMO publication' in (r['non_official_notice'] or ''))
    check('LSA-1.1.1 carries build identity', bool(r['build_id']))

    # -- NEGATIVE: an id with no corpus object must not be invented ------------
    print('\n-- negative controls --')
    r = ca.resolve('LSA-99.99.99')
    check('missing LSA provision is NOT_FOUND', r['resolution'] == ca.NOT_FOUND)
    check('missing LSA provision yields no text', r['text'] is None)
    check('missing LSA provision is not quotable', not r['quotable'])

    # -- NEGATIVE: an instrument outside the three cleared corpora -------------
    r = ca.resolve('SOLAS-II2-10')
    check('SOLAS is UNSUPPORTED_INSTRUMENT', r['resolution'] == ca.UNSUPPORTED_INSTRUMENT)
    check('SOLAS yields no text', r['text'] is None)
    check('SOLAS not quotable', not r['quotable'])

    # -- FSS: chapter is part of identity -------------------------------------
    print('\n-- FSS: chapter is part of the identity --')
    # 2.1 is a text-bearing provision in chapters 1, 2 and 3 -- and a container
    # in chapter 5. An FSS reference without its chapter is genuinely ambiguous.
    a = ca.resolve('FSSCode-1-2.1')
    b = ca.resolve('FSSCode-3-2.1')
    check('FSS 1/2.1 resolves', a['resolution'] == ca.RESOLVED)
    check('FSS 3/2.1 resolves', b['resolution'] == ca.RESOLVED)
    check('same number in different chapters is a DIFFERENT object',
          a['chapter'] != b['chapter'] and a['text'] != b['text'],
          '%s vs %s' % (a['citation'], b['citation']))
    check('FSS is NOT verbatim-quotable (it is a summary derivative)',
          not a['quotable'] and a['text_nature'] == ca.SUMMARY,
          '%s / %s' % (a['text_nature'], a['why_not_quotable']))
    check('FSS refusal names the summary nature',
          'summary' in (a['why_not_quotable'] or ''), a['why_not_quotable'])
    check('FSS still usable as evidence (text present, resolution good)',
          bool(a['text']) and a['resolution'] == ca.RESOLVED)
    check('FSS carries chapter title', bool(a['chapter_title']))
    check('FSS carries build id', a['build_id'] == 'MIW-FSS-2026.08.08-BUILD-2',
          str(a['build_id']))
    check('FSS has prev/next navigation', a['next'] is not None)

    # GUARD. The FSS text_nature block is derived from the artifact's OWN
    # embedded disclaimer. If a future FSS build carries genuine verbatim text,
    # this assertion fails on purpose, forcing the classification to be re-read
    # rather than leaving a stale block in place.
    check('FSS derivative still self-declares its wording a summary',
          'NOT the official text' in (a['non_official_notice'] or ''),
          (a['non_official_notice'] or '')[:120])

    # -- container node: addressable, cited, NOT quotable ---------------------
    c = ca.resolve('FSSCode-5-2.1')
    check('FSS container node resolves', c['resolution'] == ca.RESOLVED)
    check('FSS container node is a heading', c['structural_role'] == 'heading',
          str(c['structural_role']))
    check('FSS container node is NOT quotable', not c['quotable'])
    check('container refusal says cite the paragraphs beneath it',
          'beneath it' in (c['why_not_quotable'] or ''), c['why_not_quotable'])

    # -- NEGATIVE: wrong chapter must not silently resolve --------------------
    r = ca.resolve('FSSCode-17-2.5.1.11')   # exists in chapter 9, not 17
    check('wrong chapter does not silently resolve',
          r['resolution'] == ca.NOT_FOUND, r['resolution'])

    # -- NEGATIVE: structural label must never be quoted as the regulation ----
    print('\n-- FSS: label stubs must not be presented as wording --')
    r = ca.resolve('FSSCode-9-1.2.1')       # text == 'Section'
    check('label stub still resolves', r['resolution'] == ca.RESOLVED)
    check('label stub reports text_available', r['text_available'])
    check('label stub reports text NOT adequate', not r['text_adequate'])
    check('label stub is NOT quotable', not r['quotable'])
    check('label stub flagged text_adequate False', not r['text_adequate'])
    # FSS is blocked at the more fundamental summary level before adequacy is
    # ever reached, so the reported reason is the summary one. The adequacy gate
    # still matters: it is what would stop a stub if FSS were ever rebuilt as
    # verbatim text, and it is asserted directly above.
    check('label stub explains why', bool(r['why_not_quotable']), r['why_not_quotable'])

    # -- MARPOL Annex VI: right to quote WITHOUT text to quote ----------------
    print('\n-- MARPOL Annex VI: addressable, cited, but no text object --')
    r = ca.resolve('MARPOL-VI-14')
    check('MARPOL-VI-14 resolves via resolver', r['resolution'] == ca.RESOLVED)
    check('MARPOL-VI-14 has a citation', bool(r['citation']))
    check('MARPOL-VI-14 has NO text', not r['text_available'])
    check('MARPOL-VI-14 is NOT quotable', not r['quotable'])
    check('MARPOL non-quotable reason names the derivative gap',
          'derivative' in (r['why_not_quotable'] or '').lower(),
          r['why_not_quotable'])

    r = ca.resolve('MARPOL-VI-14-146')
    check('MARPOL paragraph object resolves', r['resolution'] == ca.RESOLVED)
    check('MARPOL paragraph has no text', r['text'] is None)

    # -- alias resolves IN to the canonical id, never out ---------------------
    r = ca.resolve('MEPC32876-3-14')
    check('MEPC32876 alias resolves', r['resolution'] == ca.RESOLVED)
    check('alias normalises to canonical id', r['object_id'] == 'MARPOL-VI-14',
          str(r['object_id']))

    r = ca.resolve('MARPOL-VI-999')
    check('unknown MARPOL id is NOT_FOUND', r['resolution'] == ca.NOT_FOUND)

    # -- rights are READ, not hard-coded --------------------------------------
    print('\n-- rights state is read from the register --')
    s = ca.rights_state('MARPOL-VI')
    check('FD-RIGHTS-1 found', s['decision'] == 'FD-RIGHTS-1')
    check('FD-RIGHTS-1 ACTIVE', s['status'] == 'ACTIVE')
    check('MARPOL cleared in principle', s['cleared'])
    check('MARPOL NOT operative today', not s['operative_today'])
    check('R2 reservation surfaced for MARPOL', 'FD-RIGHTS-1-R2' in s['reservations'],
          str(s['reservations']))

    s = ca.rights_state('FSS')
    check('FSS operative today', s['operative_today'])
    check('FSS carries reservation R1', 'FD-RIGHTS-1-R1' in s['reservations'],
          str(s['reservations']))

    s = ca.rights_state('LSA')
    check('LSA operative today', s['operative_today'])

    # -- bulk export is not reachable -----------------------------------------
    print('\n-- bulk export is structurally refused --')
    try:
        ca.resolve_chapter('FSS', '9')
        check('chapter-level retrieval refused', False, 'it returned instead of raising')
    except NotImplementedError as e:
        check('chapter-level retrieval refused', True)
        check('refusal cites FD-RIGHTS-1', 'FD-RIGHTS-1' in str(e))

    # -- frozen corpus unchanged ----------------------------------------------
    print('\n-- frozen corpus integrity --')
    for p, h in before.items():
        now = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        check('frozen file unmodified: %s' % os.path.basename(p), now == h)

    print('\n%d checks, %d failure(s)' % (RUN[0], len(FAIL)))
    if FAIL:
        for f in FAIL:
            print('  FAILED: %s' % f)
        return 1
    print('CORPUS CONSUMER TESTS PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
