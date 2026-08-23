#!/usr/bin/env python3
"""The gate for the QI -> study integration. Fails closed.

It answers one question in fifteen ways: did joining the 2010 -> August 2026
longitudinal layer to the study engine cost us any of the 2021 -> August 2026
question-level intelligence MIW already had, or quietly count the same
recurrence twice?

    python tools/study/validate_study_qi.py
"""

import glob
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import study_qi_adapter as A
import study_spine as SP

REPO = A.REPO
DOC = A.DOC

FAILURES = []
CHECKS = []


def check(rule, ok, detail=''):
    CHECKS.append((rule, bool(ok)))
    if not ok:
        FAILURES.append('%-16s %s' % (rule, detail))
    return bool(ok)


def load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def load_context():
    """Everything the gate reads, in one bundle.

    It is a bundle rather than a pile of module-level loads so the mutation
    suite can break one thing at a time in memory. A gate that can only be
    exercised by damaging the real artefacts is a gate nobody runs.
    """
    return {
        'doc': load(os.path.join(DOC, 'study_qi.json')),
        'baseline': load(os.path.join(DOC, 'modern_qi_baseline.json')),
        'holds': load(os.path.join(REPO, 'tools', 'study', 'study_qi_holds.json')),
        'spine': load(os.path.join(DOC, 'study_spine.json')),
        'mappings': load(os.path.join(DOC, 'study_mappings.json'))['mappings'],
        'occurrence_counts': load(os.path.join(DOC, 'qi', 'qi_occurrences.json'))['counts'],
        'modern': A.load_modern_qi(),
        'canonical': A.load_canonical_qi(),
        'public_html': (open(os.path.join(REPO, 'SQ', 'study-roadmap.html'),
                             encoding='utf-8').read()
                        if os.path.exists(os.path.join(REPO, 'SQ', 'study-roadmap.html'))
                        else ''),
        'run_determinism': True,
    }


