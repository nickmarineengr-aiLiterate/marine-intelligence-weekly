#!/usr/bin/env python3
"""Study Topic Map taxonomy -- ONE deterministic projection of the specs.

    spec primary_category   -->  DOMAIN        (7 roots, a partition)
    spec subject_tags       -->  STUDY TOPIC   (normalised, multi-valued)
    solved questions        -->  leaves

This module is TRANSFORMATION LOGIC, not a second classification system. It
holds no question ids, no counts and no syllabus of its own: everything it
returns is recomputed from the specs on every call. What it does own is the
small alias map below, which folds the spelling variants of one study topic
into one label so that "ISM", "ISM Code" and "Safety Management" are counted
once, not three times.

Two consumers, and they must agree byte-for-byte:

  * build_solvedqp_manifest.py stamps `study_topics` on every question record
    so the runtime `?topic=` filter can match by EQUALITY (never substring);
  * build_topic_map.py renders /solvedQP/topics.html from the same call.

topic_map_test.py proves the two are the same set for every emitted topic.
"""
import re

# --------------------------------------------------------------------------- #
# Alias map -- Founder-approved and re-verified against the corpus.
#
# Every KEY here is a label that actually appears in a solved spec's
# subject_tags (topic_map_test.py rule 10 fails on a stale key). Keys are
# matched after case-folding and whitespace-collapsing, so a key is written in
# its canonical printed form once and its case variants fold onto it for free.
#
# Nothing speculative: a merge is listed only where the two labels name the
# same study topic on their face. Adjacent-but-different topics ("Decarbon-
# isation" beside "Alternative Fuels", "Statutory Framework" beside "Survey &
# Certification") are deliberately NOT merged.
# --------------------------------------------------------------------------- #
ALIASES = {
    # Founder decision 1: Safety Management -> ISM Code.
    'ISM': 'ISM Code',
    'ISM Code': 'ISM Code',
    'Safety Management': 'ISM Code',

    'MLC': 'MLC 2006',
    'MLC 2006': 'MLC 2006',

    'Port State Control': 'Port State Control',

    # Founder decision 3: Indian Legislation is one study topic wherever it
    # occurs, and may also be its own root domain.
    'Indian Legislation': 'Indian Legislation',
    'Indian Law': 'Indian Legislation',
    'Indian Maritime Law': 'Indian Legislation',
    'Indian Maritime Legislation': 'Indian Legislation',
    'Merchant Shipping Act': 'Indian Legislation',
    'Indian maritime administration': 'Indian Legislation',

    'Casualty & Investigation': 'Casualty & Investigation',
    'Casualty Investigation': 'Casualty & Investigation',
    'Accident Investigation': 'Casualty & Investigation',
    'incident investigation': 'Casualty & Investigation',

    'Survey': 'Survey & Certification',
    'Statutory Survey': 'Survey & Certification',
    'Statutory Certification': 'Survey & Certification',
    'Survey and Certification': 'Survey & Certification',
    'Inspection': 'Survey & Certification',

    'Cyber Security': 'Cyber Risk',
    'Cyber Risk': 'Cyber Risk',

    'Digitalisation': 'Digitalisation',
    'Digital Technology': 'Digitalisation',
    'data analytics': 'Digitalisation',

    'Naval Architecture': 'Ship Design',
    'Ship Design': 'Ship Design',
    'Ship Construction': 'Ship Design',

    'Alternative Fuels': 'Alternative Fuels',
    'Alternative Fuels & Decarbonisation': 'Alternative Fuels',

    'Training': 'Training & Competence',
    'Training and Competence': 'Training & Competence',
}

# A normalised subject label becomes an explicit study topic inside a domain
# once this many DISTINCT solved questions in that domain carry it. Below the
# threshold the questions stay reachable through the domain's "Other" bucket.
THRESHOLD = 3

OTHER_LABEL = 'Other topics in this domain'

# How many topic_tags a study topic may advertise as "Also covers", and the
# minimum number of the topic's own questions a tag must appear in before it
# is shown. Two, not one: a tag on a single question is that question's label,
# not the topic's.
ALSO_COVERS_MAX = 3
ALSO_COVERS_MIN_Q = 2
# Tags too generic to tell a candidate anything on an "Also covers" line.
# Presentation hygiene only; the tags stay in the manifest and in search.
ALSO_COVERS_SKIP = frozenset({'code', 'convention'})

# Six-year query parameter names. The runtime reads exactly these.
PARAM_TOPIC = 'topic'
PARAM_DOMAIN = 'domain'


def _key(label):
    return re.sub(r'\s+', ' ', str(label or '')).strip().casefold()


_ALIAS_BY_KEY = {_key(k): v for k, v in ALIASES.items()}


