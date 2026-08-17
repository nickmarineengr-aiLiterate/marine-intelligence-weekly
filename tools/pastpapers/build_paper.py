#!/usr/bin/env python3
"""MIW past written papers -- deterministic interactive paper builder.

Usage:
  python build_paper.py <spec.json> [-o <outfile>] [--gated] [--publish]

Assembles meoclass1/pastpapers/<PAPER_ID>.html from:
  - template/style.css      (verbatim from a live reference file, via extract_shell.py)
  - template/pastpapers.css (this product's styles)
  - template/paper.js       (client behaviour)
  - a JSON content spec (validated first by validate_spec.py)

Interaction model follows meoclass1/QB10_A.html. Every question becomes a
collapsible card carrying a Model Written Answer, an expandable Study Guide and
a Quick Revision block, all generated from the one canonical question object --
no answer text is ever duplicated across files.

Modes:
  default   Founder review: noindex, quality banner, production metadata visible
            in a collapsed per-question block.
  --publish Student-facing: full SEO head, JSON-LD, production metadata omitted.
  --gated   Adds the access gate. The review workflow never uses it.

Determinism: no clock reading, no random value, no absolute path. Every date
rendered comes from the spec, so re-running with an unchanged spec is
byte-identical -- audit_paper.py asserts this.
"""
import argparse, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, TPL, BASE, CONTACT, LS_BOOKMARKS, LS_PROGRESS,
                           LS_MIGRATE_JS, STICKY_SYNC_JS, GATE, GATE_STUB, esc, esc_attr, strip_tags,
                           read_css, block_text, search_tokens, topbar, head_meta, footer,
                           is_intake, corpus_relations, delivery_links, promo_links,
                           load_all_specs, CORPUS_SEARCH_JS, corpus_fallback_block)
import recurrence_model as RM

CHEV = ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>')


# ------------------------------------------------------------------ blocks

def render_blocks(blocks, out, indent='    '):
    for nd in blocks.get('blocks', []):
        if 'h' in nd:
            out.append('%s<h3>%s</h3>' % (indent, esc(nd['h'])))
        elif 'p' in nd:
            out.append('%s<p>%s</p>' % (indent, esc(nd['p'])))
        elif 'ul' in nd:
            out.append('%s<ul>' % indent)
            for li in nd['ul']:
                out.append('%s  <li>%s</li>' % (indent, esc(li)))
            out.append('%s</ul>' % indent)
        elif 'ol' in nd:
            out.append('%s<ol>' % indent)
            for li in nd['ol']:
                out.append('%s  <li>%s</li>' % (indent, esc(li)))
            out.append('%s</ol>' % indent)
        elif 'table' in nd:
            t = nd['table']
            out.append('%s<table class="reg-tbl">' % indent)
            out.append('%s  <tr>%s</tr>' % (
                indent, ''.join('<th>%s</th>' % esc(h) for h in t['headers'])))
            for row in t['rows']:
                out.append('%s  <tr>%s</tr>' % (
                    indent, ''.join('<td>%s</td>' % esc(c) for c in row)))
            out.append('%s</table>' % indent)
        else:
            raise ValueError('unknown block type: %r' % list(nd.keys()))


# ------------------------------------------------------------------ card

def quick_revision(qr, out):
    out.append('  <section class="layer qr" aria-label="Quick revision">')
    out.append('    <div class="layer-title">Quick revision</div>')
    out.append('    <dl>')
    if qr.get('recall_15s'):
        out.append('      <dt>15-second recall</dt><dd>%s</dd>' % esc(qr['recall_15s']))
    # The skeleton is NOT repeated here. It renders once per card, as the Exam
    # Approach block above the model answer, where it does its actual job:
    # showing the shape of the answer before the prose rather than after it.
    if qr.get('keywords'):
        out.append('      <dt>Keywords</dt><dd>%s</dd>'
                   % ''.join('<span class="kw">%s</span>' % esc(k) for k in qr['keywords']))
    if qr.get('critical_numbers'):
        out.append('      <dt>Critical numbers</dt><dd><ul>')
        for n in qr['critical_numbers']:
            out.append('        <li>%s</li>' % esc(n))
        out.append('      </ul></dd>')
    if qr.get('critical_regulation'):
        out.append('      <dt>Critical regulation</dt><dd>%s</dd>' % esc(qr['critical_regulation']))
    if qr.get('major_trap'):
        out.append('      <dt>Major trap</dt><dd class="trap">%s</dd>' % esc(qr['major_trap']))
    out.append('    </dl>')
    out.append('  </section>')


# --------------------------------------------------------------- learner views
#
# Everything below is DERIVED from answer_route. The route is the one canonical
# numbered sequence: the model answer's principal headings are its steps, and so
# are the map branches, the recall blanks and the exam plan. A candidate learns
# one route, not four competing structures. See docs/MIW_LEARNING_METHOD_DESIGN.md.

MODES = [('understand', 'Understand'), ('plan', 'Exam Plan'), ('answer', 'Answer'),
         ('guide', 'Study Guide'), ('recall', 'Recall')]


def route_steps(q):
    return ((q.get('answer_route') or {}).get('steps')) or []


def limb_groups(q):
    """Route steps grouped by question limb, preserving order."""
    groups, cur = [], None
    for s in route_steps(q):
        if cur is None or cur[0] != s.get('limb'):
            cur = (s.get('limb'), [])
            groups.append(cur)
        cur[1].append(s)
    return groups


