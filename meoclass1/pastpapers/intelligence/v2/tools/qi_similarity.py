# -*- coding: utf-8 -*-
"""The single QI-v2 similarity classifier.

Phase 2 carried this logic three times — in the sweep tool, in the negative
controls, and in prose. The copies drifted, and the sweep tool held a
short-stem floor that the classifier itself did not. Everything now imports
from here.

What Phase 3A changes
---------------------
Phase 2 measured lexical containment and nothing else, and its stop-list
deleted `give`, `state`, `explain` and `list` before the comparison. Two
questions that share their nouns but ask for different work therefore scored
as the same question. `Describe the Chief Engineer's actions` and
`Criticise the Port State Control officer's actions` are not the same
question, and a classifier that cannot say so must not be pointed at hundreds
of historical stems.

A stem is now read as five features, not one bag of words:

    demand      what the examiner wants done      (DESCRIBE / CRITICISE / ...)
    actor       who the candidate is asked to be  (CHIEF_ENGINEER / PSC_OFFICER)
    polarity    which pole of a condition         (lay-up vs reactivation)
    numbers     load-bearing cardinals            (FIVE causes vs THREE causes)
    lexis       the remaining subject matter      (containment, as before)

Lexical containment still proposes. Demand, actor, polarity and numbers can
only ever *demote*. Nothing here promotes a pair, and nothing here publishes:
adjudication remains human.

Mutation testing
----------------
`Options` exists so the adversarial suite can switch a feature off and prove
that a control fails without it. A guard that no test depends on is not a
guard. See `tools/adversarial_controls.py --mutate`.
"""
from __future__ import unicode_literals

import re

# ---------------------------------------------------------------------------
# 1. Examiner demand
# ---------------------------------------------------------------------------
# The taxonomy the Founder specified. PROCEDURAL_ACTION and RESPONSIBILITY are
# not verbs — they are what a stem is doing when it asks "what would you do"
# or "who is answerable", and they behave differently from the verb classes.

DEMANDS = (
    'STATE', 'LIST', 'DEFINE', 'DESCRIBE', 'EXPLAIN', 'DISCUSS', 'COMPARE',
    'EVALUATE', 'CRITICISE', 'JUSTIFY', 'OUTLINE', 'CALCULATE', 'SKETCH',
    'PROCEDURAL_ACTION', 'RESPONSIBILITY',
)

# Surface form -> demand. Ordered longest-first at match time so that
# "write short notes" wins over "write".
DEMAND_VERBS = {
    'STATE': ['state', 'give', 'name', 'mention', 'specify', 'enumerate',
              'enlist', 'write short notes', 'short notes'],
    'LIST': ['list', 'list out', 'tabulate', 'itemise', 'itemize'],
    'DEFINE': ['define', 'what is meant by', 'what do you understand by',
               'definition of'],
    'DESCRIBE': ['describe', 'illustrate', 'detail', 'elaborate', 'narrate'],
    'EXPLAIN': ['explain', 'why', 'account for', 'clarify', 'interpret',
                'underline', 'highlight'],
    'DISCUSS': ['discuss', 'comment', 'comment on', 'analyse', 'analyze',
                'examine', 'consider'],
    'COMPARE': ['compare', 'contrast', 'differentiate', 'distinguish',
                'difference between'],
    'EVALUATE': ['evaluate', 'assess', 'appraise'],
    'CRITICISE': ['criticise', 'criticize', 'critically evaluate',
                  'critically examine', 'critique', 'critically appraise'],
    'JUSTIFY': ['justify', 'with justification', 'with proper justification',
                'give reasons', 'with reasons', 'substantiate', 'defend'],
    'OUTLINE': ['outline', 'summarise', 'summarize', 'briefly',
                'sketch out', 'give a brief'],
    'CALCULATE': ['calculate', 'compute', 'determine the value',
                  'estimate', 'derive', 'find the'],
    'SKETCH': ['sketch', 'draw', 'with a neat sketch', 'diagram',
               'draw a diagram'],
    'PROCEDURAL_ACTION': ['what action', 'what actions', 'action you',
                          'actions you', 'steps you', 'steps should',
                          'procedure you', 'how would you proceed',
                          'what would you do', 'what will you do',
                          'measures you', 'how will you', 'how would you'],
    'RESPONSIBILITY': ['who is responsible', 'who should', 'whose duty',
                       'responsibilities of', 'responsibility of',
                       'duties and responsibilities', 'liabilities of',
                       'who carries', 'who is liable', 'accountable'],
}

