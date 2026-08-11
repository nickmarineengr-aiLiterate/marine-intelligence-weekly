"""MIW True Source corpus -- consumer adapter.

READ-ONLY. This module consumes the private True Source corpus
(nickmarineengr-aiLiterate/RulesApp-Local-Input). It never writes to it, never
copies it into this repository, and never becomes a second regulation source.

Why this file exists
--------------------
`MIW_TRUE_SOURCE_CONTRACT.md` promised exactly one coupling point between the
Written product and the corpus -- `reference_href()` in `build_paper.py`. That
promise holds for *routing*. It says nothing about *reading*, and reading turned
out to need real care, because the three ready corpora are asymmetric in three
independent dimensions that no single code path can express:

    corpus            resolver-addressable   text-bearing   quotation operative
    MARPOL Annex VI   YES (320 entries)      NO             NO  (no derivative)
    FSS Code          NO                     YES            YES (reservation R1)
    LSA Code          NO                     YES            YES

The single most important rule encoded here:

    THE RIGHT TO QUOTE AND THE EXISTENCE OF TEXT TO QUOTE ARE DIFFERENT FIELDS.

`FD-RIGHTS-1` clears MARPOL Annex VI *in principle* while recording
`operativeToday: false`, because the canonical layer is
`exportPolicy: facts-and-pointers-only` and carries no provision wording at all.
A consumer that collapses those two questions into one boolean will try to render
wording that exists nowhere outside a licensed PDF. So `rights_cleared`,
`text_available` and `text_adequate` are three separate fields on every result and
are only combined at the very end, in `quotable`.

The clearance state is READ, never hard-coded -- FD-RIGHTS-1 is revocable by a
later Founder decision and revocation must take effect on every consumer surface
immediately.

Governance inherited by consuming (handover section 5): frozen corpus objects are
read-only; an error found in the corpus is REPORTED, never repaired here.
"""

import json
import os
import re

# ---------------------------------------------------------------------------
# Locating the corpus
# ---------------------------------------------------------------------------

# The corpus is a SEPARATE PRIVATE repository. It is deliberately not vendored
# into MIW and is not present on a deployment host, so every entry point below
# degrades to CORPUS_UNAVAILABLE rather than raising. A missing corpus must never
# fail a paper build -- that is contract section 8, and it is why nothing in the
# build path calls this module without checking `available()` first.
ENV_ROOT = 'MIW_TRUE_SOURCE_ROOT'
DEFAULT_ROOTS = (r'F:\RulesApp-Local-Input',)

RESOLVED = 'RESOLVED'
NOT_FOUND = 'NOT_FOUND'
CORPUS_UNAVAILABLE = 'CORPUS_UNAVAILABLE'
UNSUPPORTED_INSTRUMENT = 'UNSUPPORTED_INSTRUMENT'

# A provision whose `text` is a structural label rather than regulatory wording
# must never be rendered as if it were the regulation. Measured in the frozen FSS
# BUILD-2 derivative: 22 of 386 texts are labels such as 'Section',
# 'test switches', 'sea inlet to pump'. LSA has none -- its shortest of 292 is 65
# characters of full sentence. The threshold is deliberately crude and is a
# SAFETY GATE, not a quality score: below it we decline to quote and say why.
MIN_QUOTABLE_CHARS = 40

# A fourth question, discovered by reading the derivatives themselves rather than
# the documents describing them: IS THE STORED TEXT ACTUALLY THE PROVISION'S
# WORDING? For the two text-bearing corpora the answer differs, and the evidence
# is inside each artifact:
#
#   LSA  every provision carries textSource 'official-base-ocr(MSC.48(66))
#        page-verified' (or the equivalent amendment resolution) -- transcribed
#        official wording, page-verified. VERBATIM.
#
#   FSS  the derivative's own embedded disclaimer states the wording is a
#        'verified summary, NOT the official text', marked 'INTERNAL USE ONLY'
#        and 'never for redistribution'. Identical in BUILD-1 and BUILD-2, so it
#        is the build's declared nature and not a stray string. SUMMARY.
#
# FD-RIGHTS-1 clears MIW's constructed provision TEXT for quotation. A Founder
# decision can reclassify MIW's own record; it cannot convert a summary into
# provision wording, and quoting a summary as the regulation is precisely what
# MIW_FOUNDER_AIM.md forbids. FSS is therefore first-class VERIFICATION EVIDENCE
# (requirement statements, page-verified numerics, amendment attribution) and is
# NOT a verbatim-quotation source. Recorded as a correction request to the
# producer team; not routed around here.
VERBATIM = 'verbatim-provision-text'
SUMMARY = 'verified-requirement-summary'
NONE_HELD = 'no-text-object'