def run_checks(ctx):
    del FAILURES[:]
    del CHECKS[:]
    doc = ctx['doc']
    baseline = ctx['baseline']
    holds = ctx['holds']
    spine = ctx['spine']
    modern = ctx['modern']
    canonical = ctx['canonical']

    fams = doc['families']
    qs = doc['questions']
    recon = doc['reconciliation']['rows']

    # ---------------------------------------------------------------- A / B
    # The existing modern QI regression baseline is preserved, and every modern
    # repeat tag and relationship still resolves.
    live_with_repeat = {qid for qid, a in modern['authored'].items()
                        if a['host_recurrence_hint'] or a['reused_from']}
    frozen = set(baseline['questions_with_repeat_intelligence'])
    lost = sorted(frozen - live_with_repeat)
    check('R-MODERN-KEEP', not lost,
          '%d modern question(s) lost their repeat intelligence: %s'
          % (len(lost), lost[:8]))

    live_fams = {r['modern_family_id']: r for r in modern['derived_families']
                 if r['size'] > 1}
    frozen_fams = baseline['modern_multi_member_families']
    fam_lost = sorted(set(frozen_fams) - set(live_fams))
    check('R-MODERN-FAM', not fam_lost,
          '%d modern multi-member family(ies) disappeared: %s'
          % (len(fam_lost), fam_lost[:8]))

    shrunk = [fid for fid, rec in frozen_fams.items()
              if fid in live_fams
              and not set(rec['members']) <= set(live_fams[fid]['members'])]
    check('R-MODERN-EDGE', not shrunk,
          '%d modern family(ies) lost members with no migration: %s'
          % (len(shrunk), shrunk[:8]))

    # Every modern relationship leaves the adapter with a disposition.
    undisposed = [r['modern_family_id'] for r in recon if not r.get('disposition')]
    check('R-DISPOSITION', not undisposed,
          '%d modern relationship(s) carry no disposition: %s'
          % (len(undisposed), undisposed[:8]))
    check('R-DISP-VOCAB',
          all(r.get('disposition') in A.MODERN_DISPOSITIONS
              for r in recon if r.get('disposition')),
          'a disposition outside the governed vocabulary was recorded')

    # Every modern related-question edge either points at a real question, or is
    # a pre-2021 backward claim -- the modern layer reaching below the corpus
    # floor on its own authority. Those are not dangling: they are the claims
    # the longitudinal layer exists to corroborate, and they are reported under
    # `authored_backward_claims`. Conflating the two would either hide a real
    # broken edge or manufacture twenty false ones.
    natives = {r['question_id'] for r in qs}
    in_corpus, backward = set(), set()
    for a in modern['authored'].values():
        for t in a['related_question_ids']:
            (backward if t < 'QP21' else in_corpus).add(t)
    known_bad = {x['resolves_to'] for x in
                 holds['known_authored_edge_defects']['defects']}
    dangling = sorted(in_corpus - natives - known_bad)
    stale_allow = sorted(known_bad & natives)
    check('R-EDGE-ALLOW', not stale_allow,
          'edge defect(s) recorded as broken now resolve: %s. Remove the '
          'allowance rather than leaving a spent one in place.' % stale_allow)
    check('R-EDGE-RESOLVE', not dangling,
          '%d in-corpus related-question edge(s) point nowhere: %s'
          % (len(dangling), dangling[:8]))
    # A corroboration rate of zero means the comparison is broken, not that the
    # two layers disagree -- the sitting formats differ between the occurrence
    # id ('2016/APR') and the sitting field ('2016-04'), and string surgery on
    # the id silently reported 0/1067 until it was caught here.
    bc = doc['authored_backward_claims']
    total_claims = bc['corroborated_sittings'] + bc['uncorroborated_sittings']
    check('R-CORROBORATION',
          total_claims and bc['corroborated_sittings'] / total_claims > 0.5,
          'only %d of %d authored sitting claims corroborate against governed '
          'occurrences. Below half means the comparison is broken, not that the '
          'layers disagree -- check the sitting format before believing it.'
          % (bc['corroborated_sittings'], total_claims))

    claimed_back = doc['authored_backward_claims']['claims_pre_2021']
    check('R-EDGE-BACKWARD', claimed_back > 0 and backward,
          'the authored layer makes pre-2021 backward claims but the projection '
          'reports none -- they must stay visible, not be silently dropped')

    # ---------------------------------------------------------------- C
    # Conflicts are held explicitly, never resolved by a build.
    conflicts = [r for r in recon if r['verdict'] == 'CONFLICT']
    unheld = [r['modern_family_id'] for r in conflicts if not r.get('hold_id')]
    check('R-CONF-HELD', not unheld,
          '%d conflict(s) carry no governed hold: %s' % (len(unheld), unheld[:8]))
    check('R-CONF-STATE',
          all(h['state'] in holds['conflict_hold_states']
              for h in holds['conflict_holds']),
          'a conflict hold carries a state outside the governed vocabulary')
    resolved_without_human = [h['hold_id'] for h in holds['conflict_holds']
                              if h['state'] != 'HOLD_RECONCILIATION'
                              and not h.get('adjudicated_by')]
    check('R-CONF-HUMAN', not resolved_without_human,
          'hold(s) resolved with no named adjudicator: %s' % resolved_without_human)

    # The precedence rule claims the deterministic band always agrees. If that
    # ever stops being true the rule is no longer earned and must be re-argued.
    det = [r['modern_family_id'] for r in conflicts
           if r['modern_evidence_class'] == 'DETERMINISTIC']
    check('R-PRECEDENCE', not det,
          'the precedence rule assumes DETERMINISTIC modern families never '
          'conflict, but %d do: %s. Re-argue the rule; do not relax the gate.'
          % (len(det), det[:8]))

    # ---------------------------------------------------------------- D
    # No recurrence double-weighting.
    rm = doc['roadmap_recurrence_input']
    check('R-WEIGHT-SRC', rm['source'] == A.RECURRENCE_WEIGHT_SOURCE,
          'roadmap recurrence source is %r, not the single governed source'
          % rm['source'])
    recurrence_keys = [k for k in rm if k not in
                       ('source', 'measure', 'double_weight_guard', 'by_topic')]
    check('R-WEIGHT-ONE', not recurrence_keys,
          'the roadmap input carries more than one recurrence quantity: %s'
          % recurrence_keys)
    # The modern layer must contribute no independent weight: no question row
    # may carry a recurrence COUNT sourced from the modern layer.
    modern_count_fields = [k for k in (qs[0] if qs else {})
                           if k.startswith('modern_') and k.endswith(
                               ('_count', '_3y', '_5y', '_10y', '_horizon'))]
    check('R-WEIGHT-MOD', not modern_count_fields,
          'the modern layer exposes its own recurrence counts (%s), which the '
          'roadmap could add to the canonical ones' % modern_count_fields)

    # ---------------------------------------------------------------- E
    # Historical variants do not multiply a topic score.
    bearers = Counter(r['canonical_current_question'] for r in fams
                      if r['canonical_current_question'])
    check('R-VARIANT-1', all(v == 1 for v in bearers.values()),
          'a question bears the weight of more than one family: %s'
          % [q for q, v in bearers.items() if v > 1][:8])
    weighted = sum(doc['topics'][d]['mapped_families'] for d in doc['topics'])
    reachable = sum(1 for r in fams if r['weight_topic_id'])
    check('R-VARIANT-2', weighted == reachable,
          'per-topic family counts sum to %d but only %d families bear weight '
          '-- a family is being counted in more than one topic' % (weighted, reachable))
    multi_variant = [r['family_id'] for r in fams
                     if r['historical_variants'] and not r['canonical_current_question']]
    check('R-VARIANT-3', not multi_variant,
          'family(ies) with variants but no bearer: %s' % multi_variant[:8])

    # ---------------------------------------------------------------- F
    # Limb precision survives.
    units = {r['family_id']: r['unit'] for r in fams}
    bad_limb = []
    for r in qs:
        if not r['canonical_family_ids']:
            continue
        fu = {units.get(f) for f in r['canonical_family_ids']}
        if fu and fu != set(r['family_unit']) - {None} and r['family_unit']:
            bad_limb.append(r['question_id'])
    check('R-LIMB-CARRY', not bad_limb,
          '%d question(s) lost their family unit: %s' % (len(bad_limb), bad_limb[:8]))
    # A WHOLE_VS_LIMB_RELATION join may never be collapsed by the adapter.
    collapsed = []
    for j in canonical['joins']:
        if j['verdict'] != 'WHOLE_VS_LIMB_RELATION':
            continue
        a = set(A.family_sittings(canonical, j['family_a']))
        b = set(A.family_sittings(canonical, j['family_b']))
        if j['family_a'] == j['family_b']:
            collapsed.append(j['join_id'])
    check('R-LIMB-SPLIT', not collapsed,
          'a whole-vs-limb join was collapsed: %s' % collapsed[:8])
    # A conflict explained by such a join must be labelled, never merged.
    wl = [r for r in recon if r['verdict'] == 'LEGITIMATE_WHOLE_VS_LIMB']
    check('R-LIMB-LABEL',
          all('WHOLE_VS_LIMB_RELATION' in (r.get('governing_joins') or []) for r in wl),
          'a whole-vs-limb verdict was recorded without its governing join')

    # ---------------------------------------------------------------- G
    # A currentness risk can never read as ready to study -- unless a human
    # went and RESOLVED it. `currentness_status` is a TRIAGE verdict and says
    # so itself: it means nobody checked, not that the answer is wrong. A
    # governed Phase-2 record is the one thing that can answer it, and the
    # exemption is only granted where that record was actually earned:
    # a safe final state, a dated authority check, an independent review that
    # passed, and a canonical answer to point the candidate at. A record
    # missing any of those grants nothing, so hollowing one out cannot buy a
    # READY. The triage value itself is never rewritten -- Phase 1 is input.
    def _phase2_earned(row):
        p2 = row.get('phase2_resolution') or {}
        return bool(
            p2.get('final_state') in A.PHASE2_SAFE_STATES
            and p2.get('authority_currentness_date')
            and p2.get('review_verdict') in ('PASS', 'PASS_WITH_MINOR_FIX')
            and p2.get('canonical_current_answer'))

    unsafe_ready = [r['family_id'] for r in fams
                    if r['currentness_status'] in A.UNSAFE_CURRENTNESS
                    and r['readiness'] == 'READY_TO_STUDY_NOW'
                    and not _phase2_earned(r)]
    check('R-READY-SAFE', not unsafe_ready,
          '%d family(ies) carry a currentness risk and still read as ready: %s'
          % (len(unsafe_ready), unsafe_ready[:8]))
    check('R-READY-VOCAB',
          all(r['readiness'] in A.READINESS_STATES for r in fams),
          'a readiness state outside the governed vocabulary was emitted')
    mislabelled = [r['family_id'] for r in fams
                   if r['blocked'] != (r['readiness'] not in
                                       ('READY_TO_STUDY_NOW', 'HISTORICAL_ONLY'))]
    check('R-READY-BLOCK', not mislabelled,
          'blocked flag disagrees with readiness on %s' % mislabelled[:8])

    # ---------------------------------------------------------------- H
    # Phase-2 answer debt is visible, not silently dropped.
    queued = set(canonical['queue'])
    projected = {r['family_id'] for r in fams}
    missing = sorted(queued - projected)
    check('R-DEBT-COVER', not missing,
          '%d Phase-2 queue family(ies) never reach the study projection: %s'
          % (len(missing), missing[:8]))
    no_action = [r['family_id'] for r in fams if not r['phase2_action']]
    check('R-DEBT-ACTION', not no_action,
          '%d family(ies) carry no Phase-2 action: %s' % (len(no_action), no_action[:8]))

    # ---------------------------------------------------------------- I
    # The roadmap recurrence really does derive from the adapter.
    mappings = ctx['mappings']
    fresh_fams = A.project_families(modern, canonical, mappings)
    fresh_qs = A.project_questions(modern, canonical, mappings, fresh_fams)
    fresh = A.roadmap_recurrence(A.project_topics(fresh_fams, fresh_qs))
    check('R-ROADMAP-DERIVE', fresh['by_topic'] == rm['by_topic'],
          'the stored roadmap recurrence input is not what the adapter produces')

    for d in spine['domains']:
        stored = d['study_priority']['raw'].get('written_recurrence')
        if stored is None:
            continue
        if stored != rm['by_topic'][d['domain_id']]:
            check('R-ROADMAP-WIRED', False,
                  '%s spine written_recurrence=%s but the adapter says %s -- the '
                  'spine is not reading the adapter (or is hand-edited)'
                  % (d['domain_id'], stored, rm['by_topic'][d['domain_id']]))
            break
    else:
        check('R-ROADMAP-WIRED', True)

    # ---------------------------------------------------------------- J
    # Prerequisite gating is untouched by priority work.
    prereq_ok = all(set(d['prerequisites']) ==
                    set(next(x['prerequisites'] for x in SP.DOMAINS
                             if x['domain_id'] == d['domain_id']))
                    for d in spine['domains'])
    check('R-PREREQ', prereq_ok, 'the spine prerequisite graph no longer matches '
                                 'the registry')

    # ---------------------------------------------------------------- K
    # Study progress is durable user state.
    prog = os.path.join(DOC, 'study_progress.json')
    dirty = subprocess.run(['git', 'diff', '--name-only', '--', prog],
                           cwd=REPO, capture_output=True, text=True).stdout.strip()
    check('R-PROGRESS', not dirty,
          'study_progress.json has uncommitted changes -- a priority build must '
          'never write durable user state')

    # ---------------------------------------------------------------- L
    # Public safety: the historical band is secondary-claimed and may not be
    # published as a dated claim, and this layer is deploy-excluded.
    vercelignore = os.path.join(REPO, '.vercelignore')
    ign = open(vercelignore, encoding='utf-8').read() if os.path.exists(vercelignore) else ''
    check('R-PUBLIC-SCOPE', 'docs' in ign and 'tools' in ign,
          'docs/ and tools/ must stay deploy-excluded; study_qi.json is internal')

    html = ctx['public_html']
    leaked = []
    if html:
        for token in ('QIF-EM-', 'SECONDARY_CLAIMED', 'HISTORICAL_SECONDARY_ARCHIVE',
                      'since 2010', 'CURRENTNESS_', 'phase2_action', 'HOLD_'):
            if token in html:
                leaked.append(token)
    check('R-PUBLIC-LEAK', not leaked,
          'the public roadmap carries internal QI token(s): %s' % leaked)

    # ---------------------------------------------------------------- M / N
    # The canonical QI counts are inputs and this integration may not move them.
    check('R-QI-FAMILIES', canonical['counts']['families'] == len(fams),
          'family count moved: QI says %d, the projection carries %d'
          % (canonical['counts']['families'], len(fams)))
    occ = ctx['occurrence_counts']
    check('R-QI-OCCURRENCES', occ['recurrence_bearing'] == 1584
          and occ['total_records'] == 2282,
          'the QI occurrence counts moved (recurrence_bearing=%s total=%s). This '
          'integration reads the QI layer; it may never rebuild it.'
          % (occ['recurrence_bearing'], occ['total_records']))

    # ---------------------------------------------------------------- O
    # Determinism.
    if ctx.get('run_determinism'):
        build = subprocess.run([sys.executable,
                                os.path.join(REPO, 'tools', 'study', 'build_study_qi.py'),
                                '--check'], cwd=REPO, capture_output=True, text=True)
        check('R-DETERMINISM', build.returncode == 0,
              'build_study_qi.py --check failed: %s'
              % (build.stdout + build.stderr)[:600])

    return list(FAILURES), list(CHECKS)


def main():
    failures, checks = run_checks(load_context())
    passed = sum(1 for _, ok in checks if ok)
    print('study-QI integration gate: %d/%d checks passed' % (passed, len(checks)))
    for rule, ok in checks:
        print('  %s %s' % ('PASS' if ok else 'FAIL', rule))
    if failures:
        print('')
        print('FAILURES')
        for f in failures:
            print('  ' + f)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