_DEMAND_LOOKUP = []
for _d, _forms in DEMAND_VERBS.items():
    for _f in _forms:
        _DEMAND_LOOKUP.append((_f, _d))
_DEMAND_LOOKUP.sort(key=lambda t: -len(t[0]))

# "Port State Control" is a regime, not the command verb STATE. Left unmasked
# it gave every PSC question a spurious STATE demand, which is how
# `Describe ... PSC deficiency` and `Criticise ... PSC deficiency` came out
# demand-compatible at 1.00 — the exact confusion Phase 3A exists to remove.
_REGIME_PHRASES = re.compile(
    r'\b(port state control|port state|flag state|coastal state|'
    r'member state|state part(?:y|ies)|states parties|nation state|'
    r'state of the art)\b', re.I)


def _mask_regimes(low):
    return _REGIME_PHRASES.sub(lambda m: '·' * len(m.group(0)), low)

# Compatibility between what two stems ask for. 1.0 = the same demand.
# Anything below EXACT_DEMAND_FLOOR cannot be an exact or near repeat;
# anything below CORE_DEMAND_FLOOR cannot even be the same core ask.
EXACT_DEMAND_FLOOR = 0.90
CORE_DEMAND_FLOOR = 0.55

_DEMAND_GROUP = {
    'STATE': 'ENUMERATIVE', 'LIST': 'ENUMERATIVE', 'OUTLINE': 'ENUMERATIVE',
    'DEFINE': 'ENUMERATIVE',
    'DESCRIBE': 'EXPOSITORY', 'EXPLAIN': 'EXPOSITORY',
    'DISCUSS': 'ANALYTIC', 'COMPARE': 'ANALYTIC', 'JUSTIFY': 'ANALYTIC',
    'EVALUATE': 'CRITICAL', 'CRITICISE': 'CRITICAL',
    'CALCULATE': 'QUANTITATIVE',
    'SKETCH': 'GRAPHIC',
    'PROCEDURAL_ACTION': 'ACTION',
    'RESPONSIBILITY': 'ACTION',
}

# Named pairs, in either direction. Everything else falls to the group rules.
_DEMAND_PAIRS = {
    ('STATE', 'LIST'): 0.95,        # closely compatible, as specified
    ('STATE', 'OUTLINE'): 0.80,
    ('LIST', 'OUTLINE'): 0.80,
    ('OUTLINE', 'DESCRIBE'): 0.75,  # compatible, not necessarily exact
    ('DESCRIBE', 'EXPLAIN'): 0.80,
    ('EXPLAIN', 'DEFINE'): 0.50,    # not automatically exact
    ('DEFINE', 'DESCRIBE'): 0.50,
    ('DISCUSS', 'LIST'): 0.35,      # never exact on object overlap alone
    ('DISCUSS', 'STATE'): 0.35,
    ('DISCUSS', 'EXPLAIN'): 0.65,
    ('DISCUSS', 'COMPARE'): 0.60,
    ('EVALUATE', 'CRITICISE'): 0.90,
    ('JUSTIFY', 'EXPLAIN'): 0.60,
    ('PROCEDURAL_ACTION', 'RESPONSIBILITY'): 0.55,
    ('PROCEDURAL_ACTION', 'DESCRIBE'): 0.60,
    ('PROCEDURAL_ACTION', 'STATE'): 0.60,
}


