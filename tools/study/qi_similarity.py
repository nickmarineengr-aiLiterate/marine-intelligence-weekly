#!/usr/bin/env python3
"""Deterministic candidate generation for QI family formation.

This module PROPOSES. It never decides. Every merge it proposes is either
confirmed or overturned in `qi_phase1_adjudications.json`, and the builder
refuses to run if a proposal is neither.

Two numbers, and the difference between them is the whole point:

    containment_high = shared / len(smaller token set)
    containment_low  = shared / len(larger token set)

A SYMMETRIC pair (both high) is two statements of the same ask.
An ASYMMETRIC pair (high one way, low the other) is a subset -- almost always
one question being a LIMB of the other. Merging on the high side alone is
exactly how a limb's sitting count gets read as a whole question's, so the
merge threshold is applied to the LOW side only.
"""

import itertools
import re
from collections import defaultdict

# Function words carry no subject and would let any two questions look alike.
STOPWORDS = set(
    'a an the of to in on for and or is are be as at by with that this it its '
    'from which what how why when who whom whose you your we our they their he '
    'she his her not no do does did done shall will would should can could may '
    'might must'.split()
)

MIN_TOKENS = 4          # below this a stem cannot be scored at all
MIN_SHARED = 4          # below this an overlap is noise
BLOCK_MAX_POSTINGS = 60  # a token in >60 entities is too common to block on

# The merge threshold. Applied to containment_LOW.
MERGE_THRESHOLD = 0.75
# Below the merge threshold but above this, a pair is a RELATION candidate.
RELATION_THRESHOLD = 0.60


def tokenize(text):
    """Content tokens of a question stem. Deterministic and order-free."""
    s = re.sub(r'^q\s*\d+\s*[\.\)]?', '', text.lower().strip())
    return {t for t in re.findall(r'[a-z]{3,}', s) if t not in STOPWORDS}


def score(tokens_a, tokens_b):
    """Exact containment pair for two token sets.

    Computed on the FULL token sets. Blocking is a way of finding candidate
    pairs cheaply; reusing a blocked overlap count as the score would deflate
    every pair built from common vocabulary and silently hide real families.
    """
    shared = len(tokens_a & tokens_b)
    if not tokens_a or not tokens_b:
        return 0.0, 0.0, shared
    fa = shared / len(tokens_a)
    fb = shared / len(tokens_b)
    return max(fa, fb), min(fa, fb), shared


def candidate_pairs(texts):
    """texts: {entity_id: stem}. Returns sorted list of scored candidate pairs.

    Deterministic: the output order depends only on the input, never on dict
    iteration order or on when it was run.
    """
    toks = {k: tokenize(v) for k, v in texts.items()}
    scoreable = sorted(k for k in toks if len(toks[k]) >= MIN_TOKENS)

    postings = defaultdict(set)
    for k in scoreable:
        for t in toks[k]:
            postings[t].add(k)

    seen = set()
    for t in sorted(postings):
        ks = postings[t]
        if len(ks) > BLOCK_MAX_POSTINGS:
            continue
        for a, b in itertools.combinations(sorted(ks), 2):
            seen.add((a, b))

    out = []
    for a, b in sorted(seen):
        hi, lo, shared = score(toks[a], toks[b])
        if shared < MIN_SHARED or hi < RELATION_THRESHOLD:
            continue
        out.append({
            'a': a,
            'b': b,
            'containment_high': round(hi, 4),
            'containment_low': round(lo, 4),
            'shared_tokens': shared,
            'proposal': 'MERGE_CANDIDATE' if lo >= MERGE_THRESHOLD else 'RELATION_CANDIDATE',
        })
    out.sort(key=lambda p: (-p['containment_low'], p['a'], p['b']))
    return out


def connected_components(pairs, threshold=MERGE_THRESHOLD):
    """Union-find over merge-strength edges. Returns sorted list of sorted lists."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in pairs:
        if p['containment_low'] < threshold:
            continue
        ra, rb = find(p['a']), find(p['b'])
        if ra != rb:
            parent[rb] = ra

    groups = defaultdict(list)
    for k in list(parent):
        groups[find(k)].append(k)
    return sorted((sorted(v) for v in groups.values()), key=lambda g: g[0])


def weakest_internal_pair(members, texts):
    """Lowest DIRECT containment_low between any two members of a group.

    A group is built by transitive closure, so two members can end up together
    without ever having been compared. This surfaces that: if the weakest direct
    pair is far below the merge threshold, the group was chained together and
    needs a human look before it becomes a family.
    """
    toks = {m: tokenize(texts[m]) for m in members}
    worst = 1.0
    worst_pair = None
    for a, b in itertools.combinations(sorted(members), 2):
        _, lo, _ = score(toks[a], toks[b])
        if lo < worst:
            worst, worst_pair = lo, (a, b)
    return round(worst, 4), worst_pair