def limb_marks(q):
    """Normalised map of subpart label -> marks, for the exam-plan limb dividers.

    Two subpart key conventions coexist under schema_version 1.3: most of the
    corpus writes `ref` ("a)"), the newest papers write `label` ("(a)"). Route
    `limb` values vary the same way ("a", "a)", "(a)", "A."), so both sides are
    reduced to alphanumerics before matching. Anything that fails to match --
    a scaffold limb such as "framing" or "main", or a subpart whose `marks` the
    source paper never stated -- is simply absent from this map, and the caller
    falls back to the bare label.

    Marks are NEVER inferred. A 16-mark question with two unmarked limbs stays
    unmarked: preserving the source paper's silence is the point, because a
    guessed 8+8 would teach the candidate a split the examiner never published.
    """
    marks = {}
    for s in (q.get('subparts') or []):
        key = s.get('label') if s.get('label') is not None else s.get('ref')
        key = re.sub(r'[^a-z0-9]', '', (key or '').lower())
        if key and s.get('marks') is not None:
            marks[key] = s['marks']
    return marks


def learn_bar(q, out):
    """Mode selector. 'Answer' is pre-selected.

    Expertise reversal: scaffolding that helps a novice costs an expert. A
    candidate who already knows the topic must reach the model answer without
    being walked through the ladder, so the answer is the default view and every
    other mode is one click, never a gate.
    """
    out.append('  <div class="learn-bar" role="tablist" aria-label="Study mode">')
    for key, label in MODES:
        if key == 'understand' and not (q.get('understand_first') or route_steps(q)):
            continue
        cur = 'true' if key == 'answer' else 'false'
        out.append('    <button class="learn-btn" type="button" role="tab" '
                   'data-mode="%s" aria-selected="%s">%s</button>' % (key, cur, label))
    out.append('  </div>')


def understand_view(q, out):
    uf = q.get('understand_first')
    if uf:
        out.append('  <section class="layer uf" aria-label="Understand this first">')
        out.append('    <div class="layer-title">Understand this first</div>')
        out.append('    <p>%s</p>' % esc(uf))
        out.append('  </section>')
    knowledge_map(q, out)


def knowledge_map(q, out):
    """Knowledge map: root, then one branch per route step.

    A semantic nested list, not an SVG island -- it reflows on a phone for free
    and a screen reader can walk it. The branch titles can be hidden so the map
    works as RETRIEVAL rather than as a picture to read: the evidence for mapping
    is much stronger when the learner reconstructs it than when they consume it.
    """
    steps = route_steps(q)
    if not steps:
        return
    out.append('  <section class="layer kmap" aria-label="Knowledge map">')
    out.append('    <div class="layer-title">Knowledge map'
               '<button class="kmap-toggle" type="button" aria-pressed="false">'
               'Hide branches</button></div>')
    out.append('    <div class="kmap-root">%s</div>' % esc(q.get('short_title', q['q_no'])))
    out.append('    <ol class="kmap-tree">')
    for limb, group in limb_groups(q):
        if limb:
            out.append('      <li class="kmap-limb"><span class="kmap-limb-l">%s</span>'
                       % esc(limb))
            out.append('        <ol>')
        for s in group:
            out.append('%s<li class="kmap-branch"><span class="kmap-n">%d</span>'
                       '<span class="kmap-t">%s</span>'
                       % ('          ' if limb else '      ', s['n'], esc(s['title'])))
            kids = (s.get('points') or [])[:3]
            if kids:
                out.append('%s<ul class="kmap-kids">%s</ul>'
                           % ('            ' if limb else '        ',
                              ''.join('<li>%s</li>' % esc(k) for k in kids)))
            out.append('%s</li>' % ('          ' if limb else '      '))
        if limb:
            out.append('        </ol>')
            out.append('      </li>')
    out.append('    </ol>')
    out.append('  </section>')


def plan_view(q, out):
    """Start here: the headings to write first, with their points beneath them.

    This is the fix for "I could not finish in time". Writing the framework
    first means an interrupted answer still shows the examiner the whole shape.

    The superseded view printed every route heading TWICE -- once as the plan
    list and again inside a collapsed <details> -- and that duplication is the
    reason the core points had to be hidden at all. Merging the two into one
    list is what makes the points affordable on screen, so a candidate asking
    for "a bullet version of the answer" is given it on arrival instead of
    having to discover that a collapsed control holds it.

    There is one renderer and no opt-in. The points are the SAME
    answer_route.steps[].points the model answer, knowledge map and recall test
    derive from -- no second corpus, no new field, nothing authored twice, so
    nothing can drift.
    """
    steps = route_steps(q)
    if not steps:
        return
    n_pts = sum(len(s.get('points') or []) for s in steps)
    out.append('  <section class="layer plan" aria-label="Exam plan">')
    out.append('    <div class="layer-title">Start here '
               '<span class="plan-marks">%s marks</span></div>' % q['total_marks'])
    out.append('    <p class="plan-lead">Write these headings first, then expand them '
               'in order. If time is short, get every heading down before you expand '
               'any of them.</p>')
    out.append('    <div class="plan-cap">Bullet answer &mdash; points to write</div>')
    marks = limb_marks(q)
    for limb, group in limb_groups(q):
        if limb:
            # The candidate is being told what to write; what each limb is worth
            # decides how much of the time budget it deserves. Shown only where
            # the source paper actually stated the split -- never derived from
            # the total, and never divided equally across limbs.
            m = marks.get(re.sub(r'[^a-z0-9]', '', limb.lower()))
            out.append('    <div class="plan-limb">%s%s</div>'
                       % (esc(limb),
                          '' if m is None else
                          ' <span class="pl-mk">&middot; %d marks</span>' % m))
        out.append('    <ol class="plan-list">')
        for s in group:
            pts = s.get('points') or []
            out.append('      <li value="%d"><span class="pl-t">%s</span>%s</li>'
                       % (s['n'], esc(s['title']),
                          ('<ul class="pl-pts">%s</ul>'
                           % ''.join('<li>%s</li>' % esc(p) for p in pts)) if pts else ''))
        out.append('    </ol>')
    if q.get('memory_cue'):
        out.append('    <p class="plan-cue"><b>Memory cue.</b> %s</p>'
                   % esc(q['memory_cue']))
    # The two-level hierarchy is explicit, because the memory target and the
    # coverage target are different things. Candidates who try to memorise 25
    # core points are doing the wrong work: the route is what gets memorised.
    out.append('    <div class="plan-cov">')
    out.append('      <div class="cov-row"><span class="cov-k">Remember</span>'
               '<span class="cov-v"><b>%d</b> route headings</span></div>' % len(steps))
    out.append('      <div class="cov-row"><span class="cov-k">Cover</span>'
               '<span class="cov-v"><b>%d</b> core points beneath them</span></div>' % n_pts)
    out.append('    </div>')
    out.append('    <p class="plan-note">Memorise the <b>%d headings</b>. The core points '
               'are there to help you check whether an answer is too thin &mdash; they are '
               'not a mark scheme, and they are not %d separate facts to learn '
               'individually.</p>' % (len(steps), n_pts))
    out.append('  </section>')