def demand_compatibility(a, b):
    """Score in [0, 1] for how far two demand sets ask for the same work.

    Demand demotes only on *evidence* of a differing demand. Two stems that
    both leave the demand implicit ("stress the issues you will address") are
    not evidence of anything, and must not be penalised — that would have
    demoted the one true positive in the control set.
    """
    if not a and not b:
        return 1.0           # symmetric silence: no evidence of difference
    if not a or not b:
        return 0.75          # one side unmarked: cautious, not condemning
    best = 0.0
    for x in a:
        for y in b:
            best = max(best, _pair_compat(x, y))
    return best


def _pair_compat(x, y):
    if x == y:
        return 1.0
    named = _DEMAND_PAIRS.get((x, y)) or _DEMAND_PAIRS.get((y, x))
    if named is not None:
        return named
    gx, gy = _DEMAND_GROUP.get(x), _DEMAND_GROUP.get(y)
    if gx == gy:
        return 0.85
    # A critical demand against a non-critical one is a different question.
    if 'CRITICAL' in (gx, gy):
        return 0.25
    if 'QUANTITATIVE' in (gx, gy):
        return 0.10
    if 'GRAPHIC' in (gx, gy):
        return 0.20
    return 0.40


# ---------------------------------------------------------------------------
# 2. Actors
# ---------------------------------------------------------------------------
ACTORS = {
    'CHIEF_ENGINEER': ['chief engineer', 'chief engineer officer', 'c/e'],
    'SECOND_ENGINEER': ['second engineer', '2nd engineer'],
    'MASTER': ['master', 'captain'],
    'PSC_OFFICER': ['port state control officer', 'psc officer',
                    'port state control inspector', 'psco'],
    'PORT_STATE': ['port state control', 'port state'],
    'FLAG_STATE': ['flag state', 'flag administration'],
    'SURVEYOR': ['surveyor', 'surveying authorities', 'surveying authority'],
    'CLASS': ['classification society', 'recognized organization',
              'recognised organization', 'class society'],
    'AUDITOR': ['auditor', 'internal auditor', 'external auditor'],
    'OWNER': ['ship owner', 'shipowner', 'owners', 'ship owners'],
    'CHARTERER': ['charterer', 'charterers'],
    'SUPERINTENDENT': ['superintendent', 'technical superintendent'],
    'DPA': ['designated person ashore', 'dpa'],
    'CREW': ['crew', 'ships personnel', 'engine room personnel', 'ratings'],
}

# Pairs that invert who is acting on whom. A stem asking what the Chief
# Engineer does is not the stem asking what the inspector does to him, however
# much vocabulary they share.
_ACTOR_INVERSIONS = {
    frozenset(['CHIEF_ENGINEER', 'PSC_OFFICER']),
    frozenset(['CHIEF_ENGINEER', 'PORT_STATE']),
    frozenset(['CHIEF_ENGINEER', 'SURVEYOR']),
    frozenset(['CHIEF_ENGINEER', 'AUDITOR']),
    frozenset(['CHIEF_ENGINEER', 'CLASS']),
    frozenset(['MASTER', 'PSC_OFFICER']),
    frozenset(['OWNER', 'CHARTERER']),
    frozenset(['FLAG_STATE', 'PORT_STATE']),
    frozenset(['FLAG_STATE', 'PSC_OFFICER']),
    frozenset(['SURVEYOR', 'AUDITOR']),
}

# Ranks that differ but do not invert the task. The bank itself reuses a
# question across ranks (item 64 Second Engineer / item 182 Chief Engineer),
# so this must weaken a claim of exactness without destroying the ancestry.
_ACTOR_NEAR = {
    frozenset(['CHIEF_ENGINEER', 'SECOND_ENGINEER']),
    frozenset(['CHIEF_ENGINEER', 'SUPERINTENDENT']),
    frozenset(['PSC_OFFICER', 'PORT_STATE']),
    frozenset(['CLASS', 'SURVEYOR']),
}


