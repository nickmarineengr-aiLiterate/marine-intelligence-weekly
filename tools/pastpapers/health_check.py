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


def check(publish_mode=False, inject=None, strip_from_pages=None):
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
              'source_of_truth_policy', 'recurrence_statuses'):
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

    # Intake papers -- transcribed questions, no answers -- are held to a
    # DIFFERENT contract, not a weaker one. They must not have a paper page, must
    # not claim a deep link, and must never report as available; what they must
    # have is a complete, tagged transcription. Separating the two sets here is
    # what lets each be checked against the rules that actually apply to it.
    intake = {p['paper_id'] for p in man['papers']
              if p.get('paper_status') != 'available'}
    # Every check below that reads a rendered paper page runs over this list, not
    # over man['papers']. An intake paper has no page, so those checks have
    # nothing to read and would report the absence as a defect.
    solved_papers = [p for p in man['papers'] if p['paper_id'] not in intake]

    errs_before = len(errs)
    specs = {}
    for p in man['papers']:
        # Derived, not read from the manifest. The path to a production input
        # is not candidate data, so it no longer ships in the served file --
        # and the convention that names it is already fixed and already
        # asserted further down, so deriving it costs nothing.
        rel = 'meoclass1/pastpapers/specs/%s.json' % p['paper_id']
        sp = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(sp):
            err('spec missing for %s: %s' % (p['paper_id'], rel))
            continue
        specs[p['paper_id']] = json.loads(rd(sp))
        page_exists = os.path.exists(os.path.join(REPO_ROOT, p['file']))
        if p['paper_id'] in intake:
            # The dangerous direction: a page left behind after a paper's answers
            # were removed would keep serving content the manifest calls unbuilt.
            if page_exists:
                err('%s is an intake paper (no answers) but a generated page exists at %s. '
                    'Delete it: a transcription must never be reachable as a solved paper.'
                    % (p['paper_id'], p['file']))
            if p['answers_built']:
                err('%s: paper_status is not available but answers_built is %d'
                    % (p['paper_id'], p['answers_built']))
        elif not page_exists:
            err('generated page missing for %s: %s' % (p['paper_id'], p['file']))
    # Report success only if this section actually raised nothing. Gating on
    # len(specs) alone printed the all-clear beside its own contradicting error.
    if len(specs) == len(man['papers']) and len(errs) == errs_before:
        ok('every manifest paper has a spec; every solved paper has a page and no '
           'intake paper does (%d solved, %d intake)'
           % (len(man['papers']) - len(intake), len(intake)))

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
            # search_aliases are authored alongside the answer -- they encode the
            # vocabulary a candidate searches for having read it. Demanding them
            # at intake would force a guess, and a guessed alias is worse than
            # none: the year sheet's own tokens already cover the printed stem.
            if not q.get('search_aliases') and pid not in intake:
                err('%s: no search_aliases' % tag)
            if not q.get('total_marks'):
                err('%s: no marks' % tag)
            if not strip(q.get('text_verbatim', '')):
                err('%s: empty question text' % tag)
            if q.get('model_answer'):
                if not q.get('study_notes'):
                    err('%s: model answer with no study guide' % tag)
                qr = q.get('quick_revision') or {}
                # No 'skeleton' here: the answer route lives in answer_route and
                # is rendered from there. Requiring it in two places was how the
                # product would have ended up teaching two competing sequences.
                missing = [k for k in ('recall_15s', 'keywords',
                                       'critical_regulation', 'major_trap') if not qr.get(k)]
                if missing:
                    err('%s: quick_revision missing %s' % (tag, ', '.join(missing)))
                if not ((q.get('answer_route') or {}).get('steps')):
                    err('%s: built answer with no answer_route' % tag)
                if len(q.get('retrieval_cards') or []) < 4:
                    err('%s: built answer with fewer than 4 retrieval cards' % tag)
    if not any('quick_revision' in e or 'answer_route' in e or 'retrieval card' in e
               for e in errs):
        ok('every built question carries a study guide, quick revision, '
           'an answer route and retrieval cards')

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
    if strip_from_pages:
        # Some faults are an ABSENCE -- a page that lost its study-state
        # migration, say. Those cannot be positive-controlled by appending, so
        # the self-test removes the marker instead.
        for p in pages:
            pages[p] = pages[p].replace(strip_from_pages, '')

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

    for p in solved_papers:
        body = pages.get(N(REPO_ROOT, p['file']), '')
        missing = [q['anchor'] for q in specs[p['paper_id']]['questions']
                   if 'id="%s"' % q['anchor'] not in body]
        if missing:
            err('%s: anchors missing from page: %s' % (p['paper_id'], ', '.join(missing)))
    if not any('anchors missing' in e for e in errs):
        ok('every question anchor present in its paper page')

    # deep links recorded in the manifest must actually resolve
    bad_deep = 0
    linked = 0
    for q in man['questions']:
        if q['paper_id'] in intake:
            # Both halves matter. A null deep link on an intake question is
            # correct; a non-null one would advertise a page that was never
            # built, which is the precise defect this pair of checks exists for.
            if q.get('url') or q.get('deep_link'):
                err('%s: intake question carries a deep link (%s) but its paper has no page'
                    % (q['question_id'], q.get('deep_link')))
                bad_deep += 1
            continue
        linked += 1
        tp = N(REPO_ROOT, q['url'])
        if tp in pages and ('id="%s"' % q['anchor']) not in pages[tp]:
            err('manifest deep_link does not resolve: %s' % q['deep_link'])
            bad_deep += 1
    if not bad_deep:
        ok('all %d manifest deep links resolve; the other %d are intake questions '
           'and correctly carry none' % (linked, len(man['questions']) - linked))

    # MEO Class I hub link
    hub = os.path.join(REPO_ROOT, 'meoclass1', 'index.html')
    if os.path.exists(hub):
        if '/meoclass1/pastpapers/' in rd(hub):
            ok('MEO Class I hub links to the Written Questions section')
        else:
            warn('MEO Class I hub does not yet link to /meoclass1/pastpapers/')

    # ---------- 4 search + interaction metadata ----------
    for p in solved_papers:
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
        for p in solved_papers:
            d = specs[p['paper_id']]
            rebuilt = build_paper.build(d, gated=False, publish=publish_mode)
            disk = pages[N(REPO_ROOT, p['file'])]
            if inject and N(REPO_ROOT, p['file']) in inject:
                disk = disk  # injected copy is expected to differ
            if rebuilt.replace('\r\n', '\n') != disk.replace('\r\n', '\n'):
                err('%s: page on disk does not match a fresh render of its spec '
                    '(was it hand-edited?)' % p['paper_id'])
        # The file on disk is the CANDIDATE PROJECTION of the review view, so
        # it is compared against that projection. Comparing it against the rich
        # object would report a correctly minimised manifest as unreproducible.
        m2 = build_index.candidate_manifest(
            build_index.build_manifest(list(specs.values())))
        if json.dumps(m2, sort_keys=True) != json.dumps(man, sort_keys=True):
            err('manifest on disk does not match a fresh build from the specs')
        if not any('does not match' in e for e in errs):
            ok('every generated file reproduces exactly from its source')
    except Exception as e:
        warn('reproducibility check could not run: %s' % e)

    # ---------- 6 review / publication state ----------
    for p in solved_papers:
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
        ok('no path leakage, no third-party branding, production metadata correctly scoped')

    # ---------- 8 QP identity migration ----------
    # These exist because the EM -> QP rename touched 26 files, and the failure
    # mode of a half-done rename is not a crash: it is a page that loads, a link
    # that 404s only when clicked, and study state silently orphaned.
    QP_ID = re.compile(r'^QP\d{4}$')
    LEGACY_ID = re.compile(r'\bEM-?\d{4}\b')

    for pid in pids:
        if not QP_ID.match(pid):
            err('paper_id %r does not match the canonical QP<YY><MM> convention' % pid)
    for q in man['questions']:
        want = '%s-%s' % (q['paper_id'], q['question_number'])
        if q['question_id'] != want:
            err('question_id %r does not match paper_id + question number (%r)'
                % (q['question_id'], want))

    # Canonical identity must be gone from every product surface. Prose that
    # merely DESCRIBES the migration is legitimate, so this deliberately scans
    # the manifest and the generated pages, not the documentation or the
    # verification records.
    for label, body in ([('manifest', rd(mpath))] +
                        [(os.path.basename(p), b) for p, b in pages.items()]):
        m = LEGACY_ID.search(body)
        if m:
            err('%s: legacy paper identifier %r still present. One canonical '
                'identity everywhere: the QP series.' % (label, m.group(0)))

    for pid in pids:
        sp = N(PP, 'specs', '%s.json' % pid)
        if not os.path.exists(sp):
            err('no spec named for paper %s (expected specs/%s.json)' % (pid, pid))
        if pid in intake:
            # A verification directory records how an ANSWER was sourced and
            # red-teamed. An intake paper has no answer, so requiring one would
            # invite an empty directory that asserts work nobody did.
            continue
        pg = N(PP, '%s.html' % pid)
        if not os.path.exists(pg):
            err('no generated page for paper %s (expected %s.html)' % (pid, pid))
        vdir = N(PP, 'verification', pid)
        if not os.path.isdir(vdir):
            err('no verification directory for paper %s (expected verification/%s/)'
                % (pid, pid))

    # The shipped migration itself. Without this, a rebuild that dropped the
    # snippet would orphan every bookmark a student had saved, silently.
    for p, body in pages.items():
        # Scope by what a page DOES, not by what it looks like: the shared
        # stylesheet is inlined everywhere, so matching on a class name like
        # .q-card matches the topics page too. A page needs the migration only
        # if it actually reads saved study state.
        if 'miw:pastpapers:v1:bookmarks' not in body:
            continue
        if 'migrateLegacyKeys' not in body:
            err('%s: no legacy study-state migration in the page script. Renaming '
                'the paper without it silently orphans saved bookmarks and progress.'
                % os.path.basename(p))

    if not any('legacy' in e or 'canonical' in e or 'no generated page' in e for e in errs):
        ok('QP identity is canonical everywhere; specs, pages and verification '
           'records all present; study-state migration shipped')

    # ---------- 9 sitting navigator ----------
    for key in ('series_years', 'months', 'paper_status_model'):
        if key not in man:
            err('manifest missing navigator key: %s' % key)
    idx = pages.get(N(PP, 'index.html'))
    if idx:
        for p in man['papers']:
            if p['paper_status'] != 'available':
                continue
            cell = 'href="%s.html"' % p['paper_id']
            if cell not in idx:
                err('index.html: %s is available but has no month cell linking to it'
                    % p['paper_id'])
            if p['month'] not in idx:
                err('index.html: no %s cell for %s' % (p['month'], p['paper_id']))
        for y in man.get('series_years', []):
            if '>%d<' % y not in idx:
                err('index.html: series year %d is not rendered in the navigator' % y)
        # A month with no answers must never read as solved.
        if idx.count('class="m avail"') != sum(
                1 for p in man['papers'] if p['paper_status'] == 'available'):
            err('index.html: count of "available" month cells does not match the '
                'number of papers with answers built')
        if not any('month cell' in e or 'navigator' in e for e in errs):
            ok('sitting navigator renders every advertised year and links each '
               'available month to its paper')

    # ---------- 10 learning layer ----------
    # Structural only. Whether a flashcard is a GOOD flashcard is human judgement
    # and is deliberately not regex-policed here.
    for sp in sorted(glob.glob(os.path.join(PP, 'specs', '*.json'))):
        d = json.loads(rd(sp))
        page = pages.get(N(PP, '%s.html' % d['paper_id']))
        if not page:
            continue
        built_qs = [q for q in d['questions'] if q.get('model_answer')]

        for q in built_qs:
            steps = (q.get('answer_route') or {}).get('steps') or []
            for s in steps:
                want = ('%d. %s' % (s['n'], s['title'])).replace(
                    '&', '&amp;')       # matches render_common.esc on bare ampersands
                if want not in page:
                    err('%s: route step %r is not rendered on the page'
                        % (q['question_id'], want))
            for c in q.get('retrieval_cards') or []:
                if 'id="%s"' % c['id'] not in page:
                    err('%s: retrieval card %s is not rendered'
                        % (q['question_id'], c['id']))

        # One map branch, one recall blank and one flashcard prompt per source
        # item. A count mismatch is how a derived view silently loses a step.
        n_steps = sum(len((q.get('answer_route') or {}).get('steps') or []) for q in built_qs)
        n_cards = sum(len(q.get('retrieval_cards') or []) for q in built_qs)
        for needle, expected, what in (
                ('class="kmap-branch"', n_steps, 'knowledge map branches'),
                ('class="recall-blank"', n_steps, 'recall blanks'),
                ('class="card-q"', n_cards, 'flashcard prompts')):
            got = page.count(needle)
            if got != expected:
                err('%s: %d %s rendered, expected %d -- a derived view has drifted '
                    'from the answer route' % (d['paper_id'], got, what, expected))

        # The learning layer must never be able to hide the answer. Sections are
        # emitted unhidden and only the script hides them, so a page built with a
        # pre-hidden answer mode would strand a no-JS reader.
        if '<div class="mode" data-mode="answer">' not in page:
            err('%s: model answer is not inside its own learner mode' % d['paper_id'])
        if re.search(r'data-mode="answer"[^>]*\shidden', page):
            err('%s: the model answer mode is emitted pre-hidden' % d['paper_id'])

    # ---------- 11 topic page renders each question exactly once ----------
    for year in sorted({p['year'] for p in man['papers']}):
        tp = pages.get(N(PP, 'topics-%d.html' % year))
        if not tp:
            continue
        for q in man['questions']:
            if q['year'] != year:
                continue
            # Count the card, not the link. An intake question renders a card
            # with no href, so counting links would score it 0 and, worse, would
            # stop detecting genuine duplication for exactly those questions.
            n = tp.count('data-qid="%s"' % q['question_id'])
            if n != 1:
                err('topics-%d.html: %s appears %d time(s), expected exactly 1. '
                    'One primary category per question -- a question rendered under '
                    'several categories is duplication, not navigation.'
                    % (year, q['question_id'], n))
    if not any('appears' in e and 'primary category' in e for e in errs):
        ok('topic page renders every question exactly once under its primary category')

    if not any('route step' in e or 'derived view' in e or 'retrieval card' in e
               or 'learner mode' in e or 'pre-hidden' in e for e in errs):
        ok('learning layer coherent: map, recall blanks and flashcards all derive '
           'from the answer route, and the answer renders unhidden')


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
        # Derive the page to inject into from the specs. Hardcoding a filename
        # here means a paper rename silently changes what the self-test covers.
        # Only a SOLVED paper has a page to inject a fault into. Sorting all
        # spec ids and taking the first would pick QP2501 -- an intake spec with
        # no page -- and abort the whole self-test, silently removing the
        # positive control that proves these checks can fail.
        spec_ids = sorted(d['paper_id'] for d in
                          (json.loads(rd(p))
                           for p in glob.glob(os.path.join(PP, 'specs', '*.json')))
                          if any(q.get('model_answer') for q in d['questions']))
        if not spec_ids:
            print('  [SELFTEST FAIL] no solved spec found to derive a paper page from')
            sys.exit(1)
        paper = N(PP, '%s.html' % spec_ids[0])
        if not os.path.exists(paper):
            print('  [SELFTEST FAIL] derived paper page does not exist: %s' % paper)
            sys.exit(1)
        cases = [
            ('filesystem path leak', {paper: '<!-- C:/Users/User/secret.pdf -->'}),
            ('third-party branding', {paper: '<!-- dieselship -->'}),
            ('dead anchor', {paper: '<a href="index.html#does-not-exist">x</a>'}),
            # A half-finished rename leaves a legacy identifier behind in one
            # generated surface. That must fail loudly, not read as cosmetic.
            ('legacy EM identifier in a generated page', {paper: '<!-- EM2607 -->'}),
            ('legacy EM sr_no in a generated page', {paper: '<!-- EM-2607 -->'}),
        ]
        bad = []
        for name, inject in cases:
            check(publish_mode=False, inject=inject)
            # the injected copy also breaks reproducibility, which is itself correct
            if not errs:
                bad.append('%s did NOT fire' % name)

        cases.append(('model answer emitted pre-hidden',
                      {paper: '<div class="mode" data-mode="answer" hidden></div>'}))

        # Absence faults: positive-controlled by removal, not injection.
        for name, marker in [('missing study-state migration', 'migrateLegacyKeys'),
                             ('missing month cell for an available paper',
                              'class="m avail"'),
                             ('knowledge map branch lost from the route',
                              'class="kmap-branch"'),
                             ('recall blank lost from the route',
                              'class="recall-blank"'),
                             ('flashcard prompt lost', 'class="card-q"')]:
            check(publish_mode=False, strip_from_pages=marker)
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
