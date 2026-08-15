#!/usr/bin/env python3
"""Contract test for the Study Topic Map (/solvedQP/topics.html).

Usage:
    python tools/pastpapers/topic_map_test.py               # contract
    python tools/pastpapers/topic_map_test.py --self-test   # mutation controls

WHAT IS UNDER TEST
------------------
topics.html owns layout and owns no product truth. Every domain, topic, count,
sitting figure and question link on the shipped bytes is recomputed here from
the canonical specs (via topic_taxonomy, the one normalisation) and cross-
checked against the delivery manifest's `study_topics`, so that:

  * a Topic Map leaf and the structured `?topic=&domain=` filter it links to
    are the SAME SET of question ids (exact set equality, not count equality);
  * no solved question is orphaned and no unsolved question is implied;
  * no authoring field, internal id or filename reaches a candidate.

--self-test mutates a copy of the real page / manifest / alias map in memory
and asserts each guard bites; then proves the shipped page passes.
"""
import argparse, copy, glob, html as html_mod, io, json, os, re, sys
from urllib.parse import urlparse, parse_qs, unquote

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT, strip_tags  # noqa: E402
import topic_taxonomy as TT  # noqa: E402
import build_topic_map as BTM  # noqa: E402
from build_solvedqp_home import load_specs, solved_sittings  # noqa: E402
from build_solvedqp_manifest import BANNED_KEYS  # noqa: E402

PAGE = os.path.join(REPO_ROOT, 'solvedQP', 'topics.html')
HOME = os.path.join(REPO_ROOT, 'solvedQP', 'index.html')
MANIFEST = os.path.join(REPO_ROOT, 'solvedQP', 'solvedqp_content_index.json')

# Vocabulary that must never face a candidate on this page. The manifest's
# banned keys, plus the internal names a page could leak as prose.
INTERNAL_TOKENS = tuple(sorted(BANNED_KEYS)) + (
    'TSCR', 'specs/', 'verification/', '.json', 'Founder', 'reused_from',
    'recurrence_class', 'source_copy', 'intelligence-only', 'PLANNED_SOON',
    'question_id',
)


def unesc(s):
    return (s.replace('&amp;', '&').replace('&middot;', '·').replace('&mdash;', '—')
             .replace('&rarr;', '→'))


# ------------------------------------------------------------------ parsing

TOPIC_RE = re.compile(
    r'<details class="tm-topic( tm-other)?">\s*<summary><div><h3>(.*?)</h3>\s*'
    r'<span class="tm-cnt"><b>(\d+)</b> solved question', re.S)
Q_RE = re.compile(r'<li><a href="(/solvedQP/(QP\d{4})\.html#(q\d+))">')
GO_RE = re.compile(r'<a class="tm-go(?: alt)?" href="([^"]+)">(?:Study these|All) (\d+) questions')
DOM_RE = re.compile(r'<details class="tm-dom" id="[^"]+">\s*<summary>\s*<div>\s*<h2>(.*?)</h2>\s*'
                    r'<span class="tm-cnt"><b>(\d+)</b> solved question', re.S)


def parse_page(html):
    """Domains -> topics -> question hrefs, from the shipped HTML alone."""
    doms = []
    for m in re.finditer(r'<details class="tm-dom" id="[^"]+">(.*?)\n  </details>', html, re.S):
        block = m.group(1)
        dm = DOM_RE.search('<details class="tm-dom" id="x">' + block)
        label = unesc(dm.group(1))
        dcount = int(dm.group(2))
        topics = []
        for tm in re.finditer(r'<details class="tm-topic( tm-other)?">(.*?)</details></li>',
                              block, re.S):
            tb = tm.group(2)
            hm = re.search(r'<h3>(.*?)</h3>\s*<span class="tm-cnt"><b>(\d+)</b>', tb, re.S)
            go = GO_RE.search(tb)
            topics.append({
                'other': bool(tm.group(1)),
                'label': unesc(hm.group(1)),
                'count': int(hm.group(2)),
                'hrefs': [x[0] for x in Q_RE.findall(tb)],
                'go_href': html_mod.unescape(go.group(1)) if go else None,
                'go_count': int(go.group(2)) if go else None,
            })
        doms.append({'label': label, 'count': dcount, 'topics': topics})
    return doms