# A specific actor eclipses the general one it belongs to. Without this,
# "a PSC inspection of the engine room" and "the PSC officer's inspection"
# both carry PORT_STATE, the sets intersect, and an inverted-responsibility
# pair reports as SAME actor.
_ACTOR_ECLIPSE = {
    'PSC_OFFICER': ['PORT_STATE'],
    'CHIEF_ENGINEER': ['CREW'],
    'SECOND_ENGINEER': ['CREW'],
    'SURVEYOR': ['CLASS'],
}


def _eclipse(actors):
    out = set(actors)
    for specific, general in _ACTOR_ECLIPSE.items():
        if specific in out:
            out -= set(general)
    return out


def actor_relation(a, b):
    """One of SAME, UNMARKED, NEAR, DISJOINT, INVERTED."""
    a, b = _eclipse(a), _eclipse(b)
    if not a or not b:
        return 'UNMARKED'
    # A shared actor settles it. Inversion means the task was handed to
    # somebody else, not that the other party is also mentioned: a question
    # about what the Chief Engineer does during a PSC inspection names both,
    # and is not inverted against itself.
    if a & b:
        return 'SAME'
    for x in a:
        for y in b:
            if frozenset([x, y]) in _ACTOR_INVERSIONS:
                return 'INVERTED'
    for x in a:
        for y in b:
            if frozenset([x, y]) in _ACTOR_NEAR:
                return 'NEAR'
    return 'DISJOINT'


# ---------------------------------------------------------------------------
# 3. Polarity — opposite conditions
# ---------------------------------------------------------------------------
# Each entry is (pole_a_terms, pole_b_terms). A stem sitting on one pole and
# its candidate ancestor on the other is asking the opposite question.
_POLARITIES = [
    (['reactivation', 'recommissioning', 'return to service',
      'active service', 'breaking out'], ['lay-up', 'layup', 'laying up',
                                          'preservation', 'prolonged lay']),
    (['entering', 'entry into', 'docking', 'dry docking down'],
     ['undocking', 'leaving', 'flooding up', 'departure from dock']),
    (['before', 'prior to', 'in advance of', 'preparation for'],
     ['after', 'following', 'subsequent to', 'on completion']),
    (['loading'], ['discharging', 'unloading']),
    (['increase', 'increasing', 'maximise', 'maximize', 'raise'],
     ['decrease', 'decreasing', 'minimise', 'minimize', 'reduce']),
    (['ahead'], ['astern']),
    (['rising'], ['falling']),
    (['newbuilding', 'new building', 'delivery'], ['scrapping', 'recycling',
                                                   'demolition']),
]


def polarity(text):
    """Return the set of (index, pole) the text sits on."""
    t = ' %s ' % text.lower()
    found = set()
    for i, (pa, pb) in enumerate(_POLARITIES):
        if any((' %s ' % w) in t or w in t for w in pa):
            found.add((i, 'A'))
        if any((' %s ' % w) in t or w in t for w in pb):
            found.add((i, 'B'))
    return found


def polarity_opposed(a, b):
    """True when the two stems sit on opposite poles of the same condition."""
    for i, p in a:
        if (i, 'A' if p == 'B' else 'B') in b and (i, p) not in b:
            return True
    return False


# ---------------------------------------------------------------------------
# 4. Numbers
# ---------------------------------------------------------------------------
_WORD_NUM = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12,
}
# Numbers that name an instrument are not a quantity the answer must match.
_INSTRUMENT_NUM = re.compile(
    r'(solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|annex|'
    r'chapter|regulation|reg|convention|protocol|amendment|no\.?)\s*[^.;]{0,24}$',
    re.I)


# Mark allocations are MIW's annotation of the paper, not part of the examiner's
# question: the bank prints none, so every marked modern stem would conflict with
# its own ancestor. The first sweep demoted QP2310-Q4 and QP2406-Q3 — both true
# repeats — purely on "(4)" and "(6)".
_MARKS = re.compile(r'\(\s*\d{1,3}\s*\)|\[\s*\d{1,3}\s*\]|\b\d{1,3}\s*marks?\b',
                    re.I)