def reference_shelf(q, out, publish):
    """The verification layer. NOT a sixth study mode.

    The five modes are a study cycle: understand, plan, write, review, recall.
    "Where does this actually come from?" is a different question -- it is
    evidence, not another way of studying the same answer -- so the shelf sits
    after the answer content rather than competing with the learning sequence.

    Renders nothing at all when a question carries no shelf, which is the state
    of every question until the Founder supplies corpus mappings. Answers and
    corpus objects are produced on parallel tracks: a missing object must never
    block a build, and must never be papered over with a fabricated link.

    Publish behaviour omits anything not resolvable, rather than shipping a
    control that leads nowhere. Review behaviour shows the pending state so
    production can see the gap.
    """
    shelf = q.get('reference_shelf') or []
    if not shelf:
        return
    shown = [r for r in shelf
             if publish is False or r.get('state') == 'REFERENCE_AVAILABLE']
    if not shown:
        return
    out.append('  <section class="layer refshelf" aria-label="Reference shelf">')
    out.append('    <div class="layer-title">Reference shelf</div>')
    out.append('    <p class="rs-lead">Where the requirements in this answer come from.</p>')
    for r in shown:
        avail = r.get('state') == 'REFERENCE_AVAILABLE'
        out.append('    <div class="rs-item%s">' % ('' if avail else ' rs-pending'))
        out.append('      <div class="rs-rel">%s</div>'
                   % esc(r.get('relationship', '').replace('_', ' ').title()))
        out.append('      <div class="rs-label">%s</div>' % esc(r['label']))
        if r.get('claim_scope'):
            out.append('      <div class="rs-scope">%s</div>' % esc(r['claim_scope']))
        if avail:
            # The resolver owns document, edition, bookmark and page. This link
            # carries the OBJECT id only, so re-pagination cannot break it.
            #
            # FAIL CLOSED. reference_href() returns None while no governed
            # viewer route exists, and then no control is emitted at all. The
            # citation above -- relationship, label, scope -- is the evidence
            # and stands on its own; a button to a route that 404s is worse
            # than no button. Availability of the SOURCE and availability of a
            # PUBLIC VIEWER are different facts, and only the first is claimed
            # here.
            href = reference_href(r['object_id'])
            if href:
                out.append('      <a class="nav-btn rs-open" href="%s">Verify source</a>'
                           % esc_attr(href))
        elif not publish:
            out.append('      <span class="rs-state">%s</span>'
                       % esc(r.get('state', '').replace('_', ' ').lower()))
        out.append('    </div>')
    out.append('  </section>')


def reference_href(object_id):
    """Single place that knows how an object id becomes a viewer route.

    Deliberately the ONLY coupling point between the paper builder and the
    reference viewer. When the resolver and viewer land, this function changes
    and nothing else does. It never emits a document or page.

    Returns None while no viewer route is governed. Callers must treat None as
    "render the citation, emit no control" -- never as "the source is missing".
    """
    if not REFERENCE_ROUTE_BASE:
        return None
    return '%s/%s' % (REFERENCE_ROUTE_BASE, object_id)


# Stands in for CORPUS_SEARCH_JS on every build that renders no corpus panel.
# paper.js guards its one entry point with `if (!mcWrap || !mcRes) return;`
# before it touches MIWCorpus, so the symbol is never reached on these pages.
CORPUS_SEARCH_ABSENT = ('  // No corpus panel on this build, so no cross-paper '
                        'search payload is inlined.')


# No public reference viewer exists. `None` is that fact stated once, in the
# one place the builder consults, so no paper can regenerate a route that 404s.
#
# This was '/reference', written while the shelf rendered nothing anywhere --
# a provisional value that became live the moment QP2307 became the first paper
# to carry REFERENCE_AVAILABLE objects, and shipped 19 dead buttons per copy.
# A provisional constant is only safe while nothing renders it, and nothing
# announces the day that stops being true.
#
# To turn the shelf's links on: build the resolver route, then set this to its
# base path. Nothing else changes, and the negative control in
# reference_route_test.py must be updated in the same commit.
REFERENCE_ROUTE_BASE = None


