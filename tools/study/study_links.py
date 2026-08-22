#!/usr/bin/env python3
"""Derive every study route from repo truth, and prove each one resolves.

    canonical id  --->  build_*_link()  --->  {url, repo_path, anchor, ok}
                              |
                              +--> validate()  reads the actual HTML and
                                   asserts the anchor id is really there

WHY THIS IS A MODULE AND NOT AN f-STRING IN THE EXPORTER
--------------------------------------------------------
A hyperlink is a claim about the product. A claim typed into a renderer is a
claim nobody checks. Every route here is built from the same governed ids the
rest of the study system uses, and `validate()` opens the destination file and
looks for the anchor -- so a workbook can never ship a link into a page that
does not exist or an anchor that was renamed.

Two anchor conventions, because the two corpora genuinely differ:

    ORAL     QB1_H#q3        -> meoclass1/QB1_H.html#q3
                                (anchor is the short in-file id)
    WRITTEN  QP2506-Q2       -> solvedQP/QP2506.html#QP2506-Q2
                                (anchor IS the canonical id)

NOT-YET-AVAILABLE IS A FIRST-CLASS RESULT. A route that does not exist returns
`ok=False` with a reason, and callers render NOT YET AVAILABLE. A dead
hyperlink is worse than an honest blank: it costs the candidate a click and
teaches him not to trust the workbook.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

SITE = 'https://marineintelligenceweekly.com'
NOT_AVAILABLE = 'NOT YET AVAILABLE'

# Site surfaces, as they exist on disk today.
STUDY_PAGE = ('meoclass1/study.html', 'gated')
TOPIC_PAGE = ('meoclass1/topics.html', 'gated')
ORAL_DIR = 'meoclass1'
WRITTEN_DIR = 'solvedQP'
PACK_DIR = os.path.join('docs', 'study')

_ANCHOR_CACHE = {}


def _anchors(repo_path):
    """Every id="..." in a file. Cached -- the exporter asks repeatedly."""
    if repo_path not in _ANCHOR_CACHE:
        full = os.path.join(ROOT, repo_path)
        if not os.path.exists(full):
            _ANCHOR_CACHE[repo_path] = None
        else:
            with open(full, encoding='utf-8', errors='replace') as fh:
                html = fh.read()
            _ANCHOR_CACHE[repo_path] = set(re.findall(r'id="([^"]+)"', html))
    return _ANCHOR_CACHE[repo_path]


def _link(repo_path, anchor, label):
    """Build a checked link record. `anchor` may be None for a whole page."""
    ids = _anchors(repo_path)
    if ids is None:
        return {'ok': False, 'reason': f'no such file: {repo_path}',
                'url': None, 'repo_path': repo_path, 'anchor': anchor,
                'label': label}
    if anchor and anchor not in ids:
        return {'ok': False, 'reason': f'no anchor #{anchor} in {repo_path}',
                'url': None, 'repo_path': repo_path, 'anchor': anchor,
                'label': label}
    url = f'{SITE}/{repo_path}' + (f'#{anchor}' if anchor else '')
    return {'ok': True, 'reason': None, 'url': url, 'repo_path': repo_path,
            'anchor': anchor, 'label': label}


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
def study_topic(topic_id):
    """The gated study landing, anchored at one topic."""
    return _link(STUDY_PAGE[0], topic_id, f'Study {topic_id}')


def oral_topic(topic_id):
    """The gated oral topic index -- every oral question for the topic."""
    return _link(TOPIC_PAGE[0], topic_id, f'Orals {topic_id}')


def oral_question(qid):
    """`QB1_H#q3` -> meoclass1/QB1_H.html#q3."""
    if '#' not in qid:
        return {'ok': False, 'reason': f'not an oral canonical id: {qid}',
                'url': None, 'repo_path': None, 'anchor': None, 'label': qid}
    stem, anchor = qid.split('#', 1)
    return _link(f'{ORAL_DIR}/{stem}.html', anchor, qid)


def written_question(qid):
    """`QP2506-Q2` -> solvedQP/QP2506.html#QP2506-Q2.

    Only SOLVED papers have a product page. A question whose paper is
    intelligence-only correctly returns not-available rather than a 404.
    """
    m = re.fullmatch(r'(QP\d{4})-Q(\d+)', qid)
    if not m:
        return {'ok': False, 'reason': f'not a written canonical id: {qid}',
                'url': None, 'repo_path': None, 'anchor': None, 'label': qid}
    return _link(f'{WRITTEN_DIR}/{m.group(1)}.html', qid, qid)


def written_paper(paper_id):
    return _link(f'{WRITTEN_DIR}/{paper_id}.html', paper_id, paper_id)


def topic_pack(topic_id):
    """Nixon's local study pack, as a Windows-safe file:/// URL.

    Local file links are the one route that cannot be proved to *open* -- only
    to exist. Excel will follow file:/// reliably; whether Windows has a
    handler for .md is the user's shell association, not something this tool
    can assert. The workbook therefore also renders the pack's mental skeleton
    internally, so a pack that will not open is an inconvenience, not a
    blocker.
    """
    num = topic_id[1:] if topic_id.startswith('D') else topic_id
    prefix = f'TOPIC_{num}_'
    d = os.path.join(ROOT, PACK_DIR)
    hit = None
    if os.path.isdir(d):
        for name in sorted(os.listdir(d)):
            if name.startswith(prefix) and name.endswith('.md'):
                hit = name
                break
    if not hit:
        return {'ok': False, 'reason': f'no topic pack for {topic_id}',
                'url': None, 'repo_path': None, 'anchor': None,
                'label': f'{topic_id} pack'}
    repo_path = f'{PACK_DIR}/{hit}'.replace(os.sep, '/')
    full = os.path.join(ROOT, PACK_DIR, hit).replace(os.sep, '/')
    return {'ok': True, 'reason': None, 'url': 'file:///' + full,
            'repo_path': repo_path, 'anchor': None, 'label': hit,
            'local': True}


def question_link(qid):
    """Dispatch on the id's own shape -- oral ids carry '#', written carry '-Q'."""
    return oral_question(qid) if '#' in qid else written_question(qid)


def validate(links):
    """Return the failures. An empty list is the only passing result."""
    return [l for l in links if not l['ok']]