def numbers(text):
    """Load-bearing cardinals: 'FIVE main problems', not 'SOLAS 74', not '(4)'."""
    t = _MARKS.sub(' ', text.lower())
    out = set()
    for m in re.finditer(r'\b(\d{1,3})\b', t):
        head = t[:m.start()]
        if _INSTRUMENT_NUM.search(head):
            continue
        v = int(m.group(1))
        if 1 <= v <= 20:                 # a quantity of things to produce
            out.add(v)
    for w, v in _WORD_NUM.items():
        if re.search(r'\b%s\b\s+\w' % w, t):
            out.add(v)
    return out


# ---------------------------------------------------------------------------
# 5. Lexis
# ---------------------------------------------------------------------------
# Function words only. Command verbs are NOT stopped here — they are lifted
# into the demand feature first, so they are never silently discarded.
STOP = set("""a an the of to in on for and or with as at by from is are be been
being this that these those it its which what how why when where who whom you
your as per if under over into during shall will would should can could may
might must also our their there each any all""".split())

# Only unambiguous command verbs are lifted out of the lexis. Taking every
# word of every multi-word form would delete ordinary nouns — `responsibilities`,
# `liabilities`, `actions`, `procedure`, `reasons` — and those are subject
# matter. An early Phase-3A build did exactly that and reduced
# "the responsibilities and liabilities of the shipper under the Hamburg Rules"
# to three tokens, which then tripped the short-stem floor.
_DEMAND_TOKENS = set("""state give name mention specify enumerate enlist list
tabulate itemise itemize define describe illustrate elaborate narrate explain
clarify interpret underline highlight discuss comment analyse analyze examine
compare contrast differentiate distinguish evaluate assess appraise criticise
criticize critique justify substantiate outline summarise summarize briefly
calculate compute sketch draw""".split())

SHORT_STEM_MIN_TOKENS = 4     # distinct content tokens


def _singular(t):
    if len(t) > 4 and t.endswith('ies'):
        return t[:-3] + 'y'
    if len(t) > 4 and t.endswith('es') and not t.endswith('ses'):
        return t[:-2]
    if len(t) > 3 and t.endswith('s'):
        return t[:-1]
    return t


def toks(s, drop_demand=True):
    s = (s or '').lower()
    for a, b in [('“', '"'), ('”', '"'),
                 ('‘', "'"), ('’', "'")]:
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    out = []
    for t in s.split():
        if t in STOP or len(t) < 3:
            continue
        if drop_demand and t in _DEMAND_TOKENS:
            continue
        out.append(_singular(t))
    return out


def cont(sub, sup):
    A, B = set(sub), set(sup)
    return len(A & B) / float(len(A)) if A else 0.0


# ---------------------------------------------------------------------------
# 6. The stem representation
# ---------------------------------------------------------------------------
class Stem(object):
    """The deterministic command-demand representation of one stem."""

    __slots__ = ('raw', 'demands', 'actors', 'polarity', 'numbers',
                 'lexis', 'limbs', 'distinct', 'poses_task')

    def __init__(self, text):
        self.raw = text or ''
        low = ' %s ' % re.sub(r'\s+', ' ', self.raw.lower())

        masked = _mask_regimes(low)
        self.demands = set()
        for form, dem in _DEMAND_LOOKUP:
            if re.search(r'(?<![a-z])%s(?![a-z])' % re.escape(form), masked):
                self.demands.add(dem)

        self.actors = set()
        for act, forms in ACTORS.items():
            for f in forms:
                if re.search(r'(?<![a-z])%s(?![a-z])' % re.escape(f), low):
                    self.actors.add(act)
                    break

        # Does this text ask for anything? A sentence that merely asserts the
        # same facts sets no examination task, however well its words match.
        self.poses_task = bool(
            '?' in self.raw
            or self.demands
            or re.search(r'^\s*(?:with reference to|with respect to|in '
                         r'relation to|as (?:a|the) [a-z ]{3,30},)', low)
            or re.search(r'\b(?:what|which|how|why|when|who|whom)\b', masked))

        self.polarity = polarity(self.raw)
        self.numbers = numbers(self.raw)
        self.lexis = toks(self.raw)
        self.distinct = len(set(self.lexis))
        self.limbs = re.findall(r'\(\s*(?:[a-z]|[ivx]{1,4})\s*\)', low)

    @property
    def is_short(self):
        return self.distinct < SHORT_STEM_MIN_TOKENS

    def __repr__(self):
        return 'Stem(demands=%s actors=%s n=%s distinct=%d)' % (
            sorted(self.demands), sorted(self.actors),
            sorted(self.numbers), self.distinct)