def qid_of(href):
    m = re.match(r'/solvedQP/(QP\d{4})\.html#q(\d+)$', href)
    return '%s-Q%s' % (m.group(1), m.group(2)) if m else None


def structured(manifest, topic=None, domain=None):
    """The browser's matchStructured(), reimplemented exactly: equality only."""
    out = set()
    if not topic and not domain:
        return out
    for p in manifest['papers']:
        if p['status'] != 'AVAILABLE':
            continue
        for x in p['questions']:
            if domain and x.get('primary_category') != domain:
                continue
            if topic and topic not in (x.get('study_topics') or []):
                continue
            out.add(x['question_id'])
    return out


# ------------------------------------------------------------------ rules

def run(html, specs, manifest, home_html, aliases=None, report=True):
    fails = []

    def check(name, cond, detail=''):
        if report:
            print('  [ %-4s ] %s%s' % ('OK' if cond else 'FAIL', name,
                                       ('  -- %s' % detail) if detail else ''))
        if not cond:
            fails.append(name)

    sittings = solved_sittings(specs)
    solved_q = {q['question_id']: (d, q) for d in sittings for q in d['questions']}
    tmap = TT.build_topic_map(sittings)
    page = parse_page(html)

    # 1. every solved question belongs to exactly one domain
    dom_ids = [i for d in tmap['domains'] for i in d['question_ids']]
    check('1. every solved question has exactly one domain',
          sorted(dom_ids) == sorted(solved_q) and len(dom_ids) == len(set(dom_ids)),
          '%d ids across domains, %d solved' % (len(dom_ids), len(solved_q)))

    # 2. domain counts == primary_category counts (specs) and page
    want = {}
    for d, q in solved_q.values():
        want[q['primary_category']] = want.get(q['primary_category'], 0) + 1
    got = {d['label']: d['count'] for d in page}
    check('2. page domain counts equal primary_category counts', got == want,
          'page=%s' % ({k: v for k, v in got.items() if want.get(k) != v} or 'all match'))

    # 3. every solved question reachable from >=1 topic / Other bucket (map and page)
    reach_map = {i for d in tmap['domains'] for t in d['topics'] for i in t['question_ids']}
    reach_map |= {i for d in tmap['domains'] for i in d['other']['question_ids']}
    reach_page = {qid_of(h) for d in page for t in d['topics'] for h in t['hrefs']}
    check('3. no orphan: every solved question reachable (map)', reach_map == set(solved_q),
          '%d missing' % len(set(solved_q) - reach_map))
    check('3. no orphan: every solved question reachable (page)', reach_page == set(solved_q),
          'missing %s' % sorted(set(solved_q) - reach_page)[:5])

    # 4. topic counts equal distinct question ids (page count, rows, link count)
    bad = []
    for d in page:
        for t in d['topics']:
            ids = {qid_of(h) for h in t['hrefs']}
            if len(ids) != len(t['hrefs']) or t['count'] != len(ids):
                bad.append('%s/%s says %d has %d rows' % (d['label'], t['label'], t['count'], len(ids)))
            if not t['other'] and t['go_count'] != len(ids):
                bad.append('%s/%s link says %s' % (d['label'], t['label'], t['go_count']))
    check('4. every topic count equals its distinct question rows', not bad, '; '.join(bad[:3]))

    # 4b. page topics == map topics (labels, ids, order)
    bad = []
    for pd, md in zip(page, tmap['domains']):
        if pd['label'] != md['label']:
            bad.append('domain order %s vs %s' % (pd['label'], md['label']))
            continue
        pt = [t for t in pd['topics'] if not t['other']]
        if [t['label'] for t in pt] != [t['label'] for t in md['topics']]:
            bad.append('%s topic list differs' % pd['label'])
        for a, b in zip(pt, md['topics']):
            if [qid_of(h) for h in a['hrefs']] != b['question_ids']:
                bad.append('%s/%s rows differ' % (pd['label'], a['label']))
        po = [t for t in pd['topics'] if t['other']]
        oth = md['other']['question_ids']
        if bool(po) != bool(oth) or (po and [qid_of(h) for h in po[0]['hrefs']] != oth):
            bad.append('%s Other bucket differs' % pd['label'])
    check('4b. page topics equal recomputed map (labels, rows, order)', not bad, '; '.join(bad[:3]))

    # 5. overlap permitted: topic sums may exceed the domain count
    over = [d['label'] for d in tmap['domains']
            if sum(len(t['question_ids']) for t in d['topics']) > len(d['question_ids'])]
    check('5. topic counts overlap and are not forced to sum to the domain', bool(over),
          '%d domains overlap' % len(over))
    check('5b. page states the overlap rule',
          'topic counts overlap and do not add up' in html)

    # 6. every question href resolves to a real QP page + anchor
    bad = []
    seen = set()
    for d in page:
        for t in d['topics']:
            for h in t['hrefs']:
                if h in seen:
                    continue
                seen.add(h)
                m = re.match(r'/solvedQP/(QP\d{4})\.html#(q\d+)$', h)
                if not m:
                    bad.append(h); continue
                f = os.path.join(REPO_ROOT, 'solvedQP', '%s.html' % m.group(1))
                if not os.path.exists(f):
                    bad.append(h + ' (no page)'); continue
                page_html = open(f, encoding='utf-8').read()
                if ('id="%s"' % m.group(2)) not in page_html:
                    bad.append(h + ' (no anchor)')
    check('6. every question href resolves to a real page and anchor', not bad, '; '.join(bad[:3]))

    # 7. structured filter == mapped set (EXACT SET EQUALITY), from the page's own links
    bad = []
    n_links = 0
    for d in page:
        for t in d['topics']:
            if not t['go_href']:
                continue
            qs = parse_qs(urlparse(t['go_href']).query)
            topic = (qs.get(TT.PARAM_TOPIC) or [None])[0]
            dom = (qs.get(TT.PARAM_DOMAIN) or [None])[0]
            got = structured(manifest, topic, dom)
            want_ids = {qid_of(h) for h in t['hrefs']} if not t['other'] else \
                {i for i in solved_q if solved_q[i][1]['primary_category'] == d['label']}
            n_links += 1
            if got != want_ids:
                bad.append('%s/%s: filter %d vs page %d' % (d['label'], t['label'], len(got), len(want_ids)))
    check('7. ?topic=&domain= returns EXACTLY the mapped set for every link', not bad and n_links > 0,
          '%d links checked; %s' % (n_links, '; '.join(bad[:3])))
    # 7b. domain filter == domain partition, and topic-without-domain is a superset (intersection semantics)
    bad = []
    for d in tmap['domains']:
        if structured(manifest, None, d['label']) != set(d['question_ids']):
            bad.append(d['label'])
        for t in d['topics']:
            if not set(t['question_ids']) <= structured(manifest, t['label'], None):
                bad.append('%s/%s' % (d['label'], t['label']))
    check('7b. ?domain= equals the domain partition; intersection semantics hold', not bad,
          '; '.join(bad[:3]))

    # 8. no intelligence-only (unsolved) question or paper appears
    solved_pids = {d['paper_id'] for d in sittings}
    pids = set(re.findall(r'QP\d{4}', html))
    check('8. no unsolved paper id appears on the page', pids <= solved_pids,
          'stray %s' % sorted(pids - solved_pids)[:5])
    check('8b. every question row is a solved question', None not in reach_page and reach_page <= set(solved_q))

    # 9. no banned / internal field or vocabulary
    body = html[html.index('<body>'):]
    hits = [t for t in INTERNAL_TOKENS if t in body]
    check('9. no authoring field or internal token faces the candidate', not hits, ', '.join(hits[:5]))

    # 10. every alias-map key is a real source label
    corpus_labels = {TT._key(s) for d, q in solved_q.values() for s in (q.get('subject_tags') or [])}
    al = aliases if aliases is not None else TT.ALIASES
    stale = [k for k in al if TT._key(k) not in corpus_labels]
    check('10. every alias-map entry corresponds to a real source label', not stale, ', '.join(stale[:5]))

    # 11. scope / partial-year wording is generated and correct
    scope = BTM.scope_line(sittings, len(solved_q))
    check('11. scope line states solved sittings, questions and the part year',
          scope in html and ('Built from the %d sittings' % len(sittings)) in html
          and BTM.part_year_note(sittings) in html)
    check('11b. page never claims coverage of the whole examination history',
          'All MEO Class I' not in html and '549' not in body)

    # 12. deterministic: rebuild == disk
    rebuilt = BTM.build(specs)
    check('12. rebuild is byte-identical to the shipped page', rebuilt == html)

    # 13. the manifest's study_topics agree with the taxonomy (same normaliser)
    norm = TT.make_normaliser(sittings)
    bad = []
    for p in manifest['papers']:
        for x in p.get('questions') or []:
            d, q = solved_q[x['question_id']]
            if x.get('study_topics') != TT.study_topics_for(q, norm):
                bad.append(x['question_id'])
    check('13. manifest study_topics equal the taxonomy projection', not bad, ', '.join(bad[:3]))

    # 14. entry points: home card + nav link on the map page itself
    check('14. home page links to the study roadmap', '/solvedQP/topics.html' in home_html)
    check('14b. map page carries the Written navigation', 'aria-current="page">What should I study?' in html)

    return fails


