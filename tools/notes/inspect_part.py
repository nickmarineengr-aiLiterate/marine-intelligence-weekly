#!/usr/bin/env python3
"""Inspect an existing miw-notes-mgmt Part file and print its structural metadata.
Usage: python inspect_part.py <path-to-part.html>
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def strip(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def main(path):
    h = open(path, encoding='utf-8').read()
    print('FILE      :', os.path.basename(path))
    print('BYTES     :', len(h.encode('utf-8')))
    m = re.search(r'<title>(.*?)</title>', h, re.S)
    print('TITLE     :', strip(m.group(1)) if m else '-')
    print('CANONICAL :', re.findall(r'rel="canonical"\s+href="([^"]+)"', h))
    print('ROBOTS    :', re.findall(r'name="robots"\s+content="([^"]+)"', h))
    print('GATED     :', 'miw_auth' in h)
    print('GA4       :', 'G-0YEE2CBNP5' in h)
    for cls in ('notes-badge', 'page-sub', 'header-meta'):
        v = re.findall(r'class="' + cls + r'"[^>]*>(.*?)</', h, re.S)
        print((cls.upper() + '        ')[:10] + ':', strip(v[0])[:160] if v else '-')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    print('H1        :', strip(m.group(1)) if m else '-')
    ids = re.findall(r'id="topic-(\d+)"', h)
    print('TOPIC IDS :', ids)
    for tid, blk in zip(ids, re.split(r'<div class="topic-block"', h)[1:]):
        m = re.search(r'<h2[^>]*>(.*?)</h2>', blk, re.S)
        meta = re.findall(r'class="topic-meta"[^>]*>(.*?)</div>', blk, re.S)
        print('  T' + tid + ': ' + (strip(m.group(1)) if m else '?'))
        if meta:
            print('       meta: ' + strip(meta[0])[:180])
    print('SECTION CLASSES USED:')
    print(' ', sorted(set(re.findall(r'class="([a-z0-9\- ]+)"', h))))

if __name__ == '__main__':
    main(sys.argv[1])
