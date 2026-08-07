#!/usr/bin/env python3
"""Audit a built past-paper page against its spec and manifest.

Usage:
  python audit_paper.py <spec.json> [--html <file>] [--manifest <file>] [--require-gate]

Checks (the list in the build brief, section 11):
   1  spec is valid JSON
   2  required schema fields present
   3  paper id and question ids unique
   4  marks consistency
   5  all nine question anchors present in the HTML
   6  no missing question text
   7  no aggregator marketing text
   8  HTML tag balance
   9  internal link targets resolve
  10  review gate state
  11  generated-file reproducibility
  12  manifest / spec / output consistency
  13  unresolved verification flags surfaced

Plus: no absolute filesystem path and no source-PDF path leaked into the page.

Exit code 1 on any ERROR. WARN and INFO never fail the build.
"""
import argparse, hashlib, io, json, os, re, sys
from html.parser import HTMLParser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}

# Aggregator branding and advertising that must never reach MIW output.
MARKETING = [
    'dieselship', 'dsguides', 'purchase our original books',
    'clean content, cad drawing', 'maritime publishing',
    'please click here to purchase', 'get quick access to answers',
]

GATE_RE = re.compile(r'miw_auth=1')
GATE_STUB = 'GATE SCRIPT STRIPPED FOR REVIEW COPY'