TEXT_NATURE = {
    'LSA': VERBATIM,
    'FSS': SUMMARY,
    'MARPOL-VI': NONE_HELD,
}


def corpus_root():
    """Return the corpus checkout path, or None if it is not on this machine."""
    env = os.environ.get(ENV_ROOT)
    if env:
        return env if os.path.isdir(env) else None
    for c in DEFAULT_ROOTS:
        if os.path.isdir(c):
            return c
    return None


def available():
    return corpus_root() is not None


def _load(rel):
    root = corpus_root()
    if root is None:
        return None
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Rights -- read from the register, never assumed
# ---------------------------------------------------------------------------

RIGHTS_REL = os.path.join('true-source', 'source-rights-register.json')

# QP-side instrument tokens -> the instrumentId used in the rights register.
INSTRUMENT_IDS = {
    'LSA': 'TS-LSA',
    'FSS': 'TS-FSS',
    'MARPOL-VI': 'TS-MARPOL-VI',
}


def rights_state(instrument):
    """Current FD-RIGHTS-1 state for one instrument, read live from the register.

    Returns a dict with `cleared` (the decision covers this corpus and is ACTIVE)
    and `operative_today` (a text object actually exists for the clearance to
    apply to). Those are separate because the register itself separates them.
    """
    out = {'decision': None, 'status': None, 'cleared': False,
           'operative_today': False, 'reservations': [], 'note': None}
    reg = _load(RIGHTS_REL)
    if reg is None:
        out['note'] = 'rights register unreadable -- corpus unavailable'
        return out
    want = INSTRUMENT_IDS.get(instrument)
    for d in reg.get('founderDecisions') or []:
        if d.get('decisionId') != 'FD-RIGHTS-1':
            continue
        out['decision'] = 'FD-RIGHTS-1'
        out['status'] = d.get('status')
        out['reservations'] = [r.get('reservationId') for r in d.get('reservations') or []
                               if r.get('appliesTo') in (want, 'all three corpora')]
        for c in d.get('corporaCleared') or []:
            if c.get('instrumentId') != want:
                continue
            # A revoked or superseded decision must stop clearing immediately.
            out['cleared'] = (d.get('status') == 'ACTIVE')
            out['operative_today'] = bool(c.get('operativeToday'))
            out['note'] = c.get('operativeNote')
    return out


# ---------------------------------------------------------------------------
# Reference identity
# ---------------------------------------------------------------------------

# LSA carries its own stable, MIW-shaped provisionId (LSA-1.1.1) and the handover
# says to use it as-is. FSS carries NO single identity: numbering restarts inside
# every chapter, so `2.1` exists in 16 of the 17 chapters. Chapter is therefore
# part of FSS identity and an FSS reference without it is a defect, not a
# shorthand. `FSSCode-<chapter>-<number>` encodes exactly the (chapter, number)
# pair the corpus declares -- it introduces no new corpus vocabulary and is used
# only as the QP-side address.
LSA_RE = re.compile(r'^LSA-(\d+(?:\.\d+)*)$')
FSS_RE = re.compile(r'^FSSCode-(\d+)-(\d+(?:\.\d+)*)$')
MARPOL_VI_RE = re.compile(r'^MARPOL-VI-')

# `MEPC32876-<chapter>-<seq>` is the source/consolidation vocabulary. The corpus
# identityPolicy admits it as ALIAS INPUT and forbids it as a canonical target,
# so it is accepted here and normalised away by `_resolve_marpol`. This is the
# whole answer to the "MARPOL identity split": there is one canonical family and
# one alias family, not two competing identities.
MEPC_ALIAS_RE = re.compile(r'^MEPC32876-')


def instrument_of(object_id):
    if LSA_RE.match(object_id):
        return 'LSA'
    if FSS_RE.match(object_id):
        return 'FSS'
    if MARPOL_VI_RE.match(object_id) or MEPC_ALIAS_RE.match(object_id):
        return 'MARPOL-VI'
    return None


# ---------------------------------------------------------------------------
# Per-corpus readers
# ---------------------------------------------------------------------------

LSA_REL = os.path.join('true-source', '03-imo-instruments', 'LSA-Code',
                       'consolidated', 'MIW_LSA_CODE_CONSOLIDATED_2026.json')
FSS_REL = os.path.join('true-source', '03-imo-instruments', 'FSS-Code', 'consolidated',
                       'MIW-FSS-2026.08.08-BUILD-2', 'MIW_FSS_CODE_CONSOLIDATED_2026.json')
RESOLVER_REL = os.path.join('true-source', '12-search-index', 'QP_REFERENCE_RESOLVER.json')


