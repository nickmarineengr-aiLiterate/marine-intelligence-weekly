#!/usr/bin/env python3
"""The current-answer library gate. Fails closed.

    python tools/current_answers/validate_current_answers.py

WHAT THIS GATE IS DEFENDING
---------------------------
Four things, in order of how badly they would hurt:

1.  A synthetic question becoming EVIDENCE. MIW's whole recurrence product
    rests on "this was actually set, on this date, and here is the printed
    copy". A present-day canonical question was set by nobody. If one ever
    leaks into the occurrence layer or the examiner layer, every count MIW
    publishes becomes a number partly about itself (R-CA-NO-RECURRENCE,
    R-CA-NO-EXAMINER, R-CA-NO-SITTING).

2.  A library answer reading as a SOLVED PAPER. The archive pages exist to say
    "MIW has not answered these". A link that says "solved" on that page is the
    one sentence those pages cannot ship (R-CA-ARCHIVE-LABEL).

3.  "Verified" spent on an unverified answer. The same failure the Phase-2
    contract exists to prevent, one layer down (R-CA-AUTHORITY, R-CA-REVIEW).

4.  A paid answer going public. The library is the gated Written product, and
    the gate is the middleware MATCHER -- not a header, not a meta tag
    (R-CA-GATED, R-CA-PUBLIC-ROADMAP).
"""

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'tools', 'study'))

import ca_model as M                       # noqa: E402
import study_qi_adapter as A               # noqa: E402

QI_DIR = os.path.join(REPO, 'docs', 'study', 'qi')
SPEC_DIR = os.path.join(REPO, 'meoclass1', 'pastpapers', 'specs')
PHASE2 = os.path.join(REPO, 'tools', 'study', 'qi_phase2_adjudications.json')
PUBLIC_ROADMAP = os.path.join(REPO, 'SQ', 'study-roadmap.html')
MIDDLEWARE = os.path.join(REPO, 'middleware.js')

RESULTS = []


def check(rule, ok, detail=''):
    RESULTS.append((rule, bool(ok), detail))


def _read(path):
    with io.open(path, encoding='utf-8', errors='replace') as f:
        return f.read()


