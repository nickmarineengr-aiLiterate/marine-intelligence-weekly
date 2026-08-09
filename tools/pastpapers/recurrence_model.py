#!/usr/bin/env python3
"""Canonical, CHRONOLOGICAL recurrence model for the Written Questions product.

Why this module exists
----------------------
Three different recurrence signals live in the specs and they mean different
things. Mixing them produces candidate-facing statements that are false.

1. ``recurrence`` (list, e.g. ``['2018/APR', '2025/SEP/Q6', '2026/JAN/Q2']``)
   is the THIRD-PARTY HOST's printed annotation on the source copy. Standing
   policy (CURRENT_STATUS section 20) classes it as DISCOVERY ONLY: the 2026 set
   proved it over-claims and under-claims in both directions. It is never
   canonical and this module ignores it entirely.

2. ``recurrence_class`` (new / topic_recurrence / near_recurrence /
   exact_recurrence) is an AUTHORING field. It records what was true about the
   MIW corpus *at the moment the question was built*, and production order is
   not sitting order. QP2607-Q1 (July) is stored as ``new`` while the same
   examiner task was already set in February, because July was the pilot paper
   and was built first. QP2601-Q3 (January) is stored as ``near_recurrence``
   although January is the EARLIEST sitting in its family, because its answer
   was derived from the July object. Rendering either of those to a candidate
   states the opposite of the truth.

3. ``reused_from`` is a directional pointer in AUTHORING order, for the same
   reason. This module treats it as an UNDIRECTED edge -- "these two questions
   are the same examiner task" -- and recovers direction from the calendar.

   That equivalence is not automatic, and assuming it was produced a false
   family. QP2602-Q3 (formal safety assessment applied to LITHIUM BATTERIES in
   vehicles, containers and ro-ro spaces) was authored from QP2607-Q1 (formal
   safety assessment applied to IRON ORE PELLETS in bulk carriers). What was
   reused is the METHOD, not the question: different cargo, different ship type,
   different hazard, different carriage requirements. Treating that pointer as a
   family edge told a candidate the lithium question had been set five times
   when it had been set four. So ``reuse_kind`` distinguishes the two meanings:

     same_task   (default) the examiner set the same task; a family edge
     shape_only  only the answer's shape or method was reused; NOT a family edge

   Absent means same_task, so the 38 genuine edges need no annotation and the
   claim that needs evidence is the one that has to be written down.

The rule this module enforces
-----------------------------
    Chronology comes from (year, month) and from nothing else.

A family is a connected component over two kinds of undirected edge:
``reused_from`` links, and exact equality of the normalised printed stem. Its
members are then sorted by sitting date. The earliest is the first occurrence;
every later member is a repeat OF it. That holds when 2025 is added, and it
holds when a 2027 paper turns a 2026 singleton into a family -- nothing is
cached in a spec, so the whole model re-derives on every build.

Scope honesty
-------------
The canonical set is only the sittings MIW has actually transcribed. A question
with no relatives is NOT "never asked before"; it is "not repeated inside the
set MIW has built". ``STATUS_SINGLE`` says exactly that and the generated pages
must not upgrade it.
"""
import re
import unicodedata

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')
MONTH_NUM = {m: i + 1 for i, m in enumerate(MONTHS)}

# Candidate-facing status vocabulary. Deliberately four-valued, and deliberately
# NOT the authoring vocabulary. "Topic recurrence" is absent by design: a shared
# subject is not a repeated question, and calling it one is the single most
# misleading thing this page could do.
STATUS_SINGLE = 'single'          # appears once in the canonical set
STATUS_FIRST = 'first'            # earliest sitting of a family that repeats later
STATUS_REPEAT_EXACT = 'repeat_exact'   # later sitting, stem identical to the first
STATUS_REPEAT_NEAR = 'repeat_near'     # later sitting, stem materially reworded

STATUS_LABEL = {
    STATUS_SINGLE: 'Once in this set',
    STATUS_FIRST: 'First in set',
    STATUS_REPEAT_EXACT: 'Repeated &mdash; same wording',
    STATUS_REPEAT_NEAR: 'Repeated &mdash; reworded',
}