def load():
    specs = load_specs()
    html = open(PAGE, encoding='utf-8', newline='').read()
    home = open(HOME, encoding='utf-8').read()
    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    return html, specs, manifest, home


def self_test():
    html, specs, manifest, home = load()
    ok = True

    def probe(name, mutated_html=None, mutated_manifest=None, aliases=None):
        nonlocal ok
        got = run(mutated_html if mutated_html is not None else html, specs,
                  mutated_manifest if mutated_manifest is not None else manifest,
                  home, aliases=aliases, report=False)
        print('  %-58s %s' % (name, 'PASS' if got else 'FAIL (not detected)'))
        if not got:
            ok = False

    # wrong topic count
    m = re.search(r'<h3>Port State Control</h3>\s*<span class="tm-cnt"><b>(\d+)</b>', html)
    n = m.group(1)
    probe('hand-edited topic count is caught',
          html.replace(m.group(0), m.group(0).replace('<b>%s</b>' % n, '<b>%d</b>' % (int(n) + 1)), 1))
    # orphan question: delete every row of one question
    some = re.search(r'<li><a href="(/solvedQP/QP\d{4}\.html#q\d+)">', html).group(1)
    probe('orphaned question (rows deleted) is caught',
          re.sub(r'<li><a href="%s">.*?</a></li>\n' % re.escape(some), '', html))
    # stale alias
    probe('stale alias-map entry is caught', aliases=dict(TT.ALIASES, **{'Ballast Water Mgmt': 'Ballast'}))
    # intelligence-only question inserted
    probe('intelligence-only question inserted is caught',
          html.replace('<ul class="tm-qs">',
                       '<ul class="tm-qs">\n<li><a href="/solvedQP/QP2201.html#q1"><span class="tm-sit">'
                       'January 2022 · Q1</span><span class="tm-title">x</span><span class="tm-rec">x</span></a></li>', 1))
    # missing anchor
    probe('question href to a missing anchor is caught',
          html.replace(some, some.split('#')[0] + '#q99', 1))
    # structured filter superset: an extra question carries the topic in the manifest
    mm = copy.deepcopy(manifest)
    done = False
    for p in mm['papers']:
        for x in p.get('questions') or []:
            if x['primary_category'] == 'Statutory Framework & Class' and 'Port State Control' not in x['study_topics']:
                x['study_topics'].append('Port State Control'); done = True; break
        if done:
            break
    probe('structured filter returning a superset is caught', mutated_manifest=mm)
    # banned token
    probe('internal token on the page is caught', html.replace('</main>', '<p>recurrence_class</p></main>'))
    # scope wording drift
    probe('hand-edited scope wording is caught', html.replace('Built from the ', 'Built from all ', 1))

    real = run(html, specs, manifest, home, report=True)
    print('  %-58s %s' % ('the SHIPPED page passes every rule', 'PASS' if not real else 'FAIL'))
    if real:
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        print('TOPIC MAP self-test')
        sys.exit(0 if self_test() else 1)
    html, specs, manifest, home = load()
    fails = run(html, specs, manifest, home)
    print('TOPIC MAP %s' % ('PASS' if not fails else 'FAIL (%d)' % len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