def _lsa_index():
    """Flatten LSA to ordered provisions per chapter, preserving document order.

    Order matters: previous/next navigation is a condition of the FD-RIGHTS-1
    permitted form, not a nicety.
    """
    d = _load(LSA_REL)
    if d is None:
        return None, None
    idx, order = {}, []
    for ch in d.get('chapters') or []:
        for p in ch.get('provisions') or []:
            if p.get('kind') != 'provision':
                continue
            pid = p.get('provisionId')
            if not pid:
                continue
            idx[pid] = (ch, p)
            order.append(pid)
    return d, (idx, order)


def _fss_index():
    d = _load(FSS_REL)
    if d is None:
        return None, None
    idx, order = {}, []

    def walk(node, ch):
        # Index headings as well as provisions. A heading is a CONTAINER node --
        # addressable and legitimate to cite structurally, but never quotable as
        # an obligation (handover section 7: "a container record is not a
        # provision -- cite the paragraph objects beneath it"). Indexing only
        # provisions made real container ids look like typos, which is exactly
        # the silent failure this adapter exists to prevent.
        if node.get('number'):
            key = (str(ch.get('label')), str(node['number']))
            # First occurrence wins; the corpus does not repeat (chapter, number).
            if key not in idx:
                idx[key] = (ch, node)
                order.append(key)
        for c in node.get('children') or []:
            walk(c, ch)

    for ch in d.get('chapters') or []:
        for n in ch.get('nodes') or []:
            walk(n, ch)
    return d, (idx, order)


def _neighbours(order, key):
    try:
        i = order.index(key)
    except ValueError:
        return None, None
    return (order[i - 1] if i > 0 else None,
            order[i + 1] if i + 1 < len(order) else None)


# ---------------------------------------------------------------------------
# The public entry point
# ---------------------------------------------------------------------------

def resolve(object_id):
    """Resolve one QP object id to a candidate-safe corpus reference.

    Returns a dict. It NEVER raises for an unknown id and NEVER invents content:
    an id with no corpus object comes back `NOT_FOUND`, which is the honest state
    the Reference Shelf already knows how to render.
    """
    r = {
        'object_id': object_id,
        'instrument': instrument_of(object_id),
        'resolution': None,
        # Three separate questions. Do not collapse them.
        'rights_cleared': False,
        'text_available': False,
        'text_adequate': False,
        'quotable': False,
        'text': None,
        'heading': None,
        'chapter': None,
        'chapter_title': None,
        'previous': None,
        'next': None,
        'citation': None,
        'source_pages': [],
        'build_id': None,
        'non_official_notice': None,
        'reservations': [],
        'structural_role': None,
        'text_nature': TEXT_NATURE.get(instrument_of(object_id)),
        'text_is_verbatim': False,
        'why_not_quotable': None,
    }

    if r['instrument'] is None:
        r['resolution'] = UNSUPPORTED_INSTRUMENT
        r['why_not_quotable'] = ('not one of the three ready corpora '
                                 '(LSA, FSS, MARPOL Annex VI)')
        return r

    if not available():
        r['resolution'] = CORPUS_UNAVAILABLE
        r['why_not_quotable'] = 'True Source corpus not present on this machine'
        return r

    rights = rights_state(r['instrument'])
    r['rights_cleared'] = rights['cleared']
    r['reservations'] = rights['reservations']

    if r['instrument'] == 'LSA':
        _resolve_lsa(object_id, r)
    elif r['instrument'] == 'FSS':
        _resolve_fss(object_id, r)
    else:
        _resolve_marpol(object_id, r, rights)

    r['text_is_verbatim'] = (r['text_nature'] == VERBATIM)

    # Quotability is decided LAST, from every field plus the register's operative
    # flag. Any one of them being false is a hard stop. Ordered most-fundamental
    # first so the reported reason is the real one.
    if r['resolution'] == RESOLVED:
        if not r['rights_cleared']:
            r['why_not_quotable'] = 'FD-RIGHTS-1 does not currently clear this corpus'
        elif not rights['operative_today']:
            r['why_not_quotable'] = rights.get('note') or 'clearance not operative today'
        elif not r['text_available']:
            # A per-corpus reader may already have given a more specific reason
            # (container node, not citation-verified). Do not flatten it.
            r['why_not_quotable'] = (r['why_not_quotable']
                                     or 'no provision text object exists for this reference')
        elif not r['text_is_verbatim']:
            r['why_not_quotable'] = (
                'corpus text for this instrument is a %s, not verbatim provision '
                'wording -- usable as verification evidence, not as a quotation'
                % r['text_nature'])
        elif not r['text_adequate']:
            r['why_not_quotable'] = ('corpus text is a structural label, not provision '
                                     'wording -- refusing to present it as the regulation')
        else:
            r['quotable'] = True
    return r