# The same four labels as plain text. STATUS_LABEL carries an HTML entity, which
# is right for a rendered badge and wrong for a search token or a JSON field: an
# entity inside a `data-search` attribute is double-escaped, so a candidate
# searching "repeated" would match and a candidate searching the label as it
# appears on screen would not.
STATUS_LABEL_PLAIN = {k: v.replace('&mdash;', '-') for k, v in STATUS_LABEL.items()}

# Coarse filter buckets. 'repeated' covers both repeat flavours so a candidate
# can ask the only question they actually have: "has this come back?"
STATUS_FILTER = {
    STATUS_SINGLE: 'single',
    STATUS_FIRST: 'first',
    STATUS_REPEAT_EXACT: 'repeated',
    STATUS_REPEAT_NEAR: 'repeated',
}


# A printed marks token: a bare integer in parentheses, standing on its own.
#
# The lookbehind is what makes this safe. It requires whitespace or an opening
# bracket immediately before the "(", so a parenthetical that is ATTACHED to an
# identifier is never touched: MEPC.312(74), MEPC.203(62), resolution A.1070(28)
# all keep their numbers, because those digits are part of the instrument's
# name and deleting them would merge two questions about different resolutions.
MARKS_TOKEN = re.compile(r'(?:(?<=\s)|(?<=^)|(?<=\())\((\d{1,2})\)')


def _marks_values(marks, subparts):
    """Every number this question could legitimately print as a marks token."""
    vals = {int(marks)} if marks else set()
    for s in subparts or []:
        m = s.get('marks')
        if m:
            vals.add(int(m))
    return vals


def normalise_stem(text, marks=None, subparts=None):
    """Aggressively normalised printed stem, for equality testing only.

    Case, punctuation and whitespace are discarded because the 2026 set contains
    a pair differing by exactly one inserted colon and one inserted printed
    ``(16)`` (QP2601-Q4 / QP2604-Q4, similarity 0.9946, no semantic difference at
    all). Treating that as a different question would be wrong. This is
    equality testing, never similarity scoring -- similarity ranking is a
    DISCOVERY tool that has already ranked the wrong neighbour twice in this
    corpus, and it is deliberately not used here.

    PRINTED MARKS ARE METADATA, NOT EXAMINER-DEMAND WORDING
    ------------------------------------------------------
    The same examiner task is printed with different marks tokens at different
    sittings, and the marks are already carried structurally in ``total_marks``
    and ``subparts[].marks``. Leaving them in the stem made two identical tasks
    compare unequal and label the later one "Repeated -- reworded", which tells a
    candidate the examiner changed the question when the examiner did not. Three
    real cases in this corpus:

      * QP2403-Q7 prints (6)(4)(6) and QP2412-Q9 prints (6)(5)(5) for the III
        Code question, word for word otherwise;
      * QP2510-Q5 prints a total ``(16)`` after "elaborate following:" where
        QP2403-Q5 prints none, word for word otherwise;
      * QP2403-Q4 prints no marks at all where its relatives print (16).

    So a marks token is stripped, but ONLY when both of these hold:

      1. it is a bare parenthesised integer with whitespace (or nothing) before
         the bracket -- ``MEPC.312(74)`` is attached and survives; and
      2. its value is one this question actually declares, i.e. its own
         ``total_marks`` or one of its subpart marks -- so ``(74)`` would
         survive rule 2 as well, and a number that is part of the examiner's
         demand cannot be removed unless it happens to equal a declared mark.

    Numbers inside the demand -- percentages, years, regulation and section
    numbers, capacities, "Phase 2 (of 20% - 30% reduction)" -- are untouched
    because none of them is a bare parenthesised declared-marks integer.

    Callers that pass no marks get the old behaviour, so the function is still
    usable on a bare string.
    """
    t = unicodedata.normalize('NFKC', text or '')
    keep = _marks_values(marks, subparts)
    if keep:
        t = MARKS_TOKEN.sub(lambda m: ' ' if int(m.group(1)) in keep else m.group(0), t)
    t = t.lower()
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'[^a-z0-9 ]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def load_nodes(specs):
    """Flatten specs into one node per question, keyed by stable question_id."""
    nodes = {}
    for d in specs:
        for q in d['questions']:
            qid = q['question_id']
            nodes[qid] = {
                'question_id': qid,
                'paper_id': d['paper_id'],
                'year': d['year'],
                'month': d['month'],
                'month_num': MONTH_NUM[d['month']],
                'month_year': d['month_year'],
                'q_no': q['q_no'],
                'anchor': q['anchor'],
                'marks': q['total_marks'],
                'text_verbatim': q['text_verbatim'],
                'subparts': q.get('subparts') or [],
                'short_title': q.get('short_title', q['q_no']),
                'primary_category': q.get('primary_category'),
                'subject_tags': q.get('subject_tags') or [],
                'topic_tags': q.get('topic_tags') or [],
                'answers_built': bool(q.get('model_answer')),
                '_reused_from': (q.get('reused_from')
                                 if q.get('reuse_kind', 'same_task') == 'same_task' else None),
                '_reuse_kind': q.get('reuse_kind', 'same_task'),
                '_stem': normalise_stem(q['text_verbatim'], q['total_marks'],
                                        q.get('subparts')),
            }
    return nodes


