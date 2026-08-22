#!/usr/bin/env python3
"""Acceptance for the study cockpit: START HERE, STUDY QUEUE and every route.

Two halves, and the second is the one that matters.

POSITIVE  -- the workbook says what it should say: START HERE is first, the
             current topic and session are DERIVED (not typed), every task
             carries a resolving link, progress came from the JSON.

MUTATION  -- each gate is broken on purpose and must go red. A check that has
             never been seen to fail is not evidence that anything is right.
             This repo has been bitten before by self-tests that harvested
             live state and so passed vacuously; these mutations edit real
             inputs in place and restore them in a finally block.

Usage:
    python tools/study/test_roadmap_cockpit.py
"""
import io
import json
import os
import shutil
import subprocess
import sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import export_roadmap_xlsx as EXPORT
import study_links as LINKS

D = os.path.join(ROOT, 'docs', 'study')
SESSIONS = os.path.join(D, 'study_sessions.json')
PROGRESS = os.path.join(D, 'study_progress.json')
PACK = os.path.join(D, 'TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md')
EXPORTER = os.path.join(HERE, 'export_roadmap_xlsx.py')
WORKBOOK = os.path.join(D, 'MIW_MEO_Class1_Study_Roadmap.xlsx')

ENV = dict(os.environ, PYTHONIOENCODING='utf-8')
PASS, FAIL = [], []


def ok(label, cond, detail=''):
    (PASS if cond else FAIL).append(label)
    if not cond:
        print('  FAIL %s%s' % (label, (': ' + detail) if detail else ''))


def _run(args):
    r = subprocess.run([sys.executable, EXPORTER] + args, cwd=ROOT, env=ENV,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


# --------------------------------------------------------------------------- #
# Positive
# --------------------------------------------------------------------------- #
def positive():
    model = EXPORT.build_model()
    cur = model['current']

    ok('sessions are current against their topic pack',
       model['sessions_doc']['pack_status'] == 'CURRENT',
       model['sessions_doc']['pack_status'])

    ok('a current topic is derived', bool(cur['topic']) or cur['all_complete'])
    if cur['topic']:
        # Derived, not asserted: it must be the first topic in STUDY ORDER
        # that has not reached the last stage of the declared progression.
        done = model['progression'][-1]
        earlier = [t for t in model['topics']
                   if t['study_order'] < cur['topic']['study_order']
                   and t['study_status'] != done]
        ok('current topic is the first unfinished topic in study order',
           not earlier, str([t['topic_id'] for t in earlier]))
        ok('current topic carries a reason', bool(cur['why']))

    ok('the current session has tasks', bool(model['current_tasks'])
       or not cur['session'])

    # Every task that names a question must resolve, and the question must be
    # one the governed mapping store knows about.
    store = json.load(open(os.path.join(D, 'study_mappings.json'),
                           encoding='utf-8'))['mappings']
    unresolved, unmapped = [], []
    for t in model['queue']:
        qid = t['question_id']
        if not qid:
            continue
        if qid not in store:
            unmapped.append(qid)
        if not (t['link'] or {}).get('ok'):
            unresolved.append(qid)
    ok('every queued question exists in study_mappings', not unmapped,
       str(unmapped[:5]))
    ok('every queued question resolves to a live route', not unresolved,
       str(unresolved[:5]))

    ok('no route in the whole workbook is dead',
       not model['link_failures'],
       str([f['reason'] for f in model['link_failures']][:3]))

    ok('the topic pack link resolves for the current topic',
       (cur['topic'] or {}).get('link_pack', {}).get('ok', True))

    ok('the mental skeleton is carried in the workbook',
       len(model['skeleton']) > 0, str(len(model['skeleton'])))

    ok('written questions are listed with topic and link',
       len(model['written_by_topic']) > 0
       and all(r['link']['ok'] for r in model['written_by_topic']))

    # Progress is read, never written.
    before = open(PROGRESS, 'rb').read()
    EXPORT.build_model()
    ok('building the model does not touch study_progress.json',
       open(PROGRESS, 'rb').read() == before)

    rc, out = _run(['--check'])
    ok('--check passes on the committed workbook', rc == 0, out.strip()[:200])


# --------------------------------------------------------------------------- #
# Mutation -- every gate must be shown to fire
# --------------------------------------------------------------------------- #
def mutate(label, files, apply_fn, rebuild=True):
    baks = {f: f + '.mutbak' for f in files}
    for f, b in baks.items():
        shutil.copy2(f, b)
    try:
        apply_fn()
        if rebuild:
            _run([])
        rc, out = _run(['--check'])
        ok('mutation caught: ' + label, rc != 0, 'check passed anyway')
        if rc != 0:
            first = next((l for l in out.splitlines() if l.startswith('FAIL')), '')
            print('    %s -> %s' % (label, first[:120]))
    finally:
        for f, b in baks.items():
            shutil.copy2(b, f)
            os.remove(b)


def _edit_session(fn):
    doc = json.load(open(SESSIONS, encoding='utf-8'))
    fn(doc)
    with open(SESSIONS, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')


def mutations():
    def m_pack():
        with open(PACK, 'a', encoding='utf-8') as fh:
            fh.write('\nmutation\n')
    mutate('topic pack edited, sessions not re-derived', [PACK], m_pack)

    mutate('session cites an anchor that does not exist', [SESSIONS],
           lambda: _edit_session(lambda d: d['sessions'][0]['tasks'][1]
                                 .__setitem__('question_id', 'QB1_H#q999')))

    mutate('session cites a paper with no product page', [SESSIONS],
           lambda: _edit_session(lambda d: d['sessions'][0]['tasks'][7]
                                 .__setitem__('question_id', 'QP2101-Q1')))

    def m_prog():
        doc = json.load(open(PROGRESS, encoding='utf-8'))
        doc['topics']['D01']['status'] = 'ORAL_CORE_COMPLETE'
        with open(PROGRESS, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    # Deliberately NOT rebuilt: this is the "you advanced but the workbook is
    # stale" case, which is exactly what a progress-preservation check is for.
    mutate('progress advanced but workbook not regenerated', [PROGRESS],
           m_prog, rebuild=False)


def main():
    print('study cockpit acceptance')
    positive()
    mutations()
    _run([])                        # leave a clean workbook behind
    rc, _ = _run(['--check'])
    ok('workbook is clean again after the mutation suite', rc == 0)
    print('  %d assertions' % (len(PASS) + len(FAIL)))
    if FAIL:
        print('\n%d FAILED' % len(FAIL))
        return 1
    print('  all %d PASS' % len(PASS))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