# ---------------------------------------------------------------------------
# 7. Classification
# ---------------------------------------------------------------------------
CLASSES = ('EXACT_REPEAT', 'NEAR_VERBATIM', 'SAME_CORE_ASK',
           'TOPIC_ONLY', 'NO_MEANINGFUL_MATCH', 'UNSCOREABLE_SHORT_STEM')

# Containment thresholds, unchanged from Phase 2 so the two runs compare.
T_EXACT = 0.85
T_CORE = 0.65
T_TOPIC = 0.45


class Options(object):
    """Feature switches. Off is only for mutation testing, never for a run."""

    def __init__(self, use_demand=True, use_actor=True, use_short_stem=True,
                 use_numbers=True, use_polarity=True):
        self.use_demand = use_demand
        self.use_actor = use_actor
        self.use_short_stem = use_short_stem
        self.use_numbers = use_numbers
        self.use_polarity = use_polarity


DEFAULT = Options()


class Result(object):
    __slots__ = ('cls', 'fwd', 'rev', 'containment_class', 'demand_compat',
                 'actor_rel', 'polarity_opposed', 'number_conflict',
                 'reasons', 'a', 'b')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

    def __repr__(self):
        return '%s (fwd=%.2f rev=%.2f demand=%.2f actor=%s)' % (
            self.cls, self.fwd, self.rev, self.demand_compat, self.actor_rel)


def _containment_class(fwd, rev):
    """Phase-2 lexical proposal. Proposes only — never the final answer."""
    if fwd >= T_EXACT and rev >= T_EXACT:
        return 'EXACT_OR_NEAR_VERBATIM'
    if rev >= T_EXACT:
        return 'ANCESTOR_ABSORBED_AND_EXTENDED'
    if fwd >= T_EXACT:
        return 'ANCESTOR_NARROWED'
    if max(fwd, rev) >= T_CORE:
        return 'SAME_CORE_ASK_CANDIDATE'
    if max(fwd, rev) >= T_TOPIC:
        return 'TOPIC_ONLY_CANDIDATE'
    return 'NO_MEANINGFUL_MATCH'


_RANK = {'NO_MEANINGFUL_MATCH': 0, 'TOPIC_ONLY': 1, 'SAME_CORE_ASK': 2,
         'NEAR_VERBATIM': 3, 'EXACT_REPEAT': 4}
_UNRANK = {v: k for k, v in _RANK.items()}