def _sort_key(node):
    """Sitting order. Question number breaks ties inside one paper."""
    return (node['year'], node['month_num'],
            int(re.sub(r'\D', '', node['q_no']) or 0))


def build_families(nodes):
    """Union-find over reused_from edges and identical normalised stems.

    Returns ``{question_id: relation_dict}``. Both edge kinds are needed:
    reused_from alone misses nothing today but is an authoring artefact, and
    stem equality alone would miss the reworded members of a family. Using both
    means a family survives either signal being absent.
    """
    parent = {qid: qid for qid in nodes}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for qid, n in nodes.items():
        src = n['_reused_from']
        if src and src in nodes:
            union(qid, src)

    by_stem = {}
    for qid, n in nodes.items():
        by_stem.setdefault(n['_stem'], []).append(qid)
    for members in by_stem.values():
        for other in members[1:]:
            union(members[0], other)

    groups = {}
    for qid in nodes:
        groups.setdefault(find(qid), []).append(qid)

    relations = {}
    for root, members in groups.items():
        members = sorted(members, key=lambda q: _sort_key(nodes[q]))
        first = members[0]
        first_stem = nodes[first]['_stem']
        for pos, qid in enumerate(members):
            if len(members) == 1:
                status = STATUS_SINGLE
            elif pos == 0:
                status = STATUS_FIRST
            elif nodes[qid]['_stem'] == first_stem:
                status = STATUS_REPEAT_EXACT
            else:
                status = STATUS_REPEAT_NEAR
            relations[qid] = {
                'family_id': first,          # the earliest sitting names the family
                'family_size': len(members),
                'position': pos,
                'status': status,
                'filter': STATUS_FILTER[status],
                'label': STATUS_LABEL[status],
                'label_plain': STATUS_LABEL_PLAIN[status],
                'first_occurrence': first,
                'members': list(members),
                'others': [m for m in members if m != qid],
            }
    return relations


def family_summary(nodes, relations, qid):
    """One honest candidate-facing sentence about this question's history.

    Never asserts anything about sittings MIW has not transcribed.
    """
    rel = relations[qid]
    if rel['status'] == STATUS_SINGLE:
        return 'Set once in the sittings MIW has transcribed.'
    others = ', '.join('%s %s' % (nodes[m]['month_year'], nodes[m]['q_no'])
                       for m in rel['others'])
    if rel['status'] == STATUS_FIRST:
        return 'First set here. The same task returns at %s.' % others
    first = nodes[rel['first_occurrence']]
    word = 'in the same words' if rel['status'] == STATUS_REPEAT_EXACT else 'reworded'
    sentence = 'Returns %s from %s %s.' % (word, first['month_year'], first['q_no'])
    # The first occurrence has just been named; listing it again under "also"
    # reads as a fourth sitting that does not exist.
    rest = [m for m in rel['others'] if m != rel['first_occurrence']]
    if rest:
        sentence += ' Also set at %s.' % ', '.join(
            '%s %s' % (nodes[m]['month_year'], nodes[m]['q_no']) for m in rest)
    return sentence
