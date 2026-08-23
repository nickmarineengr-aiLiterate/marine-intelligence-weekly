#!/usr/bin/env python3
"""Deterministic integrity tests for questions-<year>.html.

Two families of test, and the second matters more.

POSITIVE  -- every canonical question is present, exactly once, under the right
             month, with its printed marks and a correct recurrence tag.

NEGATIVE  -- no answer content reached the artefact, and no third-party
             recurrence annotation did either. These are the tests that would
             catch the page quietly becoming a free copy of the paid product,
             and they check the shipped BYTES, not the rendered view: content
             that is merely hidden by CSS has still been given away.

Run standalone or from run_toolchain.py.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from html import unescape as _unescape
from render_common import REPO_ROOT, strip_tags
import recurrence_model as RM

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')

# A source-copy host recurrence annotation: 2018/APR, 2025/SEP/Q6, 2022/MAR/1.
HOST_RECURRENCE = re.compile(r'\b(19|20)\d{2}/[A-Z]{3,5}\b')


def _norm(s):
    """Tag-free, lowercase, whitespace-collapsed. Leak testing compares BYTES
    that a reader could recover, so markup and spacing must not hide a match."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(s))).strip().lower()


def _sentences(blocks, min_words=9):
    """Distinctive prose fragments from an answer, for leak testing."""
    if not blocks:
        return []
    buf = []
    for b in blocks.get('blocks', []):
        if 'p' in b:
            buf.append(b['p'])
        for k in ('ul', 'ol'):
            for item in b.get(k, []):
                buf.append(item)
    out = []
    for chunk in buf:
        for s in re.split(r'(?<=[.;])\s+', strip_tags(chunk)):
            s = s.strip()
            if len(s.split()) >= min_words:
                out.append(s)
    return out


def check_year(year, errors, warnings):
    path = os.path.join(PP_DIR, 'questions-%d.html' % year)
    if not os.path.exists(path):
        errors.append('questions-%d.html does not exist' % year)
        return
    html = open(path, encoding='utf-8').read()

    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    nodes = RM.load_nodes(specs)
    relations = RM.build_families(nodes)
    year_nodes = [n for n in nodes.values() if n['year'] == year]

    if not year_nodes:
        errors.append('no canonical questions for %d' % year)
        return

    # ---- POSITIVE ---------------------------------------------------------
    ids = re.findall(r'id="(QP\d{4}-Q\d+)"', html)
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append('duplicate question ids in the page: %s' % ', '.join(dupes))
    missing = sorted({n['question_id'] for n in year_nodes} - set(ids))
    if missing:
        errors.append('%d canonical question(s) missing from the page: %s'
                      % (len(missing), ', '.join(missing)))
    extra = sorted(set(ids) - {n['question_id'] for n in year_nodes})
    if extra:
        errors.append('page carries question ids not in the %d canonical set: %s'
                      % (year, ', '.join(extra)))

    for n in year_nodes:
        # The FULL printed stem must be present, not a preview. Compare on
        # collapsed whitespace so the line-splitting in the renderer is allowed.
        stem = re.sub(r'\s+', ' ', strip_tags(n['text_verbatim'])).strip()
        # Unescape before comparing. The spec holds "Hull & Propeller"; the page
        # correctly holds "Hull &amp; Propeller", so comparing raw spec text
        # against escaped HTML reports a missing stem for any question with an
        # ampersand -- or any other escaped character -- in its first 120
        # characters. No 2026 stem had one, so this stayed latent until the 2025
        # intake landed three of them.
        flat = _unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html)))
        if stem[:120] not in flat:
            errors.append('%s printed stem not found in the page' % n['question_id'])
        if '%s marks' % n['marks'] not in html:
            warnings.append('%s printed marks (%s) not rendered'
                            % (n['question_id'], n['marks']))

    # All twelve months named, so a gap is always explicit rather than silent.
    for mn in range(1, 13):
        if '%s %d' % (RM.MONTHS[mn - 1], year) not in html:
            errors.append('%s %d does not appear on the page' % (RM.MONTHS[mn - 1], year))

    # A month with no sitting must say WHY, and a known-absent sitting must not
    # be described the same way as one MIW simply has not built.
    from build_questions_year import KNOWN_ABSENT
    for (y, mn), _ in KNOWN_ABSENT.items():
        if y != year:
            continue
        month = RM.MONTHS[mn - 1]
        seg = html.split('%s %d' % (month, year), 1)
        if len(seg) < 2 or 'No examination paper exists' not in seg[1][:900]:
            errors.append('%s %d is a known-absent sitting but the page does not say so'
                          % (month, year))

    # Recurrence tag must match the CHRONOLOGY, not the authoring field.
    for n in year_nodes:
        rel = relations[n['question_id']]
        block = _card_block(html, n['question_id'])
        if block is None:
            continue
        if 'data-rec="%s"' % rel['filter'] not in block:
            errors.append('%s recurrence filter tag is wrong (expected %s)'
                          % (n['question_id'], rel['filter']))

    # ---- NEGATIVE ---------------------------------------------------------
    spec_q = {q['question_id']: q for d in specs for q in d['questions']}
    html_norm = _norm(html)   # normalised once; the sweep runs ~600 fragments
    leaks = 0
    for n in year_nodes:
        q = spec_q[n['question_id']]
        # An answer layer legitimately quotes the printed question -- QP2602-Q7's
        # answer_route step is word-for-word the examiner's own "(ii) signature
        # subject to ratification, acceptance or approval". Finding that on a page
        # whose entire purpose is to print the question is not a leak, and a sweep
        # that cannot tell the difference is the April false-positive lesson
        # repeating. Anything already present in the stem is adjudicated out.
        stem_norm = _norm(n['text_verbatim'] + ' ' +
                          ' '.join(sp.get('text', '') for sp in n['subparts']))

        def leaked(fragment, minimum=40):
            f = _norm(fragment)
            return len(f) >= minimum and f in html_norm and f not in stem_norm

        for s in _sentences(q.get('model_answer'))[:6] + _sentences(q.get('study_notes'))[:4]:
            if leaked(s[:70]):
                errors.append('ANSWER LEAK: %s model/study prose present in the page: %r'
                              % (n['question_id'], s[:70]))
                leaks += 1
                if leaks > 8:
                    return
        qr = q.get('quick_revision') or {}
        if leaked(strip_tags(qr.get('recall_15s') or '')[:60]):
            errors.append('ANSWER LEAK: %s quick-revision recall text present'
                          % n['question_id'])
        for card in (q.get('retrieval_cards') or [])[:3]:
            if leaked(strip_tags(card.get('answer', ''))[:60]):
                errors.append('ANSWER LEAK: %s retrieval card answer present' % n['question_id'])
        for step in (q.get('answer_route') or {}).get('steps', [])[:3]:
            for pt in (step.get('points') or [])[:2]:
                if leaked(strip_tags(pt)[:55]):
                    errors.append('ANSWER LEAK: %s answer_route point %r present'
                                  % (n['question_id'], strip_tags(pt)[:55]))

    hits = sorted(set(HOST_RECURRENCE.findall(html)))
    raw = HOST_RECURRENCE.search(html)
    if raw:
        errors.append('THIRD-PARTY RECURRENCE LEAK: source-copy annotation %r reached the page'
                      % raw.group(0))

    if 'noindex' not in html:
        warnings.append('questions-%d.html is not noindex (publish build?)' % year)