def recall_view(q, out):
    """Blank skeleton first, then cards.

    Pretesting: attempting to retrieve BEFORE seeing the material helps even when
    the attempt fails, provided the correct answer follows immediately. So the
    blanks come first and reveal on demand. No typing is required -- the attempt
    is what matters, not capturing it.
    """
    steps = route_steps(q)
    if steps:
        out.append('  <section class="layer recall" aria-label="Recall the structure">')
        out.append('    <div class="layer-title">Recall the structure</div>')
        out.append('    <p class="recall-lead">Before you read the answer: can you name '
                   'all %d sections, in order? Say them or write them down, then reveal.</p>'
                   % len(steps))
        out.append('    <ol class="recall-list" data-state="hidden">')
        for s in steps:
            out.append('      <li value="%d"><span class="recall-blank" aria-hidden="true">'
                       '__________</span><span class="recall-answer" hidden>%s%s</span></li>'
                       % (s['n'], ('%s ' % esc(s['limb'])) if s.get('limb') else '',
                          esc(s['title'])))
        out.append('    </ol>')
        out.append('    <button class="recall-toggle" type="button" aria-expanded="false">'
                   'Reveal the structure</button>')
        out.append('  </section>')

    cards = q.get('retrieval_cards') or []
    if cards:
        out.append('  <section class="layer cards" aria-label="Flashcards">')
        out.append('    <div class="layer-title">Flashcards '
                   '<span class="cards-n">%d</span></div>' % len(cards))
        for c in cards:
            out.append('    <div class="card" id="%s">' % esc_attr(c['id']))
            out.append('      <button class="card-q" type="button" aria-expanded="false" '
                       'aria-controls="%s-a"><span class="card-type">%s</span>%s</button>'
                       % (esc_attr(c['id']), esc(c.get('type', '')), esc(c['prompt'])))
            out.append('      <div class="card-a" id="%s-a" hidden>' % esc_attr(c['id']))
            out.append('        <p>%s</p>' % esc(c['answer']))
            if c.get('why'):
                out.append('        <p class="card-why">%s</p>' % esc(c['why']))
            out.append('      </div>')
            out.append('    </div>')
        out.append('  </section>')


def build_card(q, paper, out, publish, corpus=None, deliver=False, delivered_ids=None,
               promo=False):
    qid = q['question_id']
    subjects = ' '.join((q.get('subject_tags') or [])).lower()
    # Canonical, chronological recurrence -- computed over the whole corpus, not
    # read off this spec. The two fields that used to drive this badge were the
    # host's printed annotation and the authoring field recurrence_class, and
    # both state things that are not true of the calendar. See recurrence_check.py.
    nodes, relations = corpus if corpus else corpus_relations()
    rel = relations[qid]
    out.append('<article class="q-card" id="%s" data-qid="%s" data-subjects="%s" data-search="%s">'
               % (q['anchor'], esc_attr(qid), esc_attr(subjects),
                  esc_attr(search_tokens(q, paper, rel))))
    out.append('  <div class="q-head">')
    out.append('    <button class="q-toggle" type="button" aria-expanded="false" '
               'aria-controls="%s-body">' % esc_attr(q['anchor']))
    out.append('      <span class="q-num">%s</span>' % esc(q['q_no']))
    out.append('      <span class="q-main">')
    out.append('        <span class="q-title">%s</span>' % esc(q.get('short_title', q['q_no'])))
    out.append('        <span class="q-meta">%s marks<span class="sep">&middot;</span>%s'
               '<span class="sep">&middot;</span>%s</span>'
               % (q['total_marks'], esc(paper['month_year']), rel['label']))
    for line in q['text_verbatim'].split('\n'):
        out.append('        <span class="q-stem">%s</span>' % esc(line))
    out.append('        <span class="q-tags">')
    for t in (q.get('subject_tags') or []):
        out.append('          <span class="q-tag">%s</span>' % esc(t))
    for t in (q.get('topic_tags') or [])[:4]:
        out.append('          <span class="q-tag sub">%s</span>' % esc(t))
    if rel['family_size'] > 1:
        out.append('          <span class="q-tag rec">%d sitting%s in this set</span>'
                   % (rel['family_size'], '' if rel['family_size'] == 1 else 's'))
    out.append('        </span>')
    out.append('      </span>')
    out.append('      %s' % CHEV)
    out.append('    </button>')
    out.append('    <div class="q-acts">')
    out.append('      <button class="icon-btn bm" type="button" aria-pressed="false" '
               'aria-label="Bookmark %s" title="Bookmark this question">&#9733;</button>' % esc_attr(qid))
    out.append('      <button class="icon-btn st" type="button" aria-pressed="false" '
               'aria-label="Mark %s as studied" title="Mark as studied">&#10003;</button>' % esc_attr(qid))
    out.append('    </div>')
    out.append('  </div>')

    out.append('  <div class="q-body" id="%s-body" hidden>' % esc_attr(q['anchor']))

    # Learner modes. Every section renders unhidden; paper.js switches them once
    # it has run. With scripting off nothing is hidden, so the model answer is
    # still reachable -- the learning layer must never be able to hide the answer.
    learn_bar(q, out)

    out.append('  <div class="mode" data-mode="understand">')
    understand_view(q, out)
    out.append('  </div>')

    out.append('  <div class="mode" data-mode="plan">')
    plan_view(q, out)
    out.append('  </div>')

    out.append('  <div class="mode" data-mode="answer">')
    out.append('  <section class="layer ma" aria-label="Model written answer">')
    out.append('    <div class="layer-title">Model written answer</div>')
    render_blocks(q['model_answer'], out)
    out.append('  </section>')
    out.append('  </div>')

    out.append('  <div class="mode" data-mode="guide">')
    out.append('  <section class="layer sg-open" aria-label="Study guide">')
    out.append('    <div class="layer-title">Study guide</div>')
    render_blocks(q['study_notes'], out, indent='      ')
    out.append('  </section>')
    out.append('  </div>')

    out.append('  <div class="mode" data-mode="recall">')
    recall_view(q, out)
    quick_revision(q.get('quick_revision') or {}, out)
    out.append('  </div>')

    # Verification layer, outside the mode selector. Distinct from cross_links
    # below: the shelf answers "where does this truth come from?", cross_links
    # answers "where else has this been examined?". Different relationships.
    reference_shelf(q, out, publish)

    xl = q.get('cross_links') or []
    if deliver:
        # Cross-links are authored RELATIVE to the review location
        # /meoclass1/pastpapers/, so '../QB10_B.html' and
        # '../oralnotes/...' resolve correctly there and resolve to
        # non-existent root paths from /solvedQP/. They also point into the
        # Oral product, which a Written-only customer does not own.
        #
        # The delivery guard in solvedqp_check.py matches absolute
        # href="/meoclass1/..." only, so these relative links would ship as
        # silent dead ends inside a paid page. Keep only sibling links to
        # papers that are actually delivered; those resolve within
        # /solvedQP/ unchanged.
        xl = [x for x in xl
              if re.match(r'^QP\d+\.html(?:#|$)', str(x.get('href', '')))
              and (delivered_ids is None
                   or str(x['href']).split('.')[0] in delivered_ids)]
    elif promo:
        # The mirror image of the delivery case, and it fails the other way.
        # From /meoclass1/oralnotes/, the '../' links into the Oral product
        # resolve correctly AND are inside this reader's own entitlement, so
        # they stay. The bare sibling links do not: 'QP2607.html#q5' resolves
        # to /meoclass1/oralnotes/QP2607.html, which has never existed.
        #
        # Rewriting them to /solvedQP/QP2607.html would make them resolve and
        # would still be wrong -- an unlabelled link out of a free sample into
        # a product this reader has not bought is an entitlement bounce wearing
        # a cross-reference's clothes. The page already asks for the sale twice,
        # in words, above and below. Drop them.
        xl = [x for x in xl
              if not re.match(r'^QP\d+\.html(?:#|$)', str(x.get('href', '')))]
    if xl:
        out.append('  <p class="rec-note">Also on the platform: %s</p>'
                   % ' &middot; '.join('<a href="%s">%s</a>'
                                       % (esc_attr(x['href']), esc(x['label'])) for x in xl))
    # Recurrence, candidate-facing. One honest sentence, computed from the
    # calendar over MIW's own transcriptions. What used to stand here was the
    # source copy host's printed "previously asked" table, republished verbatim
    # -- another party's analysis, proved wrong in both directions by the 2026
    # set, shipped to a paying student as though MIW had established it.
    out.append('  <p class="rec-note"><span class="q-tag rec">%s</span> %s</p>'
               % (rel['label'], RM.family_summary(nodes, relations, qid)))

    # Production metadata: review mode only. Never shipped to students.
    if not publish:
        out.append('  <details class="prod-meta">')
        out.append('    <summary>Production metadata (review build only)</summary>')
        out.append('    <div class="pm-inner">')
        out.append('      <b>Reuse tier</b> %s &middot; <b>Verification</b> %s'
                   % (esc(q.get('reuse_tier') or '?'), esc(q.get('verification_status') or '')))
        ps = q.get('provenance_summary') or {}
        if ps:
            out.append('      <br><b>Provenance</b> %s'
                       % esc(' · '.join('%s %s' % (k, v) for k, v in ps.items() if v)))
        if q.get('sources'):
            out.append('      <br><b>Sources</b><ul>')
            for s in q['sources']:
                out.append('        <li>%s</li>' % esc(s))
            out.append('      </ul>')
        if q.get('unresolved'):
            out.append('      <b>Unresolved</b><ul>')
            for u in q['unresolved']:
                out.append('        <li>%s</li>' % esc(u))
            out.append('      </ul>')
        rv = q.get('reverify_before_publication') or []
        if rv:
            out.append('      <b>Re-verify before publication</b><ul>')
            for r in rv:
                out.append('        <li>%s &mdash; %s <i>(%s)</i></li>'
                           % (esc(r.get('claim', '')), esc(r.get('why', '')), esc(r.get('class', ''))))
            out.append('      </ul>')
        out.append('    </div>')
        out.append('  </details>')

    out.append('  </div>')
    out.append('</article>')


