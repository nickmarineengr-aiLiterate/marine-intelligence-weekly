#!/usr/bin/env python3
"""Health check for miw-notes-mgmt Part files.

Checks:
  1. HTML tag balance (stack-based, void elements excluded)
  2. Mandatory head blocks: robots noindex, GA4, canonical matching filename
  3. Gate script present/absent (reports state; --require-gate to enforce)
  4. Topic block structure: id sequence, mandatory sections present
  5. Source-draft artifacts: [cite: N], LaTeX ($...$, \\frac), TODO, placeholder
  6. Sidebar TOC anchors resolve to real topic ids
  7. Encoding: no mojibake sequences (Ã, â€, ï¿½)

Usage: python health_check.py <file.html> [more.html ...] [--require-gate]
Exit code 1 if any ERROR is raised.
"""
import io, os, re, sys
from html.parser import HTMLParser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}
# '🎯 Oral Q&' matches both the legacy raw-ampersand form and the escaped form.
MANDATORY_SECTIONS = ['📖 Definition', '⚓ Why It Matters', '🎯 Oral Q&',
                      '✍ Written Exam Focus', '🧠 Memory Box', '📚 References']
# Source-page series (LOHAN, "MIW MEO Class 1 Engineering Study Standard"): concise profile.
# Founder decision 15 Oct 2026: the historical source is acknowledged only in disclaimer
# clause 2, so a page must NOT display source-PDF page citations (FORBIDDEN_SOURCE). The
# provenance itself stays mandatory in the private spec: validate_spec.py fails any topic
# whose "pages" field does not cite its source pages.
SOURCE_SERIES = ('lohan-notes-p',)
MANDATORY_SOURCE = ['📖 Definition', '🎯 Oral Q&', '📚 References']
FORBIDDEN_SOURCE = ['PDF p']


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append('stray </%s> at line %d' % (tag, self.getpos()[0]))
            return
        top, pos = self.stack.pop()
        if top != tag:
            self.errors.append('mismatch: <%s> opened line %d closed by </%s> line %d'
                               % (top, pos[0], tag, self.getpos()[0]))


def check(path, require_gate=False):
    errs, warns = [], []
    h = open(path, encoding='utf-8').read()
    name = os.path.basename(path)

    b = Balance()
    b.feed(h)
    errs += ['TAG: ' + e for e in b.errors]
    if b.stack:
        errs += ['TAG: unclosed <%s> opened line %d' % (t, p[0]) for t, p in b.stack[-8:]]

    if 'noindex, nofollow, noarchive, nosnippet' not in h:
        errs.append('HEAD: robots noindex meta missing')
    if 'G-0YEE2CBNP5' not in h:
        errs.append('HEAD: GA4 tag missing')
    canon = re.findall(r'rel="canonical" href="([^"]+)"', h)
    if not canon:
        errs.append('HEAD: canonical missing')
    elif not canon[0].endswith('/meoclass1/oralnotes/' + name):
        errs.append('HEAD: canonical %s does not match /meoclass1/oralnotes/%s' % (canon[0], name))

    gated = 'miw_auth=1' in h
    if require_gate and not gated:
        errs.append('GATE: gate script missing (--require-gate)')

    ids = re.findall(r'id="topic-p(\d+)-(\d+)"', h)
    if not ids:
        errs.append('TOPIC: no topic blocks found')
    else:
        parts = {a for a, _ in ids}
        if len(parts) != 1:
            errs.append('TOPIC: mixed part numbers in ids: %s' % sorted(parts))
        nums = [int(b) for _, b in ids]
        if nums != list(range(1, len(nums) + 1)):
            errs.append('TOPIC: id sequence not 1..N: %s' % nums)
        fpart = re.search(r'-p(\d+)\.html$', name)
        if fpart and fpart.group(1) not in parts:
            errs.append('TOPIC: ids say part %s, filename says p%s' % (sorted(parts), fpart.group(1)))

    for blk in re.split(r'<div class="topic-block"', h)[1:]:
        tid = re.search(r'id="(topic-p\d+-\d+)"', blk)
        tid = tid.group(1) if tid else '?'
        for s in (MANDATORY_SOURCE if name.startswith(SOURCE_SERIES) else MANDATORY_SECTIONS):
            if s not in blk:
                errs.append('TOPIC %s: missing mandatory section "%s"' % (tid, s))
        if name.startswith(SOURCE_SERIES):
            for s in FORBIDDEN_SOURCE:
                if s in blk:
                    errs.append('TOPIC %s: displays a source citation "%s" (provenance lives in the private spec)' % (tid, s))
        if 'class="verify-note"' not in blk:
            warns.append('TOPIC %s: no verify-note (OK only if nothing needed correction)' % tid)
        if 'class="ce-tip"' not in blk:
            warns.append('TOPIC %s: no CE Oral Tip' % tid)
        if 'class="reg-box"' not in blk:
            warns.append('TOPIC %s: no regulatory reference box' % tid)

    for pat, msg in [(r'\[cite[:_]', 'raw [cite:] marker'),
                     (r'\\frac|\\times|\\text\{|\$\$', 'LaTeX artifact'),
                     (r'\bTODO\b|\bTBD\b|\bXXX\b|\blorem ipsum\b', 'placeholder text'),
                     (r'\{\{[a-z_]+\}\}', 'unfilled template placeholder'),
                     (r'Ã.|â€|ï¿½', 'mojibake / encoding damage')]:
        for m in re.finditer(pat, h, re.I):
            errs.append('ARTIFACT: %s near "...%s..."'
                        % (msg, h[max(0, m.start() - 40):m.start() + 40].replace('\n', ' ')))
            break

    anchors = set(re.findall(r'class="toc-link" href="#([^"]+)"', h))
    real = set(re.findall(r'id="(topic-p\d+-\d+)"', h))
    for a in sorted(anchors - real):
        errs.append('TOC: anchor #%s has no matching topic id' % a)
    for r in sorted(real - anchors):
        warns.append('TOC: topic %s has no sidebar link' % r)

    print('=' * 68)
    print('%s  (%d bytes, %d topics, gated=%s)'
          % (name, len(h.encode('utf-8')), len(ids), gated))
    for w in warns:
        print('  [WARN ]', w)
    for e in errs:
        print('  [ERROR]', e)
    if not errs:
        print('  [OK   ] no errors')
    return len(errs)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    rg = '--require-gate' in sys.argv
    total = sum(check(p, rg) for p in args)
    print('=' * 68)
    print('TOTAL ERRORS:', total)
    sys.exit(1 if total else 0)