def _card_block(html, qid):
    i = html.find('id="%s"' % qid)
    if i < 0:
        return None
    return html[max(0, i - 400):i + 2500]



# --------------------------------------------------------------------------- #
# THE WORDING ARCHIVE  --  questions-2021 / questions-2022
# --------------------------------------------------------------------------- #
#
# These sheets carry questions MIW has NOT answered, on the same URL shape as
# the sheets for years it has. That is deliberate -- a candidate should be able
# to walk the chronology without learning a second convention -- and it is
# exactly why they need their own tests. The failure to prevent is not a broken
# page. It is a page that looks like the paid product.
#
# The boundary test is the one to read twice. 2021 and 2022 are publishable
# because their sitting dates are PRINTED ON A SOURCE COPY. 2010 to 2020 reach
# MIW as SECONDARY_CLAIMED dates through a web archive, and a year page is a
# dated claim about every question on it. So a questions-2020.html is not a
# smaller version of this work; it is a different product with a different
# provenance vocabulary, and until that exists this gate refuses the file.

import build_questions_year as BQY

#: Phrases that assert a solved product. None may appear on an archive sheet.
SOLVED_CLAIMS = (
    'solved paper available',
    'open the solved paper',
    'open the solved answer',
    'current answer verified',
)


def _archive_papers():
    return BQY.load_archive()


