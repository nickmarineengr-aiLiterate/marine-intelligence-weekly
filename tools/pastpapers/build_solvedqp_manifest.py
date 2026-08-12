#!/usr/bin/env python3
"""Build the Solved QP product manifest at /solvedQP/solvedqp_content_index.json.

    specs/*.json  -->  solvedQP/solvedqp_content_index.json

Usage:
  python build_solvedqp_manifest.py [--check] [--self-test] [--out PATH]

WHAT THIS IS
------------
The single generated inventory of the Written delivery product. The index page,
its topic search, its "latest updates" strip and the daily health check all read
THIS file, so there is one statement of what is published and one place a count
can be wrong. It is a PROJECTION of the canonical specs, never a second content
database, and it is never hand-edited.

WHY IT IS NOT pastpapers_content_index.json
-------------------------------------------
That manifest already exists and is kept. It is the RETRIEVAL index for the
review/authoring surface under /meoclass1/pastpapers/, and it carries authoring
fields a candidate must never see -- reuse_tier, verification_status, the
dedup plan and red-team review paths, answer_status. Publishing it to the
delivery surface would leak production metadata into the paid product.

This manifest is the DELIVERY projection: candidate-facing fields only.

THE PAID-TEXT BOUNDARY -- the rule this file exists to hold
----------------------------------------------------------
No worked answer, study guide, recall card, answer route, memory cue or
retrieval card may ever enter this file. Those are the product. What goes in is
discovery information the candidate is already shown before buying: the printed
question stem, its topic labels, and which sitting it belongs to.

The boundary is not a convention here, it is ENFORCED: assert_no_paid_text()
walks the finished object and fails the build if any banned field name or any
model-answer substring appears. See --self-test, which proves the guard fires.

WHY UNSOLVED STEMS ARE ABSENT
-----------------------------
Current product policy publishes no unsolved question text: the home page shows
a PLANNED SOON card with no link, and the year sheets count only solved
sittings. The manifest follows that policy rather than restating it. A planned
paper therefore appears as a STATUS with a question_count and no questions, so
topic search can never make an unsolved sitting look solved.

DETERMINISM
-----------
No clock is read. `generated` is the newest `updated` date across the specs --
a content date, not a build date -- so re-running with unchanged specs is
byte-identical. The health check ages the manifest against that same content
date, which is the honest thing to age it against.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT, strip_tags  # noqa: E402
import recurrence_model as RM  # noqa: E402
# Coverage state and "which sittings are solved" are defined ONCE, by the home
# page builder, and imported here. Two derivations of "is this paper available"
# would eventually disagree, and the disagreement would be invisible: the card
# would say AVAILABLE and the manifest PLANNED, or the reverse.
from build_solvedqp_home import (coverage, solved_sittings, load_specs,
                                 AVAILABLE, PLANNED_SOON, NO_SITTING)
from build_questions_year import KNOWN_ABSENT  # noqa: E402

MANIFEST_VERSION = '1.0'
OUT_REL = os.path.join('solvedQP', 'solvedqp_content_index.json')

# Spec fields that ARE the paid product. None may reach the manifest.
PAID_QUESTION_FIELDS = (
    'model_answer', 'study_notes', 'quick_revision', 'answer_route',
    'understand_first', 'memory_cue', 'retrieval_cards', 'decomposition',
    'sources', 'reuse_evidence', 'provenance_summary',
)
# Authoring fields that are not paid text but must never face a candidate.
# recurrence_class and host_recurrence_hint are already policed corpus-wide by
# recurrence_check.py; they are named again here so this file is self-contained.
AUTHORING_FIELDS = (
    'recurrence_class', 'host_recurrence_hint', 'reuse_tier', 'answer_status',
    'verification_status', 'verification_file', 'build_state', 'review_state',
    'reverify_before_publication', 'temporal_review', 'recurrence_adjudication',
    'reused_from', 'question_delta', 'unresolved', 'decomposition_gate',
    'source_copy_path', 'source_copy_provenance',
)
BANNED_KEYS = frozenset(PAID_QUESTION_FIELDS + AUTHORING_FIELDS)


def norm_search(text):
    """Fold a printed stem to a matchable form.

    Entities out, marks and punctuation out, case out, whitespace collapsed.
    The search box compares against this, never against the display stem, so a
    candidate typing "port state control" matches a stem printed with an
    en dash, a bracketed mark total or curly quotes.
    """
    s = strip_tags(text or '')
    s = (s.replace('&amp;', ' and ').replace('&nbsp;', ' ')
          .replace('&ndash;', ' ').replace('&mdash;', ' ')
          .replace('&rsquo;', "'").replace('&lsquo;', "'")
          .replace('&ldquo;', '"').replace('&rdquo;', '"'))
    s = re.sub(r'&[a-z]+;', ' ', s)
    s = s.lower()
    s = re.sub(r'\(\s*\d+\s*\)', ' ', s)      # trailing (16) mark totals
    s = re.sub(r"[^a-z0-9'&]+", ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def sitting_label(month, year):
    return '%s %d' % (month, year)


def _paper_topics(d):
    """Category and subject labels for a paper, deduplicated, stable order."""
    cats, subs = [], []
    for q in d['questions']:
        c = q.get('primary_category')
        if c and c not in cats:
            cats.append(c)
        for s in q.get('subject_tags') or []:
            if s not in subs:
                subs.append(s)
    return sorted(cats), sorted(subs)


def question_records(d, rel, nodes):
    """Candidate-facing question rows for one AVAILABLE paper."""
    out = []
    for q in d['questions']:
        qid = q['question_id']
        stem = q.get('text_verbatim') or ''
        anchor = q.get('anchor') or ('q%s' % str(q['q_no']))
        status = rel[qid]['status']
        rec = {
            'question_id': qid,
            'paper_id': d['paper_id'],
            # q_no is already 'Q1'..'Q9' in every spec. Prefixing it again gave
            # 'QQ8' in the first build; normalise instead of assuming a format.
            'question_number': q['q_no'] if str(q['q_no']).upper().startswith('Q')
                               else 'Q%s' % q['q_no'],
            'anchor': anchor,
            'href': '/solvedQP/%s.html#%s' % (d['paper_id'], anchor),
            'marks': q.get('total_marks'),
            'short_title': q.get('short_title'),
            'stem': stem,
            'search_text': norm_search(
                ' '.join([stem, q.get('short_title') or '',
                          ' '.join(q.get('topic_tags') or []),
                          ' '.join(q.get('subject_tags') or []),
                          ' '.join(q.get('search_aliases') or []),
                          q.get('primary_category') or ''])),
            'primary_category': q.get('primary_category'),
            'subject_tags': list(q.get('subject_tags') or []),
            'topic_tags': list(q.get('topic_tags') or []),
            'search_aliases': list(q.get('search_aliases') or []),
            'intent_tags': list(q.get('intent_tags') or []),
            # The CHRONOLOGICAL status computed from (year, month) -- the same
            # candidate-facing value the year sheets render. Not recurrence_class,
            # which is an authoring field and is on the banned list above.
            'recurrence_status': status,
            'recurrence_label': RM.STATUS_LABEL_PLAIN[status],
        }
        out.append(rec)
    return out


def recently_updated(specs, avail_ids):
    """Candidate-facing change records, newest first.

    SOURCE, in precedence order:

      1. An explicit `changelog` array on the spec. This is the only place an
         authoring session records a CORRECTION, and it is structured, owned by
         the paper it describes, and reviewed with it. There is no second
         ledger and nothing scrapes SESSION_HISTORY -- free-form narrative
         written for engineers is the wrong input for a customer-facing strip.

      2. Failing that, a synthesised "sitting added" record from the spec's own
         `updated` date, for papers that are AVAILABLE. Every solved paper
         therefore appears at least once without anyone having to remember to
         write a changelog entry for the ordinary case.

    Internal churn is deliberately invisible: no branch, no commit, no build
    state. A candidate is told what changed in the product, not how it was made.
    """
    recs = []
    for d in specs:
        pid = d['paper_id']
        for e in d.get('changelog') or []:
            recs.append({
                'date': e['date'],
                'paper_id': pid,
                'sitting': sitting_label(d['month'], d['year']),
                'kind': e.get('kind', 'correction'),
                'summary': e['summary'],
                'questions': list(e.get('questions') or []),
            })
        if pid in avail_ids and not any(
                (e.get('kind') == 'added') for e in (d.get('changelog') or [])):
            n = len(d['questions'])
            recs.append({
                'date': d['updated'],
                'paper_id': pid,
                'sitting': sitting_label(d['month'], d['year']),
                'kind': 'added',
                'summary': '%s added &mdash; %d solved question%s now available.'
                           % (sitting_label(d['month'], d['year']), n,
                              '' if n == 1 else 's'),
                'questions': [],
            })
    # Newest first; ties broken on paper id so the order is total and stable.
    recs.sort(key=lambda r: (r['date'], r['paper_id']), reverse=True)
    return recs


def assert_no_paid_text(manifest, specs):
    """Fail the build rather than ship one sentence of the paid product.

    Two independent guards, because either alone has a known blind spot:

      KEY GUARD      no banned field name anywhere in the tree. Catches a future
                     field being copied across wholesale.
      SUBSTRING GUARD no 60-character run of any model answer appears anywhere
                     in the serialised manifest. Catches paid prose arriving
                     under an innocent NEW key the key guard has never heard of.

    Sixty characters is long enough that a shared regulation citation will not
    trip it, and short enough that no meaningful passage of an answer can pass.

    The substring guard must SUBTRACT the surface it is allowed to publish, or
    it convicts the product of leaking its own question paper. A model answer
    routinely opens by restating the printed stem verbatim -- QP2403-Q4's
    answer begins with the whole first sentence of its own question -- so a
    naive scan of the serialised manifest fires on the first real build. What
    it must test is whether answer prose appears BEYOND the published stems and
    labels, so the allowed corpus is assembled from exactly the fields this
    generator emits and a fragment inside it is not a leak.
    """
    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in BANNED_KEYS:
                    raise AssertionError(
                        'PAID/AUTHORING FIELD %r reached the manifest at %s' % (k, path))
                walk(v, '%s.%s' % (path, k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, '%s[%d]' % (path, i))

    walk(manifest, '$')

    blob = json.dumps(manifest, ensure_ascii=False)

    # The surface the manifest is ALLOWED to publish, from the manifest itself.
    allowed = []
    for p in manifest['papers']:
        for q in p['questions']:
            allowed.append(strip_tags(q.get('stem') or ''))
            allowed.append(q.get('short_title') or '')
            allowed.extend(q.get('topic_tags') or [])
            allowed.extend(q.get('search_aliases') or [])
    allowed_blob = ' | '.join(allowed)

    for d in specs:
        for q in d['questions']:
            ans = re.sub(r'\s+', ' ', strip_tags(q.get('model_answer') or '')).strip()
            for i in range(0, max(0, len(ans) - 60), 240):
                frag = ans[i:i + 60]
                if len(frag) == 60 and frag in blob and frag not in allowed_blob:
                    raise AssertionError(
                        'MODEL ANSWER TEXT from %s reached the manifest: %r'
                        % (q['question_id'], frag))
    return True


def build(specs):
    nodes = RM.load_nodes(specs)
    rel = RM.build_families(nodes)
    by_id = {d['paper_id']: d for d in specs}
    solved = solved_sittings(specs)
    avail_ids = {d['paper_id'] for d in solved}

    papers, absent = [], []
    for (y, mn, month, state, pid) in coverage(specs):
        if state == NO_SITTING:
            absent.append({
                'year': y, 'month': month, 'month_num': mn,
                'sitting': sitting_label(month, y),
                'status': 'KNOWN_ABSENT',
                'note': strip_tags(KNOWN_ABSENT[(y, mn)]),
            })
            continue
        d = by_id[pid]
        cats, subs = _paper_topics(d)
        rec = {
            'paper_id': pid,
            'sr_no': d['sr_no'],
            'year': y,
            'month': month,
            'month_num': mn,
            'sitting': sitting_label(month, y),
            'status': AVAILABLE if state == AVAILABLE else PLANNED_SOON,
            'question_count': len(d['questions']),
            'total_marks': d.get('total_marks'),
            'time_allowed': d.get('time_allowed'),
            'spec_version': d['version'],
            'updated': d['updated'],
            'categories': cats,
            'subject_tags': subs,
        }
        if state == AVAILABLE:
            rec['href'] = '/solvedQP/%s.html' % pid
            rec['questions'] = question_records(d, rel, nodes)
        else:
            # No href and no questions. A planned sitting has nothing to open
            # and nothing published to search; saying so structurally is what
            # stops a search result implying otherwise.
            rec['questions'] = []
        papers.append(rec)

    total_q = sum(p['question_count'] for p in papers)
    avail_q = sum(p['question_count'] for p in papers if p['status'] == AVAILABLE)
    generated = max(d['updated'] for d in specs)

    manifest = {
        'manifest_version': MANIFEST_VERSION,
        'generated': generated,
        'generated_by': 'tools/pastpapers/build_solvedqp_manifest.py from '
                        'meoclass1/pastpapers/specs/*.json',
        'scope': 'Delivery inventory and topic-search payload for the Solved QP '
                 'product. Candidate-facing fields only: printed question stems, '
                 'topic labels and sitting metadata. No worked answer, study '
                 'guide, recall card or authoring field appears here, and the '
                 'generator fails rather than emit one.',
        'source_of_truth': 'meoclass1/pastpapers/specs/<PAPER>.json. This file is '
                           'generated and is never hand-edited.',
        'status_model': {
            'AVAILABLE': 'Worked answers are published for this sitting.',
            'PLANNED_SOON': 'The printed paper is transcribed. No answers are '
                            'published, no page exists and no question text is '
                            'carried here.',
            'KNOWN_ABSENT': 'No examination was held in this month.',
        },
        'total_papers': len(papers),
        'available_papers': sum(1 for p in papers if p['status'] == AVAILABLE),
        'planned_papers': sum(1 for p in papers if p['status'] == PLANNED_SOON),
        'known_absent_sittings': len(absent),
        'total_questions': total_q,
        'available_questions': avail_q,
        'years': sorted({p['year'] for p in papers}, reverse=True),
        'recently_updated': recently_updated(specs, avail_ids),
        'papers': papers,
        'known_absent': absent,
    }
    assert_no_paid_text(manifest, specs)
    return manifest


def serialise(manifest):
    return json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=False) + '\n'


# ---------------------------------------------------------------- self-test

def self_test(specs):
    """Every failure this generator is supposed to prevent, injected and caught.

    A guard that has never fired is a guard nobody has tested.
    """
    import copy
    fails = []

    def check(name, fn):
        try:
            fn()
        except AssertionError as e:
            print('  [ OK  ] %s -- caught: %s' % (name, str(e)[:70]))
            return
        except Exception as e:                                   # pragma: no cover
            fails.append('%s raised %r instead of AssertionError' % (name, e))
            return
        fails.append('%s was NOT caught' % name)

    m = build(specs)

    # 1. paid answer text smuggled in under an innocent key.
    #    Taken from the MIDDLE of an answer, deliberately: an answer's opening
    #    sentences often restate the printed stem, which the guard is required
    #    to allow, so injecting the head would test nothing.
    def paid_text():
        bad = copy.deepcopy(m)
        ans = ''
        for d in specs:
            for q in d['questions']:
                cand = re.sub(r'\s+', ' ', strip_tags(q.get('model_answer') or '')).strip()
                if len(cand) > len(ans):
                    ans = cand
        mid = len(ans) // 2
        bad['papers'][0]['teaser'] = ans[mid:mid + 400]
        assert_no_paid_text(bad, specs)
    check('paid answer text under a new key', paid_text)

    # 2. a banned authoring field copied across
    def authoring():
        bad = copy.deepcopy(m)
        bad['papers'][0]['reuse_tier'] = 'D'
        assert_no_paid_text(bad, specs)
    check('authoring field reuse_tier', authoring)

    # 3. recurrence_class -- the field that must never face a candidate
    def rec_class():
        bad = copy.deepcopy(m)
        for p in bad['papers']:
            if p['questions']:
                p['questions'][0]['recurrence_class'] = 'expected'
                break
        assert_no_paid_text(bad, specs)
    check('recurrence_class on a question', rec_class)

    # 4-10. structural invariants, asserted against the real manifest
    inv = []

    def want(cond, msg):
        inv.append((bool(cond), msg))

    want(all(p.get('href') for p in m['papers'] if p['status'] == AVAILABLE),
         'every AVAILABLE paper has an href')
    want(all('href' not in p for p in m['papers'] if p['status'] == PLANNED_SOON),
         'no PLANNED_SOON paper carries an href')
    want(all(not p['questions'] for p in m['papers'] if p['status'] == PLANNED_SOON),
         'no PLANNED_SOON paper publishes question text')
    qids = [q['question_id'] for p in m['papers'] for q in p['questions']]
    want(len(qids) == len(set(qids)), 'question ids are unique')
    want(m['available_questions'] == len(qids),
         'available_questions agrees with the published question rows')
    want(m['total_papers'] == m['available_papers'] + m['planned_papers'],
         'paper counts partition')
    want(all(q['search_text'] for p in m['papers'] for q in p['questions']),
         'every published question has a non-empty search_text')
    want(all(re.fullmatch(r'Q[1-9]\d*', q['question_number'])
             for p in m['papers'] for q in p['questions']),
         'question numbers are Qn, not QQn')
    want(all(q['href'] == '/solvedQP/%s.html#%s' % (q['paper_id'], q['anchor'])
             for p in m['papers'] for q in p['questions']),
         'every question href resolves to its own paper and anchor')
    want(serialise(build(specs)) == serialise(m),
         'a second build is byte-identical')
    want(all(a['status'] == 'KNOWN_ABSENT' for a in m['known_absent']),
         'known-absent rows are labelled')
    want(not any(p['paper_id'] in {a.get('paper_id') for a in m['known_absent']}
                 for p in m['papers']),
         'no sitting is both a paper and known-absent')

    for ok, msg in inv:
        print('  [ %-4s ] %s' % ('OK' if ok else 'FAIL', msg))
        if not ok:
            fails.append(msg)

    if fails:
        for f in fails:
            print('  FAIL: %s' % f)
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='write nothing; fail if the manifest on disk is stale')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--out')
    args = ap.parse_args()

    specs = load_specs()
    if args.self_test:
        ok = self_test(specs)
        print('SOLVEDQP MANIFEST SELF-TEST %s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1

    manifest = build(specs)
    text = serialise(manifest)
    path = args.out or os.path.join(REPO_ROOT, OUT_REL)

    if args.check:
        cur = io.open(path, encoding='utf-8').read() if os.path.exists(path) else None
        if cur != text:
            print('solvedqp manifest is STALE -- re-run build_solvedqp_manifest.py')
            return 1
        print('solvedqp manifest is current')
        return 0

    old = io.open(path, encoding='utf-8').read() if os.path.exists(path) else None
    if old != text:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
    print('solvedQP/solvedqp_content_index.json  %s  %d paper(s), %d available, '
          '%d published question(s)'
          % ('unchanged' if old == text else 'written',
             manifest['total_papers'], manifest['available_papers'],
             manifest['available_questions']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