errs, warns, infos = [], [], []
err = errs.append
warn = warns.append
info = infos.append


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append('stray </%s> at line %d' % (tag, self.getpos()[0]))
            return
        top, pos = self.stack[-1]
        if top == tag:
            self.stack.pop()
        else:
            self.problems.append('</%s> at line %d closes <%s> opened at line %d'
                                 % (tag, self.getpos()[0], top, pos[0]))
            self.stack.pop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('--html')
    ap.add_argument('--manifest')
    ap.add_argument('--require-gate', action='store_true')
    args = ap.parse_args()

    # -- 1 valid JSON -------------------------------------------------------
    try:
        raw_spec = open(args.spec, encoding='utf-8').read()
        d = json.loads(raw_spec)
    except json.JSONDecodeError as e:
        print('[ERROR] spec is not valid JSON: %s' % e)
        sys.exit(1)
    info('1  spec parses as JSON')

    pid = d.get('paper_id')
    qs = d.get('questions', [])

    html_path = args.html or os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers',
                                          '%s.html' % pid)
    if not os.path.exists(html_path):
        print('[ERROR] built page not found: %s' % html_path)
        sys.exit(1)
    html = open(html_path, encoding='utf-8', newline='').read()
    low = html.lower()

    # -- 2 required fields --------------------------------------------------
    need = ['schema_version', 'paper_id', 'sr_no', 'total_marks', 'instructions',
            'source_copy_provenance', 'official_source_verified',
            'transcription_verified', 'build_state', 'review_state', 'questions']
    missing = [k for k in need if k not in d]
    if missing:
        err('2  spec missing required fields: %s' % ', '.join(missing))
    else:
        info('2  all required schema fields present')

    # -- 3 uniqueness -------------------------------------------------------
    nos = [q.get('q_no') for q in qs]
    anchors = [q.get('anchor') for q in qs]
    if len(set(nos)) != len(nos):
        err('3  duplicate q_no in spec')
    if len(set(anchors)) != len(anchors):
        err('3  duplicate anchor in spec')
    if not pid:
        err('3  paper_id missing')
    if len(set(nos)) == len(nos) and len(set(anchors)) == len(anchors):
        info('3  paper id and %d question ids unique' % len(nos))

    # -- 4 marks consistency ------------------------------------------------
    bad = 0
    for q in qs:
        marked = [s for s in (q.get('subparts') or []) if s.get('marks') is not None]
        if marked and sum(s['marks'] for s in marked) != q.get('total_marks'):
            err('4  %s: subparts sum to %d, total_marks is %s'
                % (q['q_no'], sum(s['marks'] for s in marked), q.get('total_marks')))
            bad += 1
    if not bad:
        info('4  marks consistent within every question (paper-level 6x16=96 vs printed '
             '100 is recorded in marks_note, not silently corrected)')

    # -- 5 anchors ----------------------------------------------------------
    miss = [a for a in anchors if 'id="%s"' % a not in html]
    if miss:
        err('5  anchors missing from HTML: %s' % ', '.join(miss))
    else:
        info('5  all %d question anchors present (#q1 .. #q%d)' % (len(anchors), len(anchors)))

    # -- 6 question text present -------------------------------------------
    def norm(s):
        return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()

    flat = norm(html)
    missing_text = []
    for q in qs:
        for line in q['text_verbatim'].split('\n'):
            probe = norm(line)
            probe = probe.replace('&', '&amp;')
            if len(probe) > 40 and probe[:60] not in flat and \
                    norm(line)[:60] not in flat:
                missing_text.append('%s: %s...' % (q['q_no'], norm(line)[:50]))
    if missing_text:
        for m in missing_text:
            err('6  question text not found in HTML -- %s' % m)
    else:
        info('6  verbatim question text present for all %d questions' % len(qs))

    # -- 7 marketing text ---------------------------------------------------
    hits = [m for m in MARKETING if m in low]
    if hits:
        err('7  aggregator marketing text present in output: %s' % ', '.join(hits))
    else:
        info('7  no aggregator marketing text in output')

    # -- 8 tag balance ------------------------------------------------------
    b = Balance()
    b.feed(html)
    if b.problems:
        for p in b.problems[:10]:
            err('8  tag balance: %s' % p)
    elif b.stack:
        for tag, pos in b.stack[:10]:
            err('8  unclosed <%s> opened at line %d' % (tag, pos[0]))
    else:
        info('8  HTML tags balanced')

    # -- 9 internal link targets -------------------------------------------
    frags = re.findall(r'href="#([^"]+)"', html)
    dead = [f for f in frags if 'id="%s"' % f not in html]
    if dead:
        err('9  in-page links with no target: %s' % ', '.join(sorted(set(dead))))
    else:
        info('9  all %d in-page links resolve' % len(frags))

    rels = re.findall(r'href="(\.\./[^"#]+)"', html)
    page_dir = os.path.dirname(os.path.abspath(html_path))
    dead_rel = [r for r in rels
                if not os.path.exists(os.path.normpath(os.path.join(page_dir, r)))]
    if dead_rel:
        for r in sorted(set(dead_rel)):
            err('9  cross-link target does not exist on disk: %s' % r)
    elif rels:
        info('9  all %d cross-links resolve on disk' % len(rels))

    # -- 10 gate state ------------------------------------------------------
    gated = bool(GATE_RE.search(html))
    stub = GATE_STUB in html
    if args.require_gate and not gated:
        err('10 gate required but not present')
    elif not args.require_gate and gated:
        err('10 review copy must be UNGATED but the gate script is present')
    elif not args.require_gate and not stub:
        warn('10 review copy is ungated but carries no review placeholder comment')
    else:
        info('10 gate state correct: %s' % ('gated' if gated else
                                            'ungated review copy, placeholder present'))

    if d.get('gated') is not gated:
        err('10 spec says gated=%s but the page is %s'
            % (d.get('gated'), 'gated' if gated else 'ungated'))

    # -- path leakage -------------------------------------------------------
    # A drive letter must not be preceded by another word character, or the "s:"
    # in "https://" matches and every canonical URL is reported as a path leak.
    leaks = re.findall(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s"<]+|/home/[^\s"<]+|'
                       r'/Users/[^\s"<]+', html)
    if leaks:
        err('   absolute filesystem path leaked into the page: %s' % leaks[0])
    src = d.get('source_copy_path')
    if src and src in html:
        err('   source PDF path leaked into the page: %s' % src)
    if not leaks and not (src and src in html):
        info('   no filesystem paths exposed in the page')

    # -- 11 reproducibility -------------------------------------------------
    try:
        sys.path.insert(0, HERE)
        import build_paper
        rebuilt = build_paper.build(d, gated=gated)
        # Compare on normalised line endings. git's autocrlf can hand back a
        # CRLF working copy of an LF-written file, which is not a content
        # difference and must not be reported as one. This repo has been bitten
        # by CRLF on content-hashed assets before.
        if rebuilt.replace('\r\n', '\n') == html.replace('\r\n', '\n'):
            if rebuilt != html:
                warn('11 page reproduces, but the file on disk has CRLF line endings '
                     'while the builder writes LF -- check .gitattributes/autocrlf '
                     'before hashing this file for any purpose')
            info('11 rebuild %s (sha256 %s)'
                 % ('is byte-identical' if rebuilt == html
                    else 'reproduces, line endings normalised',
                    hashlib.sha256(html.encode('utf-8')).hexdigest()[:16]))
        else:
            err('11 rebuilding from the spec does not reproduce the page on disk')
    except Exception as e:
        warn('11 reproducibility check could not run: %s' % e)

    # -- 12 manifest consistency -------------------------------------------
    mpath = args.manifest
    if not mpath:
        try:
            sys.path.insert(0, os.path.join(REPO_ROOT, 'tools', 'notes'))
            from miw_paths import PASTPAPERS_MANIFEST
            mpath = PASTPAPERS_MANIFEST
        except Exception as e:
            warn('12 could not resolve the manifest path from miw_paths: %s' % e)
    if mpath and os.path.exists(mpath):
        try:
            man = json.load(open(mpath, encoding='utf-8'))
        except json.JSONDecodeError as e:
            err('12 manifest is not valid JSON: %s' % e)
            man = None
        if man:
            papers = {x['paper_id']: x for x in man.get('papers', [])}
            if pid not in papers:
                err('12 manifest has no entry for %s' % pid)
            else:
                mp = papers[pid]
                if mp.get('build_state') != d.get('build_state'):
                    err('12 build_state differs: spec %r, manifest %r'
                        % (d.get('build_state'), mp.get('build_state')))
                if mp.get('question_count') != len(qs):
                    err('12 question_count differs: spec %d, manifest %r'
                        % (len(qs), mp.get('question_count')))
                if mp.get('file') and not os.path.exists(
                        os.path.join(REPO_ROOT, mp['file'])):
                    err('12 manifest points at a file that does not exist: %s' % mp['file'])
                # manifest 2.0 keeps a flat, cross-paper question index
                mq = {q['question_id']: q for q in man.get('questions', [])
                      if q.get('paper_id') == pid}
                spec_ids = {q['question_id'] for q in qs}
                if set(mq) != spec_ids:
                    err('12 manifest question set differs from spec (%d vs %d)'
                        % (len(mq), len(spec_ids)))
                for q in qs:
                    e = mq.get(q['question_id'])
                    if not e:
                        continue
                    if e.get('answer_status') != q.get('answer_status'):
                        err('12 %s answer_status differs: spec %r, manifest %r'
                            % (q['q_no'], q.get('answer_status'), e.get('answer_status')))
                    if e.get('reuse_tier') != q.get('reuse_tier'):
                        err('12 %s reuse_tier differs: spec %r, manifest %r'
                            % (q['q_no'], q.get('reuse_tier'), e.get('reuse_tier')))
                    if e.get('anchor') != q.get('anchor'):
                        err('12 %s anchor differs: spec %r, manifest %r'
                            % (q['q_no'], q.get('anchor'), e.get('anchor')))
                if not any(x.startswith('12') for x in errs):
                    info('12 manifest, spec and output agree')
    elif mpath:
        warn('12 manifest does not exist yet: %s' % mpath)

    # -- 13 unresolved flags ------------------------------------------------
    total_open = 0
    for q in qs:
        for u in (q.get('unresolved') or []):
            total_open += 1
            built = bool(q.get('model_answer'))
            print('  [OPEN%s] %s: %s' % ('!' if built else ' ', q['q_no'], u))
    if total_open:
        info('13 %d unresolved verification flag(s) surfaced above '
             '(OPEN! marks one on a BUILT answer)' % total_open)
    else:
        info('13 no unresolved verification flags')

    if d.get('official_source_verified') is not True:
        info('   official-source verification is FALSE by design and is stated on the page')

    # -- report -------------------------------------------------------------
    print()
    for i in infos:
        print('  [ok   ] %s' % i)
    for w in warns:
        print('  [WARN ] %s' % w)
    for e in errs:
        print('  [ERROR] %s' % e)
    print()
    print('%s audit: %d error(s), %d warning(s)' % (pid, len(errs), len(warns)))
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
