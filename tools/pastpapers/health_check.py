#!/usr/bin/env python3
"""Health check for the Past Written Papers product.

Usage:
  python health_check.py [--self-test]

Deliberately separate from audit_paper.py. The auditor answers "is this ONE
generated paper faithful to its spec?"; this answers "is the PRODUCT coherent?"
-- manifest, both index pages, links between them, content completeness, build
reproducibility, review state and safety. Combining them would produce one
unmaintainable script, which the brief rules out.

Exit 1 on ERROR. WARN never fails.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')

errs, warns, oks = [], [], []


def err(m):
    errs.append(m)


def warn(m):
    warns.append(m)


def ok(m):
    oks.append(m)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def N(*parts):
    """Normalised absolute path.

    Manifest paths use forward slashes; os.path.join on Windows then yields
    mixed separators, so two spellings of the same file hash to different dict
    keys. That silently broke the self-test injection. Always go through N().
    """
    return os.path.normpath(os.path.join(*parts))


def check(publish_mode=False, inject=None):
    global errs, warns, oks
    errs, warns, oks = [], [], []

    # ---------- 1 manifest / spec integrity ----------
    mpath = os.path.join(PP, 'pastpapers_content_index.json')
    if not os.path.exists(mpath):
        err('manifest missing: %s' % mpath)
        return
    try:
        man = json.loads(rd(mpath))
    except json.JSONDecodeError as e:
        err('manifest is not valid JSON: %s' % e)
        return
    ok('manifest parses')

    for k in ('manifest_version', 'papers', 'questions', 'topic_tree',
              'source_of_truth_policy', 'recurrence_classes'):
        if k not in man:
            err('manifest missing required key: %s' % k)

    pids = [p['paper_id'] for p in man['papers']]
    if len(set(pids)) != len(pids):
        err('duplicate paper_id in manifest')
    qids = [q['question_id'] for q in man['questions']]
    if len(set(qids)) != len(qids):
        err('duplicate question_id in manifest')
    if not errs:
        ok('%d paper id(s) and %d question id(s) unique' % (len(pids), len(qids)))

    specs = {}
    for p in man['papers']:
        sp = os.path.join(REPO_ROOT, p['spec'])
        if not os.path.exists(sp):
            err('spec missing for %s: %s' % (p['paper_id'], p['spec']))
            continue
        specs[p['paper_id']] = json.loads(rd(sp))
        if not os.path.exists(os.path.join(REPO_ROOT, p['file'])):
            err('generated page missing for %s: %s' % (p['paper_id'], p['file']))
    if len(specs) == len(man['papers']):
        ok('every manifest paper has a spec and a generated page')

    # ---------- 2 content completeness ----------
    for pid, d in specs.items():
        qs = d['questions']
        if len(qs) != 9:
            warn('%s has %d questions (expected 9 for this series)' % (pid, len(qs)))
        for q in qs:
            tag = '%s %s' % (pid, q['q_no'])
            if not q.get('question_id'):
                err('%s: no question_id' % tag)
            if q['question_id'] != '%s-%s' % (pid, q['q_no']):
                err('%s: question_id %r is not %s-%s' % (tag, q['question_id'], pid, q['q_no']))
            if not q.get('short_title'):
                err('%s: no short_title (side index and search need it)' % tag)
            if not (q.get('topic_tags') or q.get('subject_tags')):
                err('%s: no tags' % tag)
            if not q.get('search_aliases'):
                err('%s: no search_aliases' % tag)
            if not q.get('total_marks'):
                err('%s: no marks' % tag)
            if not strip(q.get('text_verbatim', '')):
                err('%s: empty question text' % tag)
            if q.get('model_answer'):
                if not q.get('study_notes'):
                    err('%s: model answer with no study guide' % tag)
                qr = q.get('quick_revision') or {}
                missing = [k for k in ('recall_15s', 'skeleton', 'keywords',
                                       'critical_regulation', 'major_trap') if not qr.get(k)]
                if missing:
                    err('%s: quick_revision missing %s' % (tag, ', '.join(missing)))
    if not any('quick_revision' in e for e in errs):
        ok('every built question carries a study guide and quick revision')

    # ---------- 3 pages, links, anchors ----------
    idx = os.path.join(PP, 'index.html')
    if not os.path.exists(idx):
        err('index.html missing -- run build_index.py')
    topics = sorted(glob.glob(os.path.join(PP, 'topics-*.html')))
    if not topics:
        err('no topics-<year>.html generated')

    pages = {}
    for p in [N(idx)] + [N(t) for t in topics] + [N(REPO_ROOT, x['file']) for x in man['papers']]:
        if os.path.exists(p):
            pages[p] = rd(p)
    if inject:
        for p, extra in inject.items():
            if p in pages:
                pages[p] = pages[p] + extra

    dead = 0
    for p, body in pages.items():
        base = os.path.dirname(p)
        # Strip <script> and <style> first. The index page inlines JS that builds
        # markup by string concatenation, so href="' + esc(r.u) + '" appears in
        # source and is not a link. Scanning it as one produces a false dead link.
        markup = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', body)
        for href in set(re.findall(r'href="([^"#][^"]*?)(?:#([^"]*))?"', markup)):
            target, frag = href
            if target.startswith(('http', 'mailto:', '/')):
                continue
            tp = N(base, target)
            if not os.path.exists(tp):
                err('dead link in %s -> %s' % (os.path.basename(p), target))
                dead += 1
            elif frag and tp in pages and ('id="%s"' % frag) not in pages[tp]:
                err('dead anchor in %s -> %s#%s' % (os.path.basename(p), target, frag))
                dead += 1
    if not dead:
        ok('all relative links and cross-page anchors resolve (%d page(s))' % len(pages))

    for p in man['papers']:
        body = pages.get(N(REPO_ROOT, p['file']), '')
        missing = [q['anchor'] for q in specs[p['paper_id']]['questions']
                   if 'id="%s"' % q['anchor'] not in body]
        if missing:
            err('%s: anchors missing from page: %s' % (p['paper_id'], ', '.join(missing)))
    if not any('anchors missing' in e for e in errs):
        ok('every question anchor present in its paper page')

    # deep links recorded in the manifest must actually resolve
    bad_deep = 0
    for q in man['questions']:
        tp = N(REPO_ROOT, q['url'])
        if tp in pages and ('id="%s"' % q['anchor']) not in pages[tp]:
            err('manifest deep_link does not resolve: %s' % q['deep_link'])
            bad_deep += 1
    if not bad_deep:
        ok('all %d manifest deep links resolve' % len(man['questions']))

    # MEO Class I hub link
    hub = os.path.join(REPO_ROOT, 'meoclass1', 'index.html')
    if os.path.exists(hub):
        if '/meoclass1/pastpapers/' in rd(hub):
            ok('MEO Class I hub links to the Written Questions section')
        else:
            warn('MEO Class I hub does not yet link to /meoclass1/pastpapers/')

    # ---------- 4 search + interaction metadata ----------
    for p in man['papers']:
        body = pages.get(N(REPO_ROOT, p['file']), '')
        n_search = body.count('data-search=')
        n_qid = body.count('data-qid=')
        if n_search < p['question_count']:
            err('%s: only %d data-search attributes for %d questions'
                % (p['paper_id'], n_search, p['question_count']))
        if n_qid < p['question_count']:
            err('%s: only %d data-qid attributes for %d questions'
                % (p['paper_id'], n_qid, p['question_count']))
        for token in ('aria-expanded', 'aria-pressed', 'miw:pastpapers:v1:bookmarks',
                      'miw:pastpapers:v1:progress'):
            if token not in body:
                err('%s: page is missing %s' % (p['paper_id'], token))
    if not any('data-search' in e or 'aria-' in e for e in errs):
        ok('search, bookmark and progress metadata present on every question card')

    # ---------- 5 build reproducibility ----------
    try:
        import build_paper, build_index
        for p in man['papers']:
            d = specs[p['paper_id']]
            rebuilt = build_paper.build(d, gated=False, publish=publish_mode)
            disk = pages[N(REPO_ROOT, p['file'])]
            if inject and N(REPO_ROOT, p['file']) in inject:
                disk = disk  # injected copy is expected to differ
            if rebuilt.replace('\r\n', '\n') != disk.replace('\r\n', '\n'):
                err('%s: page on disk does not match a fresh render of its spec '
                    '(was it hand-edited?)' % p['paper_id'])
        m2 = build_index.build_manifest(list(specs.values()))
        if json.dumps(m2, sort_keys=True) != json.dumps(man, sort_keys=True):
            err('manifest on disk does not match a fresh build from the specs')
        if not any('does not match' in e for e in errs):
            ok('every generated file reproduces exactly from its source')
    except Exception as e:
        warn('reproducibility check could not run: %s' % e)

    # ---------- 6 review / publication state ----------
    for p in man['papers']:
        body = pages.get(N(REPO_ROOT, p['file']), '')
        noindex = 'noindex' in body
        gated = 'miw_auth=1' in body
        if not publish_mode and not noindex:
            err('%s: review build is NOT noindex' % p['paper_id'])
        if publish_mode and noindex:
            err('%s: publish build still carries noindex' % p['paper_id'])
        if p['gated'] != gated:
            err('%s: manifest says gated=%s but the page is %s'
                % (p['paper_id'], p['gated'], 'gated' if gated else 'ungated'))
    for p in [idx] + topics:
        if os.path.exists(p) and not publish_mode and 'noindex' not in pages.get(N(p), ''):
            err('%s: review build is NOT noindex' % os.path.basename(p))
    if not any('noindex' in e or 'gated' in e for e in errs):
        ok('review state correct: %s' % ('publish mode' if publish_mode
                                         else 'all pages noindex and ungated'))

    # ---------- 7 safety ----------
    leak_rx = re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s"<]+|/home/[^\s"<]+|/Users/[^\s"<]+')
    for p, body in pages.items():
        m = leak_rx.search(body)
        if m:
            err('%s: filesystem path leaked -- %s' % (os.path.basename(p), m.group(0)[:60]))
        for bad in ('dieselship', 'dsguides', 'purchase our original books'):
            if bad in body.lower():
                err('%s: aggregator marketing text present (%s)' % (os.path.basename(p), bad))
        if publish_mode:
            for internal in ('Production metadata', 'reverify_before_publication',
                             'red_team_review', 'P1_PRIMARY_VERIFIED'):
                if internal in body:
                    err('%s: internal production metadata exposed in publish mode (%s)'
                        % (os.path.basename(p), internal))
    if not any('leaked' in e or 'marketing' in e or 'production metadata exposed' in e
               for e in errs):
        ok('no path leakage, no aggregator branding, production metadata correctly scoped')


def strip(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def report():
    for m in oks:
        print('  [ok   ] %s' % m)
    for m in warns:
        print('  [WARN ] %s' % m)
    for m in errs:
        print('  [ERROR] %s' % m)
    print('health check: %d error(s), %d warning(s)' % (len(errs), len(warns)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    check(publish_mode=args.publish)
    report()
    base_errs = len(errs)

    if args.self_test:
        print()
        print('  self-test: injecting faults and asserting the checker fires')
        paper = N(PP, 'EM2607.html')
        cases = [
            ('filesystem path leak', {paper: '<!-- C:/Users/User/secret.pdf -->'}),
            ('aggregator branding', {paper: '<!-- dieselship -->'}),
            ('dead anchor', {paper: '<a href="index.html#does-not-exist">x</a>'}),
        ]
        bad = []
        for name, inject in cases:
            check(publish_mode=False, inject=inject)
            # the injected copy also breaks reproducibility, which is itself correct
            if not errs:
                bad.append('%s did NOT fire' % name)
        for b in bad:
            print('  [SELFTEST FAIL] %s' % b)
        print('  self-test: %s' % ('FAILED' if bad else 'all injected faults detected'))
        if bad:
            base_errs += len(bad)

    sys.exit(1 if base_errs else 0)


if __name__ == '__main__':
    main()