def classify(a, b, opts=DEFAULT):
    """Classify a modern stem `a` against a candidate ancestor `b`.

    `a` and `b` may be strings or Stem objects. Returns a Result whose `cls`
    is one of CLASSES. Lexical containment proposes a ceiling; every other
    feature can only lower it.
    """
    A = a if isinstance(a, Stem) else Stem(a)
    B = b if isinstance(b, Stem) else Stem(b)

    fwd, rev = cont(A.lexis, B.lexis), cont(B.lexis, A.lexis)
    cc = _containment_class(fwd, rev)
    reasons = []

    # -- the short-stem gate lives HERE, not in the caller --------------------
    # Phase 2 kept this floor in the sweep loop, so calling the classifier
    # directly with "Deviation" or "War risk" returned an exact repeat.
    if opts.use_short_stem and (A.is_short or B.is_short):
        short = A if A.is_short else B
        return Result(
            cls='UNSCOREABLE_SHORT_STEM', fwd=fwd, rev=rev,
            containment_class=cc, demand_compat=0.0, actor_rel='UNMARKED',
            polarity_opposed=False, number_conflict=False, a=A, b=B,
            reasons=['stem has %d distinct content tokens, floor is %d; '
                     'a label is not a question'
                     % (short.distinct, SHORT_STEM_MIN_TOKENS)])

    # -- lexical ceiling ------------------------------------------------------
    if cc == 'EXACT_OR_NEAR_VERBATIM':
        ceiling = 'EXACT_REPEAT' if fwd >= 0.98 and rev >= 0.98 else 'NEAR_VERBATIM'
    elif cc in ('ANCESTOR_ABSORBED_AND_EXTENDED', 'ANCESTOR_NARROWED'):
        # Containment proposes an ancestor relationship; §22 says it may not
        # decide the class on its own.
        ceiling = 'SAME_CORE_ASK'
        reasons.append('containment proposes %s' % cc)
    elif cc == 'SAME_CORE_ASK_CANDIDATE':
        ceiling = 'SAME_CORE_ASK'
    elif cc == 'TOPIC_ONLY_CANDIDATE':
        ceiling = 'TOPIC_ONLY'
    else:
        ceiling = 'NO_MEANINGFUL_MATCH'

    cap = _RANK[ceiling]

    # -- examiner demand ------------------------------------------------------
    dc = demand_compatibility(A.demands, B.demands) if opts.use_demand else 1.0
    if opts.use_demand:
        if dc < CORE_DEMAND_FLOOR:
            cap = min(cap, _RANK['TOPIC_ONLY'])
            reasons.append('demand incompatible (%.2f): %s vs %s'
                           % (dc, sorted(A.demands) or ['-'],
                              sorted(B.demands) or ['-']))
        elif dc < EXACT_DEMAND_FLOOR:
            cap = min(cap, _RANK['SAME_CORE_ASK'])
            reasons.append('demand differs (%.2f): %s vs %s'
                           % (dc, sorted(A.demands) or ['-'],
                              sorted(B.demands) or ['-']))

    # -- actor ----------------------------------------------------------------
    ar = actor_relation(A.actors, B.actors) if opts.use_actor else 'UNMARKED'
    if opts.use_actor:
        if ar == 'INVERTED':
            cap = min(cap, _RANK['TOPIC_ONLY'])
            reasons.append('actor inverted: %s vs %s'
                           % (sorted(A.actors), sorted(B.actors)))
        elif ar == 'DISJOINT':
            cap = min(cap, _RANK['SAME_CORE_ASK'])
            reasons.append('different actor: %s vs %s'
                           % (sorted(A.actors), sorted(B.actors)))
        elif ar == 'NEAR':
            cap = min(cap, _RANK['NEAR_VERBATIM'])
            reasons.append('adjacent rank: %s vs %s'
                           % (sorted(A.actors), sorted(B.actors)))

    # -- one side sets no task -------------------------------------------------
    if opts.use_demand and A.poses_task != B.poses_task:
        cap = min(cap, _RANK['SAME_CORE_ASK'])
        reasons.append('one side states rather than asks')

    # -- opposite conditions ---------------------------------------------------
    po = polarity_opposed(A.polarity, B.polarity) if opts.use_polarity else False
    if po:
        cap = min(cap, _RANK['TOPIC_ONLY'])
        reasons.append('opposite condition')

    # -- numbers ---------------------------------------------------------------
    nc = bool(A.numbers and B.numbers and A.numbers != B.numbers) \
        if opts.use_numbers else False
    if nc:
        cap = min(cap, _RANK['SAME_CORE_ASK'])
        reasons.append('critical number changed: %s vs %s'
                       % (sorted(A.numbers), sorted(B.numbers)))

    return Result(cls=_UNRANK[cap], fwd=fwd, rev=rev, containment_class=cc,
                  demand_compat=dc, actor_rel=ar, polarity_opposed=po,
                  number_conflict=nc, reasons=reasons, a=A, b=B)


STRONG = ('EXACT_REPEAT', 'NEAR_VERBATIM')