def _finish_text(r, text):
    r['text_available'] = bool(text)
    r['text_adequate'] = bool(text) and len(text.strip()) >= MIN_QUOTABLE_CHARS
    # Text is only carried out of the adapter when it may actually be shown.
    # Deciding that here, rather than at the render site, means no caller can
    # accidentally print a label or an uncleared provision.
    r['text'] = text


def _resolve_lsa(object_id, r):
    doc, pair = _lsa_index()
    if doc is None:
        r['resolution'] = CORPUS_UNAVAILABLE
        return
    idx, order = pair
    if object_id not in idx:
        r['resolution'] = NOT_FOUND
        return
    ch, p = idx[object_id]
    r['resolution'] = RESOLVED
    r['chapter'] = ch.get('chapter')
    r['chapter_title'] = ch.get('title')
    r['heading'] = p.get('heading')
    r['source_pages'] = p.get('sourcePages') or []
    r['non_official_notice'] = doc.get('disclaimer')
    r['build_id'] = (doc.get('build') or {}).get('buildId') or 'MIW-LSA-2026.08.04-BUILD-20'
    prev, nxt = _neighbours(order, object_id)
    r['previous'], r['next'] = prev, nxt
    r['citation'] = 'LSA Code chapter %s, paragraph %s' % (ch.get('chapter'), p.get('number'))
    # Only citation-verified provisions from a frozen corpus may be quoted.
    if p.get('textStatus') == 'citation-verified':
        _finish_text(r, p.get('text'))
    else:
        _finish_text(r, None)
        r['why_not_quotable'] = 'provision is not citation-verified'


def _resolve_fss(object_id, r):
    m = FSS_RE.match(object_id)
    doc, pair = _fss_index()
    if doc is None:
        r['resolution'] = CORPUS_UNAVAILABLE
        return
    idx, order = pair
    key = (m.group(1), m.group(2))
    if key not in idx:
        r['resolution'] = NOT_FOUND
        return
    ch, n = idx[key]
    r['resolution'] = RESOLVED
    r['chapter'] = ch.get('label')
    r['chapter_title'] = ch.get('title')
    r['heading'] = n.get('heading') or None
    r['non_official_notice'] = doc.get('disclaimer')
    r['build_id'] = doc.get('buildId')
    prev, nxt = _neighbours(order, key)
    r['previous'] = 'FSSCode-%s-%s' % prev if prev else None
    r['next'] = 'FSSCode-%s-%s' % nxt if nxt else None
    r['citation'] = 'FSS Code chapter %s, paragraph %s' % (ch.get('label'), n.get('number'))
    r['structural_role'] = n.get('kind')
    if n.get('kind') == 'provision':
        _finish_text(r, n.get('text'))
    else:
        _finish_text(r, None)
        r['why_not_quotable'] = ('container node; cite the paragraph objects '
                                 'beneath it')


def _resolve_marpol(object_id, r, rights):
    """MARPOL Annex VI resolves to identity and provenance -- never to wording.

    This is not a gap to work around. `finalDerivativeBuildId` is null, the
    canonical layer is facts-and-pointers-only, and the only wording that exists
    anywhere is inside a licensed PDF that may never reach a consumer surface.
    The correct behaviour is to resolve, cite, and state plainly that text is
    pending.
    """
    res = _load(RESOLVER_REL)
    if res is None:
        r['resolution'] = CORPUS_UNAVAILABLE
        return
    for e in res.get('entries') or []:
        if e.get('canonicalId') == object_id:
            r['resolution'] = RESOLVED
            r['citation'] = e.get('unit')
            r['chapter_title'] = e.get('unit')
            _finish_text(r, None)  # by design: no text object exists
            return
        if object_id in (e.get('aliases') or []):
            # Aliases resolve IN to the canonical id, never out (identityPolicy).
            r['resolution'] = RESOLVED
            r['object_id'] = e.get('canonicalId')
            r['citation'] = e.get('unit')
            _finish_text(r, None)
            return
    r['resolution'] = NOT_FOUND


# ---------------------------------------------------------------------------
# Bulk access is refused, structurally
# ---------------------------------------------------------------------------

def resolve_chapter(*_a, **_k):
    """Deliberately unimplemented.

    FD-RIGHTS-1 prohibits rendering a whole chapter, appendix or instrument in a
    single view and prohibits any surface from which the corpus text can be
    reassembled wholesale. The safest way to honour that is to give the consumer
    no chapter-level text call to reach for in the first place.
    """
    raise NotImplementedError(
        'Chapter-level text retrieval is prohibited by FD-RIGHTS-1 '
        '(one provision at a time, in chapter context). Use resolve().')
