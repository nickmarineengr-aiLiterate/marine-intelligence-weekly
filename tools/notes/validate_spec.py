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
# Source-page series (spec["series"]["profile"] == "source-pages", e.g. LOHAN):
# concise by design, so written-exam and memory blocks appear only where they
# earn their place; every topic must instead cite its source PDF pages.
TOPIC_SRC = ['n', 'toc', 'title', 'tag', 'pages', 'definition', 'qa', 'refs']
# examiner is optional here: shown only when MIW's examiner corpus supports it.
VERIFY_SOFT_MAX = 450  # chars; candidate-facing notes stay short, detail lives in the register


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
    src = (d.get('series') or {}).get('profile') == 'source-pages'
    for t in d.get('topics', []):
        ns.append(t.get('n'))
        for k in (TOPIC_SRC if src else TOPIC):
            if k not in t:
                errs.append('topic %s: missing key %s' % (t.get('n'), k))
        if src:
            if not t.get('qa'):
                errs.append('topic %s: no oral Q&A item' % t.get('n'))
            if 'PDF pp.' not in str(t.get('pages', '')) and 'PDF p.' not in str(t.get('pages', '')):
                errs.append('topic %s: pages must cite source "PDF pp. a–b"' % t.get('n'))
            if len(t.get('verify', '')) > VERIFY_SOFT_MAX:
                print('  [WARN ] topic %s verify note %d chars (> %d)' % (t.get('n'), len(t['verify']), VERIFY_SOFT_MAX))
            continue
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