def _json(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def load_bundle():
    """Everything the gate reads, in one dict.

    Separated from the checks for the same reason the Phase-2 gate separates
    them: the mutation suite corrupts a COPY of this bundle in memory and proves
    each rule bites, without ever writing a mutation to disk.
    """
    fams = []
    if os.path.exists(PHASE2):
        fams = _json(PHASE2)['families']
    specs = {}
    for name in sorted(os.listdir(SPEC_DIR)):
        if name.endswith('.json'):
            specs[name[:-5]] = _json(os.path.join(SPEC_DIR, name))
    pages = {}
    if os.path.isdir(M.PAGE_DIR):
        for name in sorted(os.listdir(M.PAGE_DIR)):
            if name.endswith('.html'):
                pages[name[:-5]] = _read(os.path.join(M.PAGE_DIR, name))
    archive_pages = {}
    for base in (os.path.join(REPO, 'meoclass1', 'pastpapers'),
                 os.path.join(REPO, 'solvedQP')):
        for yr in (2021, 2022):
            p = os.path.join(base, 'questions-%d.html' % yr)
            if os.path.exists(p):
                archive_pages[os.path.relpath(p, REPO).replace('\\', '/')] = _read(p)
    # Read as (filename, id) pairs rather than recovered from the entries dict.
    # `load_entries()` is keyed by id, so a duplicate id would silently collapse
    # to one row and R-CA-ID-UNIQUE would be unable to see the thing it exists
    # to catch. It lives in the bundle so the mutation suite can reach it.
    filed = []
    if os.path.isdir(M.SPEC_DIR):
        for name in sorted(os.listdir(M.SPEC_DIR)):
            if name.endswith('.json'):
                filed.append((name, _json(os.path.join(M.SPEC_DIR, name))
                              .get('current_answer_id')))
    # The examiner / oral evidence layer, read here rather than inside the
    # check. It was read inside the check first, which made R-CA-NO-EXAMINER
    # the one rule in this gate the mutation suite could not reach -- it went
    # straight to disk, so a corrupted bundle could not express the failure.
    # A rule that cannot be attacked is a rule nobody has evidence works.
    ex_paths = [os.path.join(REPO, 'meoclass1', 'qb_content_index.json'),
                os.path.join(REPO, 'meoclass1', 'examiner-index.html'),
                os.path.join(REPO, 'SQ', 'examiner-index.html')]
    ex_dir = os.path.join(REPO, 'meoclass1', 'oral-intelligence')
    if os.path.isdir(ex_dir):
        for root, _dirs, files in os.walk(ex_dir):
            ex_paths.extend(os.path.join(root, f) for f in files
                            if f.endswith(('.json', '.html')))
    examiner = {os.path.relpath(p, REPO).replace('\\', '/'): _read(p)
                for p in ex_paths if os.path.exists(p)}
    return {
        'entries': M.load_entries(),
        'filed': filed,
        'examiner': examiner,
        'registry': M.load_registry(),
        'fams': fams,
        'specs': specs,
        'pages': pages,
        'archive_pages': archive_pages,
        'qi_occ': _json(os.path.join(QI_DIR, 'qi_occurrences.json')),
        'qi_fams': _json(os.path.join(QI_DIR, 'qi_families.json')),
        'qi_ents': _json(os.path.join(QI_DIR, 'qi_source_entities.json')),
        'public_roadmap': (_read(PUBLIC_ROADMAP)
                           if os.path.exists(PUBLIC_ROADMAP) else None),
        'middleware': _read(MIDDLEWARE) if os.path.exists(MIDDLEWARE) else None,
        'real_qids': {q['question_id'] for s in specs.values()
                      for q in s.get('questions', []) if q.get('question_id')},
    }


# --------------------------------------------------------------------------

def run_checks(B):
    entries = B['entries']
    ids = list(entries)

    # ------------------------------------------------------------------ A / B
    # Identity. A duplicate id silently makes one answer unreachable; a QP-shaped
    # id makes a synthetic question indistinguishable from a printed one to every
    # consumer in the repo, all of which key on that shape.
    on_disk = [i for _n, i in B['filed']]
    dupes = sorted({i for i in on_disk if on_disk.count(i) > 1})
    check('R-CA-ID-UNIQUE', not dupes,
          'duplicate current_answer_id(s) on disk. One answer is unreachable '
          'and which one depends on filename sort order: %s' % dupes)

    bad_id = [i for i in ids if not M.is_ca_id(i)]
    check('R-CA-ID-GRAMMAR', not bad_id,
          'current_answer_id(s) outside the CA-EM-nnnn namespace: %s' % bad_id)

    # The same prohibition over the WHOLE library id space, not just the
    # entries. R-CA-ID-GRAMMAR already refuses a QP-shaped id inside an entry,
    # so scanning entries alone would make this rule unreachable -- a rule that
    # can never fail reads as protection and provides none. What it adds is the
    # two id surfaces the grammar rule does not see: the filenames on disk and
    # the rendered page names, either of which could carry a QP shape while
    # every entry stayed well-formed.
    qp_shaped = sorted({i for i in ids if M.is_qp_id(i)}
                       | {n[:-5] for n, _i in B['filed'] if M.is_qp_id(n[:-5])}
                       | {p for p in B['pages'] if M.is_qp_id(p)})
    check('R-CA-ID-NOT-QP', not qp_shaped,
          'current-answer id(s), file name(s) or page name(s) shaped like a '
          'past-paper question. Every consumer in the repo -- the recurrence '
          'model, the examiner layer, the year sheets -- keys on that shape, so '
          'a current answer must never be able to pass as a sitting: %s'
          % qp_shaped)

    # Filename is the id. A file named otherwise is findable by one route only.
    misfiled = [n for n, i in B['filed'] if i != n[:-5]]
    check('R-CA-FILENAME', not misfiled,
          'entry file(s) whose name is not their id: %s' % misfiled)

    # ------------------------------------------------------------------ schema
    missing, bad_schema, bad_scope, bad_vis, bad_origin = [], [], [], [], []
    for i, e in entries.items():
        for k in M.REQUIRED:
            if not e.get(k):
                missing.append('%s.%s' % (i, k))
        if e.get('schema') != M.SCHEMA:
            bad_schema.append(i)
        if e.get('scope') not in M.SCOPES:
            bad_scope.append(i)
        if e.get('candidate_visibility') not in M.VISIBILITY:
            bad_vis.append(i)
        if e.get('question_origin') not in M.QUESTION_ORIGINS:
            bad_origin.append(i)
    check('R-CA-REQUIRED', not missing,
          'entry field(s) missing or empty: %s' % missing)
    check('R-CA-SCHEMA', not bad_schema, 'wrong schema id: %s' % bad_schema)
    check('R-CA-SCOPE', not bad_scope, 'unrecognised scope: %s' % bad_scope)
    check('R-CA-VISIBILITY', not bad_vis,
          'entry(ies) not declared GATED. Section 39 -- current answers are the '
          'paid Written product: %s' % bad_vis)
    check('R-CA-ORIGIN', not bad_origin,
          'entry(ies) with no governed question_origin. There is deliberately '
          'no origin meaning "printed on a source copy": %s' % bad_origin)

    # A LIMB entry must say which limb of what.
    limb_bad = [i for i, e in entries.items()
                if e.get('scope') == 'LIMB'
                and not ((e.get('limb_of') or {}).get('limb_id')
                         and (e.get('limb_of') or {}).get('limb_label'))]
    check('R-CA-LIMB-DECLARED', not limb_bad,
          'LIMB entry(ies) that do not name the limb they answer: %s' % limb_bad)

    # ------------------------------------------------------------------ C
    # A current answer with no family is an answer to nothing MIW measured.
    # The library is DOWNSTREAM of QI (section 7): it may not invent a subject.
    gov_fams = {f['family_id'] for f in B['qi_fams']['families']}
    no_fam = [i for i, e in entries.items() if not (e.get('family_ids') or [])]
    ghost_fam = ['%s -> %s' % (i, f) for i, e in entries.items()
                 for f in (e.get('family_ids') or []) if f not in gov_fams]
    check('R-CA-FAMILY', not no_fam,
          'entry(ies) linked to no QI family. The library is downstream of QI '
          'and may not invent a subject: %s' % no_fam)
    check('R-CA-FAMILY-REAL', not ghost_fam,
          'entry(ies) naming a family that does not exist: %s' % ghost_fam)

    # ------------------------------------------------------------------ D / E
    ver = {i: e for i, e in entries.items()
           if e.get('review_status') in M.RENDERABLE}
    no_auth = [i for i, e in ver.items() if not (e.get('authority_sources') or [])]
    bad_auth = [i for i, e in ver.items()
                if (e.get('authority_sources') or [])
                and not any(s.get('class') in M.ACCEPTED_AUTHORITY
                            for s in e['authority_sources'])]
    no_date = [i for i, e in ver.items()
               if not e.get('authority_review_date') or not e.get('currentness_as_of')]
    check('R-CA-AUTHORITY', not no_auth,
          'verified entry(ies) with no primary authority: %s' % no_auth)
    check('R-CA-AUTHORITY-CLASS', not bad_auth,
          'verified entry(ies) whose authority is of no accepted class: %s' % bad_auth)
    check('R-CA-AUTHORITY-DATE', not no_date,
          'verified entry(ies) with no review/currentness date. An undated '
          'currency check is not a currency check: %s' % no_date)

    # Section 15: one citation universe, not two. If these two lists ever drift
    # the same source would satisfy one gate and fail the other.
    try:
        import validate_phase2_tranche as V
        same = set(V.ACCEPTED_AUTHORITY) == set(M.ACCEPTED_AUTHORITY)
    except Exception:
        same = False
    check('R-CA-AUTHORITY-VOCAB', same,
          'the current-answer authority vocabulary has drifted from the Phase-2 '
          'one. Two citation universes is exactly what section 15 forbids.')

    no_rev = [i for i, e in ver.items()
              if not (e.get('review_record') or {}).get('reviewer')
              or not (e.get('review_record') or {}).get('verdict')]
    bad_rev = [i for i, e in ver.items()
               if (e.get('review_record') or {}).get('verdict')
               and e['review_record']['verdict'] not in M.PASSING_REVIEW]
    check('R-CA-REVIEW', not no_rev,
          'entry(ies) claiming CURRENT_ANSWER_VERIFIED with no independent '
          'review. Section 16 -- authority alone never verifies: %s' % no_rev)
    check('R-CA-REVIEW-PASS', not bad_rev,
          'verified entry(ies) whose review did not pass: %s' % bad_rev)

    # Versioning is not decoration: it is what lets a current answer legally
    # change when a past-paper answer may not. An entry with no history has no
    # way to record WHY it moved.
    ver_bad = [i for i, e in entries.items()
               if not any(v.get('version') == e.get('answer_version')
                          for v in (e.get('version_history') or []))]
    check('R-CA-VERSION', not ver_bad,
          'entry(ies) whose answer_version has no matching version_history row. '
          'Section 13 -- do not overwrite history invisibly: %s' % ver_bad)

    hist_bad = [('%s v%s' % (i, v.get('version')))
                for i, e in entries.items()
                for v in (e.get('version_history') or [])
                if not (v.get('version') and v.get('date') and v.get('reason'))]
    check('R-CA-VERSION-FIELDS', not hist_bad,
          'version_history row(s) missing version, date or reason: %s' % hist_bad)

    # ------------------------------------------------------------------ F
    # ZERO RECURRENCE CONTRIBUTION. Proved by sweeping the occurrence layer for
    # the id shape, not by asserting it in prose.
    ca_pat = re.compile(r'\bCA-EM-\d{4}\b')
    occ_hits = sorted(set(ca_pat.findall(json.dumps(B['qi_occ'], ensure_ascii=False))))
    fam_hits = sorted(set(ca_pat.findall(json.dumps(B['qi_fams'], ensure_ascii=False))))
    ent_hits = sorted(set(ca_pat.findall(json.dumps(B['qi_ents'], ensure_ascii=False))))
    check('R-CA-NO-RECURRENCE', not (occ_hits or fam_hits or ent_hits),
          'a current-answer id reached the recurrence layer. A synthetic '
          'question is not evidence that anybody was asked it, and a count that '
          'includes one is partly a count of MIW: occurrences=%s families=%s '
          'entities=%s' % (occ_hits, fam_hits, ent_hits))

    # ...and the inverse, which is the failure that would not look like one:
    # a library entry quietly claiming to BE an occurrence.
    occ_shaped = [i for i, e in entries.items()
                  if any(k in e for k in ('occurrence_id', 'evidence_band',
                                          'date_certainty', 'native_id'))]
    check('R-CA-NOT-AN-OCCURRENCE', not occ_shaped,
          'entry(ies) carrying occurrence-layer fields: %s' % occ_shaped)

    # ------------------------------------------------------------------ G
    ex_hits = sorted(p for p, text in B['examiner'].items() if ca_pat.search(text))
    check('R-CA-NO-EXAMINER', not ex_hits,
          'a current-answer id reached the examiner / oral evidence layer. A '
          'synthetic question is not evidence that an examiner asked it: %s'
          % ex_hits)

    # ------------------------------------------------------------------ H
    # HISTORICAL SPECS UNTOUCHED. A past paper may LINK to a current answer --
    # that is the whole point of a successor route -- but it may never be OWNED
    # by one, and its sitting-anchored answer text may never cite one.
    owned = ['%s.%s' % (pid, q.get('question_id'))
             for pid, s in B['specs'].items() for q in s.get('questions', [])
             if any(k in q for k in ('current_answer_id', 'current_answer_owner',
                                     'canonical_current_answer'))]
    check('R-CA-SPEC-NOT-OWNED', not owned,
          'past-paper question(s) carrying current-answer ownership fields. A '
          'sitting-anchored answer is owned by its sitting: %s' % owned)

    in_answer = []
    for pid, s in B['specs'].items():
        for q in s.get('questions', []):
            body = json.dumps([q.get('model_answer'), q.get('study_notes')],
                              ensure_ascii=False)
            if ca_pat.search(body):
                in_answer.append(q.get('question_id'))
    check('R-CA-SPEC-ANSWER-CLEAN', not in_answer,
          'past-paper model answer / study guide text naming a current-answer '
          'id. A February 2024 answer may not cite an August 2026 artefact: %s'
          % in_answer)

    # ------------------------------------------------------------------ I / J / K
    # OWNERSHIP, from the Phase-2 side. Typed, resolvable, and complete.
    untyped, bad_type, ghost, mismatched, unrenderable = [], [], [], [], []
    for r in B['fams']:
        fid = r['family_id']
        raw = [r.get('canonical_current_answer')] + list(
            r.get('family_current_answers') or [])
        for obj in raw:
            if obj is None:
                continue
            t, i = M.resolve_owner(obj)
            if i is None:
                continue
            if t not in M.OWNER_TYPES:
                bad_type.append('%s -> %s' % (fid, t))
                continue
            # A library owner written in the untyped legacy shape would be read
            # as SOLVED_PAPER by the resolver and would then fail to resolve
            # against the spec set -- a confusing failure a long way from its
            # cause. Refuse it at the shape.
            if M.is_ca_id(i) and not (isinstance(obj, dict) and obj.get('owner_type')):
                untyped.append('%s -> %s' % (fid, i))
            if t in M.LIBRARY_OWNER_TYPES:
                if not M.is_ca_id(i):
                    mismatched.append('%s: %s owner_id %s is not a library id'
                                      % (fid, t, i))
                elif i not in entries:
                    ghost.append('%s -> %s' % (fid, i))
                elif entries[i].get('review_status') not in M.RENDERABLE:
                    unrenderable.append('%s -> %s (%s)'
                                        % (fid, i, entries[i].get('review_status')))
            elif t in M.PAPER_OWNER_TYPES:
                if not M.is_qp_id(i):
                    mismatched.append('%s: %s owner_id %s is not a question id'
                                      % (fid, t, i))
                elif i not in B['real_qids']:
                    ghost.append('%s -> %s' % (fid, i))

    check('R-CA-OWNER-TYPED', not untyped,
          'family(ies) naming a library answer without an explicit owner_type. '
          'Section 17 -- ownership is typed, never parsed out of a string: %s'
          % untyped)
    check('R-CA-OWNER-TYPE-KNOWN', not bad_type,
          'unrecognised owner_type: %s' % bad_type)
    check('R-CA-OWNER-SHAPE', not mismatched,
          'owner_type and owner_id disagree about what kind of thing is being '
          'named: %s' % mismatched)
    check('R-CA-OWNER-RESOLVES', not ghost,
          'family(ies) naming an owner that does not exist. Section 42 J and K: '
          '%s' % ghost)
    check('R-CA-OWNER-RENDERABLE', not unrenderable,
          'family(ies) routing a candidate to a library entry that is not '
          'verified and therefore has no page: %s' % unrenderable)

    # ------------------------------------------------------------------ L
    # LIMB SCOPING. Two failures, and they are different.
    dup_limb, no_scope, both = [], [], []
    for r in B['fams']:
        fid = r['family_id']
        limbs = r.get('family_current_answers') or []
        seen = [l.get('limb_id') for l in limbs]
        if len(seen) != len(set(seen)):
            dup_limb.append(fid)
        for l in limbs:
            if not l.get('limb_id') or not l.get('scope'):
                no_scope.append('%s.%s' % (fid, l.get('limb_id')))
        # A family owns itself whole, or limb by limb. Both at once means two
        # answers to "where do I send this candidate", and the two will drift.
        if limbs and r.get('canonical_current_answer'):
            both.append(fid)
    check('R-CA-LIMB-UNIQUE', not dup_limb,
          'family(ies) declaring the same limb twice: %s' % dup_limb)
    check('R-CA-LIMB-SCOPED', not no_scope,
          'limb owner(s) with no limb_id or no scope. An unscoped limb answer '
          'is a whole-question answer wearing a limb label: %s' % no_scope)
    check('R-CA-OWNERSHIP-EXCLUSIVE', not both,
          'family(ies) claiming BOTH a whole-question owner and limb owners: %s'
          % both)

    # A library LIMB entry must be claimed by a limb slot, never by a whole
    # family. This is the rule that stops one verified limb blessing its
    # siblings: a sibling can only be reached through its OWN slot.
    claimed_whole, claimed_limb = {}, {}
    for r in B['fams']:
        t, i = M.resolve_owner(r.get('canonical_current_answer'))
        if t in M.LIBRARY_OWNER_TYPES and i:
            claimed_whole.setdefault(i, []).append(r['family_id'])
        for l in r.get('family_current_answers') or []:
            t, i = M.resolve_owner(l)
            if t in M.LIBRARY_OWNER_TYPES and i:
                claimed_limb.setdefault(i, []).append(
                    '%s.%s' % (r['family_id'], l.get('limb_id')))
    wrong_slot = ['%s is scope=%s but claimed as %s'
                  % (i, entries[i].get('scope'), kind)
                  for kind, d in (('whole-question owner', claimed_whole),
                                  ('limb owner', claimed_limb))
                  for i in d if i in entries
                  and ((kind.startswith('whole') and entries[i].get('scope') != 'WHOLE_QUESTION')
                       or (kind.startswith('limb') and entries[i].get('scope') != 'LIMB'))]
    check('R-CA-LIMB-SLOT', not wrong_slot,
          'a library entry is claimed in the wrong kind of slot, so one limb '
          'answer would answer for a whole question or vice versa: %s'
          % wrong_slot)

    # ------------------------------------------------------------------ M
    # GATING. The gate is the middleware MATCHER. A page one directory outside
    # it is public no matter what its meta tags say.
    matcher_ok = bool(B['middleware'] and '/solvedQP/:path*' in B['middleware'])
    check('R-CA-GATED-MATCHER', matcher_ok,
          'middleware.js no longer matches /solvedQP/:path*, so every current '
          'answer page is now public. Middleware is never invoked off-matcher.')

    off_route = [i for i in B['pages']
                 if not M.page_url(i).startswith('/solvedQP/current/')]
    check('R-CA-GATED-ROUTE', not off_route,
          'current-answer page(s) outside the gated route: %s' % off_route)

    indexable = [i for i, h in B['pages'].items() if 'noindex' not in h.lower()]
    check('R-CA-NOINDEX', not indexable,
          'current-answer page(s) without noindex. Paid content is never '
          'indexable: %s' % indexable)

    # Every VERIFIED entry has a page, and every page has a verified entry.
    no_page = [i for i in ver if i not in B['pages']]
    orphan = [i for i in B['pages'] if i not in ver]
    check('R-CA-PAGE-EXISTS', not no_page,
          'verified entry(ies) with no rendered page: %s' % no_page)
    check('R-CA-PAGE-ORPHAN', not orphan,
          'rendered page(s) with no verified entry behind them. A live URL for '
          'an answer MIW no longer stands behind: %s' % orphan)

    # ------------------------------------------------------------------ page
    # Section 21. The page must say what it is, and must not say what it is not.
    unlabelled = [i for i, h in B['pages'].items()
                  if 'Current framework answer' not in h]
    check('R-CA-PAGE-LABELLED', not unlabelled,
          'current-answer page(s) not identifying themselves as a current '
          'framework answer: %s' % unlabelled)

    # Forbidden claims.
    #
    # Two things this rule got wrong on its first run, and both are worth
    # keeping written down because they are the generic shape of a bad guard.
    #
    # 1. It scanned the WHOLE file, and `read_css()` inlines the shared
    #    stylesheet whose comments discuss "the solved paper page". A guard that
    #    reads its own machinery's source comments as product claims will fail
    #    on every page for ever and be switched off. So the style block is
    #    stripped before scanning.
    # 2. It matched bare phrases like "printed serial", which this page uses in
    #    its own DENIAL -- "it carries no examination date, no printed serial
    #    and no printed mark". A substring cannot tell a claim from its
    #    negation, and the negation is the sentence the page exists to say.
    #
    # What is matched instead is the exact markup and wording the PAST-PAPER
    # renderer emits when it makes the claim. Those strings have one meaning.
    # `data-qid` / `data-paper` are how every other surface recognises a
    # past-paper card, so their presence here would not be cosmetic.
    FAKE = ('Open the solved answer', 'Open the solved paper',
            'Solved paper available', 'data-paper=', 'data-qid=',
            'class="q-num"', 'class="q-meta"', 'Exam sitting:')
    faking = ['%s: %s' % (i, c) for i, h in B['pages'].items()
              for c in FAKE if c in re.sub(r'(?s)<style>.*?</style>', '', h)]
    check('R-CA-NO-FAKE-SITTING', not faking,
          'current-answer page(s) making a past-paper claim: %s' % faking)

    # ...and it must be in the BODY, where a reader is. The first version of
    # this rule scanned the whole file and was therefore satisfied by the
    # `<meta name="description">` alone -- a page could drop the sentence out
    # of its visible content and still pass, on the strength of a tag no
    # candidate will ever see. The mutation suite found that, which is what a
    # mutation suite is for.
    disclaim = [i for i, h in B['pages'].items()
                if 'not a past-paper question' not in h.split('<body', 1)[-1].lower()]
    check('R-CA-PAGE-DISCLAIMS', not disclaim,
          'current-answer page(s) not stating plainly that they are not a past '
          'paper. On a page that looks exactly like a solved answer, that '
          'sentence is the entire difference: %s' % disclaim)

    sitting_keys = ['%s.%s' % (i, k) for i, e in entries.items()
                    for k in M.FORBIDDEN_SITTING_KEYS if k in e]
    check('R-CA-NO-SITTING', not sitting_keys,
          'entry field(s) that would make a current answer look like a sitting. '
          'A field cannot be "mostly absent" -- something will read it: %s'
          % sitting_keys)

    depth_bad = [i for i, e in entries.items()
                 if (e.get('recommended_exam_depth') or {}).get('marks_band')
                 and (e['recommended_exam_depth'].get('basis')
                      not in M.DEPTH_BASIS)]
    check('R-CA-MARKS-BASIS', not depth_bad,
          'entry(ies) carrying a marks band without declaring it a '
          'recommendation. Section 22 -- recommended depth is not a printed '
          'mark: %s' % depth_bad)

    # ------------------------------------------------------------------ N
    # The archive may point at a current answer. It may never call it solved.
    bad_arch = []
    for path, raw in B['archive_pages'].items():
        # Same lesson as R-CA-NO-FAKE-SITTING: the shared stylesheet is inlined
        # and its comments talk about "the solved paper page". Strip it, or the
        # guard reads its own machinery as a product claim.
        html = re.sub(r'(?s)<style>.*?</style>', '', raw)
        for m in ca_pat.finditer(html):
            window = html[max(0, m.start() - 400):m.end() + 400]
            if re.search(r'[Ss]olved (answer|paper)', window):
                bad_arch.append('%s near %s' % (path, m.group(0)))
        if 'MIW has not solved these papers' not in html:
            bad_arch.append('%s lost its own not-solved statement' % path)
    check('R-CA-ARCHIVE-LABEL', not bad_arch,
          'a wording-archive page labels a current answer as solved, or dropped '
          'its not-solved statement. These pages exist to say MIW has NOT '
          'answered these questions: %s' % bad_arch)

    # ------------------------------------------------------------------ P
    # The public roadmap is unchanged by this layer. Full answers are gated and
    # the public surface never learns a library id.
    pub = B['public_roadmap']
    pub_hits = sorted(set(ca_pat.findall(pub))) if pub else []
    check('R-CA-PUBLIC-ROADMAP', not pub_hits,
          'the PUBLIC study roadmap names a current-answer id. Section 39 and '
          '46 -- the public surface is unchanged by this layer: %s' % pub_hits)

    # And the answer PROSE never leaves the gated route. Sampled on the longest
    # paragraph of each answer, which is the one worth stealing.
    leaked = []
    for i, e in entries.items():
        blocks = (e.get('answer') or {}).get('blocks') or []
        ps = sorted((b['p'] for b in blocks if isinstance(b, dict) and b.get('p')),
                    key=len, reverse=True)
        if not ps:
            continue
        probe = re.sub(r'<[^>]+>', '', ps[0])[:120].strip()
        if pub and probe and probe in pub:
            leaked.append(i)
    check('R-CA-NO-PUBLIC-ANSWER', not leaked,
          'current-answer prose found on a public surface: %s' % leaked)

    # ------------------------------------------------------------------ O
    # READINESS DERIVES FROM THE OWNER. The registry is generated, so a stale
    # one means a page was published from an input nobody rebuilt against.
    reg = B['registry']
    check('R-CA-REGISTRY', reg is not None and reg.get('schema') == M.REGISTRY_SCHEMA,
          'the current-answer registry is missing or has the wrong schema.')
    if reg:
        reg_ids = {r['current_answer_id'] for r in reg['entries']}
        check('R-CA-REGISTRY-FRESH', reg_ids == set(ids),
              'the registry disagrees with the entries on disk: registry=%s '
              'disk=%s' % (sorted(reg_ids - set(ids)), sorted(set(ids) - reg_ids)))
        stale_status = ['%s: registry says %s, entry says %s'
                        % (r['current_answer_id'], r['review_status'],
                           entries[r['current_answer_id']].get('review_status'))
                        for r in reg['entries']
                        if r['current_answer_id'] in entries
                        and r['review_status'] != entries[r['current_answer_id']]
                        .get('review_status')]
        check('R-CA-REGISTRY-STATUS', not stale_status,
              'the registry carries a review status the entry does not: %s'
              % stale_status)

    # The adapter must actually grant readiness through a library owner. This is
    # the end-to-end assertion: if the adapter cannot see library ownership, a
    # resolved family silently reads NEW_ANSWER_REQUIRED and every page above is
    # decoration.
    lib_fams = [r for r in B['fams']
                if any(t in M.LIBRARY_OWNER_TYPES for t, _ in M.owner_ids(r))]
    not_granted = [r['family_id'] for r in lib_fams
                   if r.get('final_state') in A.PHASE2_SAFE_STATES
                   and r.get('readiness_after') != 'READY_TO_STUDY_NOW']
    check('R-CA-READINESS-FLOWS', not not_granted,
          'family(ies) resolved through a library answer that did not reach '
          'READY_TO_STUDY_NOW: %s' % not_granted)


def main():
    B = load_bundle()
    run_checks(B)
    fails = [r for r in RESULTS if not r[1]]
    for rule, ok, detail in RESULTS:
        print('[%s] %s' % ('PASS' if ok else 'FAIL', rule))
        if not ok:
            print('       %s' % detail)
    print('\n%d/%d invariants pass over %d entry/entries.'
          % (len(RESULTS) - len(fails), len(RESULTS), len(B['entries'])))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