def check_archive(errors, warnings):
    """Rules A to K for every published wording-archive sheet."""
    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    archive = _archive_papers()
    years = BQY.archive_years(specs, archive)

    sys.path.insert(0, os.path.join(REPO_ROOT, 'tools', 'study'))
    import qi_projection as QIP

    solved_ids = {q['question_id'] for d in specs for q in d['questions']}

    for year in years:
        expected = sorted(q['question_id']
                          for ms in archive[year].values()
                          for p in ms for q in p['questions'])
        for path in (os.path.join(PP_DIR, 'questions-%d.html' % year),
                     os.path.join(REPO_ROOT, 'solvedQP', 'questions-%d.html' % year)):
            rel = os.path.relpath(path, REPO_ROOT).replace('\\', '/')
            if not os.path.exists(path):
                errors.append('ARCHIVE-A %s: archive year %d has no sheet' % (rel, year))
                continue
            html = open(path, encoding='utf-8').read()
            low = html.lower()
            got = re.findall(r'<div class="hit" data-qsearch="[^"]*" id="([^"]+)">', html)

            # A -- derives from the governed archive store, question for question.
            if sorted(got) != expected:
                errors.append('ARCHIVE-A %s: rendered question set does not match the '
                              'archive store (%d rendered, %d held)'
                              % (rel, len(got), len(expected)))

            # B -- no duplicates. A repeated card doubles a question silently.
            if len(got) != len(set(got)):
                errors.append('ARCHIVE-B %s: a question is rendered more than once' % rel)

            # C -- NO FABRICATION. Every id on the page exists in the store.
            ghosts = sorted(set(got) - set(expected))
            if ghosts:
                errors.append('ARCHIVE-C %s: question(s) on the page that the archive '
                              'store does not hold: %s' % (rel, ghosts[:5]))

            # D -- no solved-answer claim, in any of its wordings.
            #
            # Scanned with the LEGEND BLOCKS REMOVED. The legend has to name the
            # readiness vocabulary in order to explain whose answer it describes
            # -- including "Current answer verified" -- and a rule that cannot
            # tell an explanation from an assertion would force the page to
            # choose between passing the gate and telling the truth. Everything
            # else on the page, chips and headings included, is still scanned.
            body = re.sub(r'<section class="topic-group qy-legend">.*?</section>',
                          ' ', low, flags=re.S)
            for claim in SOLVED_CLAIMS:
                if claim in body:
                    errors.append('ARCHIVE-D %s: asserts %r on a sheet MIW has not '
                                  'solved' % (rel, claim))

            # E -- no link into a solved paper or answer anchor. The successor
            #      is rendered as a SENTENCE by qi_projection for this reason.
            for href in re.findall(r'href="([^"]+)"', html):
                if re.search(r'/(solvedQP|pastpapers)/QP\d{4}[^"]*\.html', href):
                    errors.append('ARCHIVE-E %s: links to a solved paper (%s). An archive '
                                  'question must not resolve to an answer.' % (rel, href))
                    break

            # F -- Layer 1 stays off. The calendar recurrence model is built from
            #      the SPEC set; a modern tag here would either be invented or
            #      would mean the archive had been fed into that model, which
            #      rewrites the tags on 2023-2026.
            for tag in ('>Repeated<', '>First in set<', '>Once in MIW'):
                if tag in html:
                    errors.append('ARCHIVE-F %s: carries a Layer-1 recurrence tag (%s). '
                                  'Those are computed from the solved calendar.'
                                  % (rel, tag.strip('<>')))

            # G -- longitudinal tags come from the candidate-safe projection and
            #      match it question by question. Not "are in the vocabulary" --
            #      are the ones THIS question was projected.
            for qid in got:
                want = {t for _, t in QIP.tags_for(qid, audience='GATED')}
                block = _archive_card(html, qid)
                for chip in re.findall(r'<span class="q-tag[^"]*">([^<]+)</span>', block):
                    c = _unescape(chip).strip()
                    if c in ('Question wording held', 'No sitting',
                             'Not yet in the MIW set'):
                        continue
                    if _unescape_all(want, c):
                        continue
                    errors.append('ARCHIVE-G %s %s: chip %r is not what the governed '
                                  'projection gives this question' % (rel, qid, c))
                    break

            # H -- no third-party host recurrence annotation.
            m = HOST_RECURRENCE.search(strip_tags(html))
            if m:
                errors.append('ARCHIVE-H %s: source-copy host recurrence annotation '
                              'reached the page (%s)' % (rel, m.group(0)))

            # I -- the page states what it does not have, in terms.
            if 'has not solved these papers' not in low:
                errors.append('ARCHIVE-I %s: does not state that MIW has not solved these '
                              'papers' % rel)
            if '0 solved answers' not in low:
                errors.append('ARCHIVE-I %s: header does not carry the zero-answer count'
                              % rel)

            # J -- counts on the page equal the governed source.
            if ('%d questions' % len(expected)) not in low:
                errors.append('ARCHIVE-J %s: header question count disagrees with the '
                              'archive store (%d held)' % (rel, len(expected)))

            # M -- a readiness chip on this page is about the CONCEPT's answer
            #      elsewhere in the corpus, never about the question printed
            #      here. 55 of the 198 archive questions inherit
            #      READY_TO_STUDY_NOW from their family and render an all-clear;
            #      unqualified, that contradicts the page's own header.
            if 'never this' not in low or 'has been answered by miw' not in low:
                errors.append('ARCHIVE-M %s: renders readiness chips without the sentence '
                              'that says whose answer they describe' % rel)

            # L -- the search on this sheet must not reach into the solved
            #      corpus. The solved year sheets carry an escape hatch that
            #      offers "search all solved papers"; on an archive sheet that
            #      folds two different statuses into one result list, and a
            #      reader who searches "general average" would be shown solved
            #      hits under a heading that says these questions are not
            #      solved. The archive searches itself and stops there.
            # Probe the MARKUP and the SCRIPT, not the stylesheet: the shared
            # CSS defines .mc-wrap for every page that links it, and matching
            # that would fail every archive sheet on a rule about behaviour.
            for probe in ('id="mc-wrap"', 'search all solved papers',
                          'miwcorpus.load'):
                if probe in low:
                    errors.append('ARCHIVE-L %s: carries the solved-corpus search escape '
                                  'hatch (%r), which mixes archive and solved status in '
                                  'one result list' % (rel, probe))
                    break

            # K -- a successor sentence may only name a REAL solved question.
            for sid in re.findall(r'Current framework: see ([A-Za-z0-9\-]+)', html):
                if sid not in solved_ids:
                    errors.append('ARCHIVE-K %s: names %s as the current framework and no '
                                  'such solved question exists' % (rel, sid))

    return years