# ------------------------------------------------------------------ document

PROMO_SLUG = 'written-sample-january-2026'


def promo_header():
    """Top banner on the Written promo shown to existing Oral subscribers."""
    return [
        '<div class="review-banner" style="background:#f0fdfa;border-color:#99f6e4;color:#134e4a">',
        '  <strong>Written Question Paper sample.</strong> Preparing for Written too? '
        'As an MIW Oral subscriber you can study this complete January 2026 Written paper '
        'here &mdash; all nine questions, all five study modes, nothing withheld. '
        '<a href="/SQ/index.html#solved-qp" style="font-weight:600">Unlock the full Solved QP '
        'collection &mdash; &#8377;1,500 &rarr;</a>',
        '</div>',
    ]


def promo_footer(newest_label):
    """Closing CTA. The newest sitting is derived from the specs, never typed."""
    newest = newest_label or 'the newest available sitting'
    return [
        '<section class="cheat" id="solved-qp-cta">',
        '  <h2>Continue with all solved Written papers</h2>',
        '  <p class="lead">January is your complete subscriber sample. Full Solved QP access '
        'includes every currently available solved paper, including the newest available '
        'sitting &mdash; <strong>%s</strong> &mdash; and every paper added after it.</p>' % esc(newest),
        '  <p class="lead" style="font-size:1.05rem"><strong>&#8377;1,500</strong> one-time.</p>',
        '  <p><a class="sample-card-btn" href="/SQ/index.html#solved-qp" '
        'style="display:inline-block;background:#0d9488;color:#fff;text-decoration:none;'
        'padding:11px 22px;border-radius:8px;font-weight:600">Get Solved QP Access &rarr;</a></p>',
        '</section>',
        '',
    ]


