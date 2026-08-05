#!/usr/bin/env python3
"""Validate a Part content spec: JSON syntax + required keys per topic.
Usage: python validate_spec.py <spec.json>
"""
import io, json, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOP = ['part', 'prev_part', 'prev_pages', 'pages', 'title_topics',
       'meta_description', 'page_sub', 'qb_links', 'topics']
TOPIC = ['n', 'toc', 'title', 'tag', 'pages', 'examiner',
         'definition', 'why', 'qa', 'exam', 'memory', 'refs']


def main(path):
    raw = open(path, encoding='utf-8').read()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError as e:
        line = raw.splitlines()[e.lineno - 1] if e.lineno <= len(raw.splitlines()) else ''
        print('JSON ERROR: %s' % e)
        print('  line %d col %d' % (e.lineno, e.colno))
        print('  >> %s' % line[max(0, e.colno - 80):e.colno + 80])
        sys.exit(1)
    errs = []
    for k in TOP:
        if k not in d:
            errs.append('missing top-level key: %s' % k)
    ns = []
    for t in d.get('topics', []):
        ns.append(t.get('n'))
        for k in TOPIC:
            if k not in t:
                errs.append('topic %s: missing key %s' % (t.get('n'), k))
        if len(t.get('qa', [])) < 3:
            errs.append('topic %s: fewer than 3 Q&A items' % t.get('n'))
        if len(t.get('exam', [])) < 3:
            errs.append('topic %s: fewer than 3 written-exam questions' % t.get('n'))
        if not t.get('verify'):
            print('  [WARN ] topic %s has no verification note' % t.get('n'))
    if ns != list(range(1, len(ns) + 1)):
        errs.append('topic numbers not sequential from 1: %s' % ns)
    print('SPEC   :', path)
    print('PART   :', d.get('part'), '| pages', d.get('pages'), '| topics', ns)
    for e in errs:
        print('  [ERROR]', e)
    print('  [OK   ] spec valid' if not errs else '  %d error(s)' % len(errs))
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main(sys.argv[1])