def _archive_card(html, qid):
    """Exactly one card's markup, bounded by the next card or the next month.

    _card_block() takes a fixed 2,900-character window, which is fine for a
    solved sheet where the cards are long. Archive cards are short: the window
    ran past the end of one card and swept up the chips of the two after it,
    so every question appeared to be carrying its neighbours' tags. A bounded
    slice is the only honest way to ask "what does THIS card say".
    """
    start = html.find('id="%s">' % qid)
    if start < 0:
        return ''
    start = html.rfind('<div class="hit"', 0, start + 1)
    nxt = html.find('<div class="hit"', start + 1)
    end = html.find('<section class="topic-group"', start + 1)
    stops = [x for x in (nxt, end) if x > 0]
    return html[start:min(stops)] if stops else html[start:]


def _unescape_all(want, chip):
    """True if `chip` matches any projected tag once entities are folded."""
    return any(_unescape(strip_tags(w)).strip() == chip for w in want)


def check_pre_archive_boundary(errors):
    """No year page below the floor, and no navigation reaching for one.

    This is the guard that keeps 2010-2020 out of the standard chronology. It
    is deliberately a FILESYSTEM test as well as a link test: a page can exist
    and be unlinked, and it is still published.
    """
    floor = BQY.ARCHIVE_FLOOR
    for root in (PP_DIR, os.path.join(REPO_ROOT, 'solvedQP')):
        for path in sorted(glob.glob(os.path.join(root, 'questions-*.html'))):
            m = re.search(r'questions-(\d{4})\.html$', os.path.basename(path))
            if m and int(m.group(1)) < floor:
                errors.append('ARCHIVE-BOUNDARY %s exists. Years below %d reach MIW as '
                              'SECONDARY_CLAIMED dates and may not carry a year page '
                              'until a historical-archive design exists.'
                              % (os.path.relpath(path, REPO_ROOT).replace('\\', '/'), floor))
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, 'solvedQP', '*.html'))) + \
            sorted(glob.glob(os.path.join(PP_DIR, '*.html'))):
        html = open(path, encoding='utf-8').read()
        for y in re.findall(r'questions-(\d{4})\.html', html):
            if int(y) < floor:
                errors.append('ARCHIVE-BOUNDARY %s links to questions-%s.html, which is '
                              'below the %d floor'
                              % (os.path.relpath(path, REPO_ROOT).replace('\\', '/'),
                                 y, floor))
                break

def main():
    errors, warnings = [], []
    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    years = sorted({d['year'] for d in specs})
    for y in years:
        check_year(y, errors, warnings)

    # The wording archive is a different product on the same URL shape, so it
    # gets its own rules -- and the boundary guard runs whether or not any
    # archive year exists, because its job is to catch a year appearing.
    arc = check_archive(errors, warnings)
    check_pre_archive_boundary(errors)
    years = years + list(arc)

    for w in warnings:
        print('  WARN  %s' % w)
    for e in errors:
        print('  FAIL  %s' % e)
    if errors:
        print('QUESTIONS YEAR: %d error(s), %d warning(s)' % (len(errors), len(warnings)))
        sys.exit(1)
    print('QUESTIONS YEAR: OK  %d year(s), %d warning(s)' % (len(years), len(warnings)))


if __name__ == '__main__':
    main()