def build(spec, gated=False, publish=False, deliver=False, promo=False, newest_label=None):
    # promo = the complete January paper shown to existing ORAL subscribers
    # inside /meoclass1/oralnotes/. It is customer-facing (so no production
    # metadata and no review banner) but it lives under the Oral product root
    # and is opened by the ORAL entitlement, not by SOLVED_QP. It demonstrates
    # the Written product; it does not grant it.
    # deliver = the paid customer copy served from /solvedQP/.
    #
    # It is a customer-facing build, so it carries no production metadata and
    # no Founder review banner. It stays noindex and emits NO JSON-LD, because
    # paid answers must never reach structured data -- which is why `publish`
    # itself stays False here and only `content_publish` is raised.
    #
    # It does NOT need to suppress recurrence. The two signals that were unsafe
    # to show a candidate -- the source copy host's printed annotation and the
    # authoring field recurrence_class -- are no longer rendered or searched in
    # ANY mode: render_common.search_tokens drops both unconditionally and the
    # card renders recurrence from corpus_relations(), which is MIW's own
    # chronological model. There is nothing left here to gate.
    content_publish = publish or deliver or promo
    d = spec
    pid = d['paper_id']
    qs = d['questions']
    built = [q for q in qs if q.get('model_answer')]

    title = ('%s %s &mdash; MEO Class I Written Questions & Answers | Marine Intelligence Weekly'
             % (d['subject'], d['month_year']))
    desc = ('All %d questions from the %s MEO Class I %s written paper (%s), with model written '
            'answers, study guides and quick revision.'
            % (len(qs), d['month_year'], d['subject'], d['sr_no']))

    o = []
    a = o.append

    extra = []
    ld = {'@context': 'https://schema.org', '@type': 'LearningResource',
          'name': '%s %s -- MEO Class I Written Questions and Answers' % (d['subject'], d['month_year']),
          'description': strip_tags(desc),
          'educationalLevel': 'MEO Class I (Marine Engineer Officer, Management Level)',
          'learningResourceType': 'Past examination paper with model answers',
          'inLanguage': 'en',
          'about': sorted({t for q in qs for t in (q.get('subject_tags') or [])}),
          'isPartOf': {'@type': 'Collection', 'name': 'MIW MEO Class I Written Questions & Answers',
                       'url': '%s/meoclass1/pastpapers/' % BASE},
          'version': d['version']}
    if publish:
        ld['url'] = '%s/meoclass1/pastpapers/%s.html' % (BASE, pid)
        # Honest representation: an ordered list of the actual exam questions, each
        # carrying a real short answer. Not FAQPage -- these are examination
        # questions with model answers, not frequently asked questions.
        ld['hasPart'] = [{
            '@type': 'Question',
            'position': i + 1,
            'name': strip_tags(q['text_verbatim']),
            'url': '%s/meoclass1/pastpapers/%s.html#%s' % (BASE, pid, q['anchor']),
            'answerCount': 1,
            'acceptedAnswer': {'@type': 'Answer',
                               'text': strip_tags((q.get('quick_revision') or {}).get('recall_15s', ''))},
        } for i, q in enumerate(built) if (q.get('quick_revision') or {}).get('recall_15s')]
        extra.append('<script type="application/ld+json">')
        extra.append(json.dumps(ld, indent=2, ensure_ascii=False))
        extra.append('</script>')
        extra.append('<script type="application/ld+json">')
        extra.append(json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Marine Intelligence Weekly', 'item': BASE},
                {'@type': 'ListItem', 'position': 2, 'name': 'MEO Class I', 'item': '%s/meoclass1/' % BASE},
                {'@type': 'ListItem', 'position': 3, 'name': 'Written Questions & Answers',
                 'item': '%s/meoclass1/pastpapers/' % BASE},
                {'@type': 'ListItem', 'position': 4, 'name': '%s %s' % (d['subject'], d['month_year'])},
            ]}, indent=2, ensure_ascii=False))
        extra.append('</script>')

    if deliver:
        canonical = '/solvedQP/%s.html' % pid
    elif promo:
        canonical = '/meoclass1/oralnotes/%s.html' % PROMO_SLUG
    else:
        canonical = '/meoclass1/pastpapers/%s.html' % pid
    o.extend(head_meta(strip_tags(title), strip_tags(desc), canonical, publish, extra))
    a('<style>')
    a(read_css())
    a('</style>')
    a('</head>')
    a('')
    # data-paper-id lets the corpus fallback exclude the paper the reader is
    # already looking at, without parsing it back out of the URL.
    a('<body data-paper-id="%s">' % esc_attr(pid))
    a(GATE if gated else GATE_STUB)
    a('<a class="skip" href="#paper-main">Skip to questions</a>')
    a('')
    # A delivered paper navigates within /solvedQP/ only, and its year link
    # points at its OWN year's sheet.
    # Navigation follows the ENTITLEMENT that opens the page, never the product
    # the content belongs to. The promo is Written content opened by ORAL, so it
    # takes storefront links; the default Written set would bounce its reader
    # into SOLVED_QP, which is the very thing the page is asking them to buy.
    if deliver:
        nav_active, nav_links = 'Solved QP', delivery_links(year=d['year'])
    elif promo:
        nav_active, nav_links = '', promo_links()
    else:
        nav_active, nav_links = 'Written Questions', None
    o.extend(topbar(nav_active, links=nav_links))
    a('')
    a('<header class="page-header">')
    a('  <div class="wrap">')
    a('    <span class="badge">Written Questions &amp; Answers &middot; %s</span>' % esc(d['sr_no']))
    a('    <h1>%s &mdash; %s</h1>' % (esc(d['subject']), esc(d['month_year'])))
    a('    <p class="sub">%s &middot; Function: %s &middot; %s</p>'
      % (esc(d['printed_authority']), esc(d['function']), esc(d['class'])))
    a('    <div class="header-meta">')
    a('      <span>Sr. No. %s</span>' % esc(d['sr_no']))
    a('      <span>%s</span>' % esc(d['time_allowed']))
    a('      <span>Total marks %s</span>' % esc(d['total_marks']))
    a('      <span>%d questions &middot; answer six</span>' % len(qs))
    a('      <span>%s</span>' % esc(d.get('region_note', '')))
    a('    </div>')
    a('  </div>')
    a('</header>')
    a('')

    if promo:
        o.extend(promo_header())
        a('')

    if not content_publish:
        a('<div class="review-banner">')
        a('  <strong>Founder review copy &mdash; ungated, uncommitted, not published.</strong> '
          'Generated from <code>specs/%s.json</code> by the Past Papers toolchain. '
          'Build state <strong>%s</strong>, review state <strong>%s</strong>, version %s, '
          'updated %s. Production metadata is shown per question in this build only.'
          % (pid, esc(d['build_state']), esc(d['review_state']), esc(d['version']), esc(d['updated'])))
        a('</div>')

    # controls
    a('<div class="controls-bar">')
    a('  <div class="controls-inner">')
    a('    <label class="search-wrap">')
    a('      <span class="visually-hidden-label" aria-hidden="true">&#128269;</span>')
    a('      <input id="search-input" type="search" autocomplete="off" '
      'placeholder="Search questions, topics, regulations &mdash; e.g. general average, SOPEP, ammonia" '
      'aria-label="Search questions in this paper">')
    a('      <button id="search-clear" class="icon-btn" type="button" aria-label="Clear search">&times;</button>')
    a('    </label>')
    for key, label in [('all', 'All'), ('bookmarked', 'Bookmarked'),
                       ('unstudied', 'Not studied'), ('studied', 'Studied')]:
        a('    <button class="filter-btn" type="button" data-filter="%s" aria-pressed="%s">%s</button>'
          % (key, 'true' if key == 'all' else 'false', label))
    for s in sorted({t for q in qs for t in (q.get('subject_tags') or [])}):
        a('    <button class="filter-btn" type="button" data-filter="%s" aria-pressed="false">%s</button>'
          % (esc_attr(s.lower()), esc(s)))
    a('    <button id="reset-progress" class="filter-btn" type="button">Clear my progress</button>')
    a('    <span class="count-label" id="count-label" role="status" aria-live="polite"></span>')
    a('  </div>')
    a('</div>')
    a('')

    a('<div class="main-layout">')
    a('<nav class="sidebar" aria-label="Question index">')
    a('  <h2>Questions</h2>')
    a('  <div class="toc-list">')
    for q in qs:
        a('    <a class="toc-link" href="#%s" data-qid="%s"><span class="tn">%s</span>'
          '<span class="tt">%s</span></a>'
          % (q['anchor'], esc_attr(q['question_id']), esc(q['q_no']),
             esc(q.get('short_title', ''))))
    a('    <a class="toc-link" href="#rapid-revision"><span class="tn">&#9733;</span>'
      '<span class="tt">Rapid revision</span></a>')
    a('  </div>')
    a('</nav>')
    a('')
    a('<main id="paper-main">')
    a('<p id="ls-warning" class="rec-note" hidden>Your browser is blocking local storage, so '
      'bookmarks and studied marks will not be saved. Everything else works normally.</p>')

    a('<section aria-label="Examination instructions" class="reg-ref-box">')
    a('  <div class="rrb-title">Examination instructions, as printed</div>')
    a('  <ul>')
    for i in d['instructions']:
        a('    <li>%s</li>' % esc(i))
    a('  </ul>')
    a('  <p class="rec-note">%s</p>' % esc(d.get('marks_note', '')))
    a('</section>')
    a('')

    # Loaded once for the whole paper: the family model is a property of the
    # corpus, so recomputing it per card would be nine identical passes.
    corpus = corpus_relations()
    # Which papers actually exist on the delivery surface, so a cross-link is
    # only kept when its target is really there.
    delivered_ids = None
    if deliver:
        delivered_ids = {s['paper_id'] for s in load_all_specs() if not is_intake(s)}
    for q in qs:
        build_card(q, d, o, content_publish, corpus,
                   deliver=deliver, delivered_ids=delivered_ids, promo=promo)
        a('')

    a('<div id="no-results">No question matches that search. Try a topic, a regulation '
      'or a question number &mdash; for example <b>general average</b>, <b>MARPOL Annex VI</b> or <b>Q5</b>.</div>')

    # The corpus escape hatch. A paper search is correctly scoped to its own
    # nine questions -- and on its own it tells a reader who typed "port state
    # control" into QP2607 that nothing matches, when 23 questions across 18
    # sittings do. The fallback answers the question the reader actually asked.
    #
    # Delivery only: the manifest it reads lives at /solvedQP/, and a review
    # copy under /meoclass1/pastpapers/ must not link a reviewer into the paid
    # delivery surface (nor 404 against a manifest that is not its own).
    if deliver:
        o.extend(corpus_fallback_block('this paper'))

    # ---- paper-level rapid revision -------------------------------------
    a('<section class="cheat" id="rapid-revision">')
    a('  <h2>%s rapid revision</h2>' % esc(d['month_year']))
    a('  <p class="lead">Every question in one pass. Generated from each question\'s Quick Revision '
      'block &mdash; open the full answer from the question number.</p>')
    a('  <table class="rapid">')
    a('    <thead><tr><th>Q</th><th>Topic</th><th>Answer route</th>'
      '<th>Critical rule / number</th><th>Major trap</th></tr></thead>')
    a('    <tbody>')
    for q in built:
        qr = q.get('quick_revision') or {}
        # The route comes from answer_route, exactly as it does in the plan, the
        # map and the recall test. There is only one route in the system.
        skel = ' &rarr; '.join(esc(s['title']) for s in route_steps(q))
        crit = esc(qr.get('critical_regulation', ''))
        nums = (qr.get('critical_numbers') or [])
        if nums:
            crit += '<br><span class="rec-note">%s</span>' % esc(nums[0])
        a('      <tr>')
        a('        <td data-l="Question"><a href="#%s">%s</a></td>' % (q['anchor'], esc(q['q_no'])))
        a('        <td data-l="Topic">%s<br><span class="rec-note">%s marks</span></td>'
          % (esc(q.get('short_title', '')), q['total_marks']))
        a('        <td data-l="Answer route">%s</td>' % skel)
        a('        <td data-l="Critical rule">%s</td>' % crit)
        a('        <td data-l="Major trap">%s</td>' % esc(qr.get('major_trap', '')))
        a('      </tr>')
    a('    </tbody>')
    a('  </table>')
    a('</section>')

    if promo:
        o.extend(promo_footer(newest_label))

    a('<div class="q-footer">')
    a('  <span class="correction-link">Correction? <a href="mailto:%s?subject=Past%%20Paper%%20%s%%2C%%20Correction%%20Required">%s</a></span>'
      % (CONTACT, pid, CONTACT))
    # 'UNGATED REVIEW COPY' is production's own word for a build nobody has paid
    # for. On the promo it faced a paying Oral subscriber and told them the
    # complete paper they were reading was an internal draft -- the opposite of
    # what the page is for. Every customer-facing build now names the PRODUCT.
    if deliver:
        build_label = 'SOLVED QP'
    elif promo:
        build_label = 'WRITTEN SAMPLE'
    elif gated:
        build_label = 'GATED'
    else:
        build_label = 'UNGATED REVIEW COPY'
    a('  <span class="q-version">Written Questions &middot; %s &middot; v%s &middot; %s</span>'
      % (pid, esc(d['version']), build_label))
    a('</div>')
    a('</main>')
    a('</div>')
    a('')
    o.extend(footer(content_publish))
    a('')
    js = open(os.path.join(TPL, 'paper.js'), encoding='utf-8').read()
    js = (js.replace('__LS_BOOKMARKS__', LS_BOOKMARKS)
            .replace('__LS_PROGRESS__', LS_PROGRESS)
            .replace('__LS_MIGRATE__', LS_MIGRATE_JS)
            # Only the delivered copy renders the corpus panel (see the
            # `if deliver:` above), and paper.js reads the corpus solely from
            # inside that panel's code path. Inlining the reader everywhere
            # else shipped a /solvedQP/ manifest URL into pages whose readers
            # do not own SOLVED_QP -- inert, because nothing ever called it,
            # but a cross-product dependency that LOOKS live is one refactor
            # away from becoming live. The panel and its reader now appear and
            # disappear together, so they cannot drift apart.
            .replace('__CORPUS_SEARCH__',
                     CORPUS_SEARCH_JS if deliver else CORPUS_SEARCH_ABSENT)
            .replace('__STICKY_SYNC__', STICKY_SYNC_JS))
    a('<script>')
    a(js.rstrip('\n'))
    a('</script>')
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('-o', '--out')
    ap.add_argument('--gated', action='store_true')
    ap.add_argument('--publish', action='store_true')
    ap.add_argument('--deliver', action='store_true',
                    help='paid customer copy for /solvedQP/ (noindex, no JSON-LD, '
                         'no production metadata, Solved QP navigation)')
    ap.add_argument('--oral-promo', action='store_true',
                    help='complete Written paper shown to existing ORAL subscribers '
                         'inside /meoclass1/oralnotes/, with purchase CTAs')
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding='utf-8'))

    # An intake spec has questions but no answers, so there is no paper page to
    # build. Refusing here -- rather than rendering a page of empty answer cards
    # -- is what stops a transcription from ever looking like a product. Exit 0:
    # this is the correct outcome for such a spec, not a failure.
    if is_intake(spec):
        print('SKIP %s: intake spec, no answers authored yet. Its questions '
              'render on questions-%d.html; a paper page is built once the '
              'first answer exists.' % (spec['paper_id'], spec['year']))
        return

    # The promo's closing CTA names the newest solved sitting. Derive it from
    # the specs so it moves on its own as papers are added, rather than
    # becoming a stale claim in hand-written copy.
    newest_label = None
    if args.oral_promo:
        solved = [s for s in load_all_specs() if not is_intake(s)]
        if solved:
            solved.sort(key=lambda s: (s['year'], RM.MONTH_NUM[s['month']]))
            newest_label = solved[-1]['month_year']

    html = build(spec, gated=args.gated, publish=args.publish, deliver=args.deliver,
                 promo=args.oral_promo, newest_label=newest_label)

    if args.out:
        out = args.out
    elif args.oral_promo:
        out = os.path.join(REPO_ROOT, 'meoclass1', 'oralnotes', '%s.html' % PROMO_SLUG)
    elif args.deliver:
        out = os.path.join(REPO_ROOT, 'solvedQP', '%s.html' % spec['paper_id'])
    else:
        out = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers',
                           '%s.html' % spec['paper_id'])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    prev = open(out, encoding='utf-8', newline='').read() if os.path.exists(out) else None
    with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(html)

    try:
        rel = os.path.relpath(out, REPO_ROOT).replace('\\', '/')
    except ValueError:
        # -o may point at another drive (Windows). Not an error; just report it whole.
        rel = out.replace('\\', '/')
    n = sum(1 for q in spec['questions'] if q.get('model_answer'))
    print('built %s' % rel)
    print('  %d bytes, %d questions, %d with answers'
          % (len(html.encode('utf-8')), len(spec['questions']), n))
    print('  mode: %s, gate: %s'
          % ('PUBLISH' if args.publish
             else ('SOLVED QP delivery (noindex)' if args.deliver
                   else ('Oral Written sample (noindex)' if args.oral_promo
                         else 'review (noindex)')),
             'PRESENT' if args.gated else 'stripped'))
    if prev is not None:
        print('  rebuild: %s' % ('IDENTICAL to previous output' if prev == html else 'CHANGED'))


if __name__ == '__main__':
    main()