def canonical_forms(specs_or_questions):
    """Case-fold table: folded key -> printed label, chosen by frequency.

    For labels NOT in ALIASES, the display form is the most frequent printed
    casing across the solved corpus, ties broken alphabetically. Deterministic,
    and derived: no hand list of preferred spellings.
    """
    counts = {}
    for q in _iter_questions(specs_or_questions):
        for s in q.get('subject_tags') or []:
            k = _key(s)
            if not k:
                continue
            counts.setdefault(k, {})
            counts[k][s.strip()] = counts[k].get(s.strip(), 0) + 1
    out = {}
    for k, forms in counts.items():
        best = sorted(forms.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        out[k] = best
    return out


def _iter_questions(specs_or_questions):
    for item in specs_or_questions:
        if isinstance(item, dict) and 'questions' in item:
            for q in item['questions']:
                yield q
        else:
            yield item


def make_normaliser(specs_or_questions):
    """Return normalise(label) -> canonical study-topic label (or None)."""
    forms = canonical_forms(specs_or_questions)

    def normalise(label):
        k = _key(label)
        if not k:
            return None
        if k in _ALIAS_BY_KEY:
            return _ALIAS_BY_KEY[k]
        return forms.get(k, re.sub(r'\s+', ' ', str(label).strip()))
    return normalise


def study_topics_for(q, normalise):
    """Deduplicated, order-preserving list of study topics for one question."""
    out = []
    for s in q.get('subject_tags') or []:
        c = normalise(s)
        if c and c not in out:
            out.append(c)
    return out


def sitting_key(d):
    return (d['year'], d.get('month_num') or _month_num(d.get('month')))


def _month_num(month):
    import recurrence_model as RM
    return RM.MONTH_NUM[month]


def build_topic_map(sittings, normalise=None):
    """Compute the whole map from SOLVED sittings (specs that carry answers).

    Returns a plain, JSON-serialisable structure:

      {'domains': [ {label, question_ids, sitting_count, latest,
                     topics: [ {label, question_ids, sitting_count, latest,
                                also_covers: [..]} ],
                     other: {label, question_ids} } ],
       'question_ids': [...],  # every solved question id, once
       'sittings': N, 'questions': N,
       'alias_count': N}

    Ordering is total: domains by question count desc then label; topics by
    question count desc then label; question ids newest sitting first, then
    question number.
    """
    normalise = normalise or make_normaliser(sittings)
    # (sitting_key desc, q_no asc) sort for every question list.
    order = {}
    meta = {}
    for d in sittings:
        sk = sitting_key(d)
        for q in d['questions']:
            qid = q['question_id']
            order[qid] = (-sk[0], -sk[1], _qnum(q['q_no']))
            meta[qid] = (d, q)

    def sort_ids(ids):
        return sorted(ids, key=lambda i: order[i])

    def sitting_stats(ids):
        """(distinct sitting count, label of the newest sitting)."""
        papers = {meta[i][0]['paper_id'] for i in ids}
        newest = meta[sort_ids(ids)[0]][0]
        return len(papers), '%s %d' % (newest['month'], newest['year'])

    domains = {}
    for d in sittings:
        for q in d['questions']:
            dom = q.get('primary_category')
            if not dom:
                raise AssertionError('%s has no primary_category' % q['question_id'])
            domains.setdefault(dom, {})
            domains[dom].setdefault('__all__', []).append(q['question_id'])
            for t in study_topics_for(q, normalise):
                domains[dom].setdefault(t, [])
                if q['question_id'] not in domains[dom][t]:
                    domains[dom][t].append(q['question_id'])

    out_domains = []
    for dom, table in domains.items():
        all_ids = sort_ids(table.pop('__all__'))
        topics = []
        covered = set()
        for label, ids in table.items():
            if len(ids) >= THRESHOLD:
                ids = sort_ids(ids)
                sc, latest = sitting_stats(ids)
                topics.append({
                    'label': label,
                    'question_ids': ids,
                    'sitting_count': sc,
                    'latest': latest,
                    'also_covers': _also_covers(label, ids, meta),
                })
                covered.update(ids)
        topics.sort(key=lambda t: (-len(t['question_ids']), t['label']))
        other_ids = [i for i in all_ids if i not in covered]
        sc, latest = sitting_stats(all_ids)
        out_domains.append({
            'label': dom,
            'question_ids': all_ids,
            'sitting_count': sc,
            'latest': latest,
            'topics': topics,
            'other': {'label': OTHER_LABEL, 'question_ids': other_ids},
        })
    out_domains.sort(key=lambda x: (-len(x['question_ids']), x['label']))

    all_q = sort_ids(order.keys())
    return {
        'domains': out_domains,
        'question_ids': all_q,
        'sittings': len(sittings),
        'questions': len(all_q),
        'alias_count': len(ALIASES),
        'threshold': THRESHOLD,
    }


def _qnum(q_no):
    m = re.search(r'\d+', str(q_no))
    return int(m.group(0)) if m else 0


def _also_covers(topic_label, ids, meta):
    """Top topic_tags inside this topic's questions, for the 'Also covers' line.

    A tag is eligible when it appears in at least ALSO_COVERS_MIN_Q distinct
    questions of the topic and is not merely the topic's own name. Ordering is
    (count desc, label) so the line is stable across builds.
    """
    counts = {}
    for i in ids:
        q = meta[i][1]
        seen = set()
        for t in q.get('topic_tags') or []:
            t = re.sub(r'\s+', ' ', str(t)).strip()
            k = t.casefold()
            if not t or k in seen or k == topic_label.casefold() or k in ALSO_COVERS_SKIP:
                continue
            seen.add(k)
            counts.setdefault(k, [0, t])
            counts[k][0] += 1
    ranked = sorted(((n, lbl) for n, lbl in counts.values()),
                    key=lambda x: (-x[0], x[1].casefold()))
    return [lbl for n, lbl in ranked if n >= ALSO_COVERS_MIN_Q][:ALSO_COVERS_MAX]


def topic_query(topic, domain):
    """The structured filter URL for one Topic Map leaf, domain-scoped."""
    from urllib.parse import quote
    return '/solvedQP/?%s=%s&%s=%s' % (PARAM_TOPIC, quote(topic, safe=''),
                                       PARAM_DOMAIN, quote(domain, safe=''))


def domain_query(domain):
    from urllib.parse import quote
    return '/solvedQP/?%s=%s' % (PARAM_DOMAIN, quote(domain, safe=''))
