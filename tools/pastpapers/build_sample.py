#!/usr/bin/env python3
"""Generate the free Solved QP conversion sample from a projection config.

    specs/QP2601.json  +  sample/QP2601.sample.json  -->  SQ/<output>.html
         (canonical)            (projection)                (public artefact)

Three properties, in order of importance.

1. THE SAMPLE IS NEVER A SECOND ANSWER TRUTH. The full-demo questions are
   rendered by importing build_paper's own view functions -- understand_view,
   plan_view, render_blocks, recall_view, quick_revision. There is no forked
   copy of any answer, so a correction to specs/QP2601.json reaches the sample
   on the next build and cannot be missed.

2. WITHHELD CONTENT IS NEVER SHIPPED. For a preview question the generator does
   not render-then-hide; it never emits the model answer, study guide, cards,
   quick revision or route points at all. Opening View Source on the published
   page recovers two complete answers, which is what was given away on purpose,
   and nothing else. sample_check.py proves this against the shipped bytes.

3. A FULL DEMO MAY NOT UNLOCK A PAID PAPER. Six of January's nine questions are
   the earliest sitting of a family that returns later in 2026 -- publishing one
   in full publishes its February, March, April or July twin as well, and one of
   them reaches the July paper the storefront exists to sell. The build FAILS if
   a configured demo question has relatives.
"""
import argparse
import glob
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, BASE, CONTACT, esc, esc_attr, strip_tags,
                           read_css, head_meta)
from build_paper import (understand_view, plan_view, recall_view, quick_revision,
                         render_blocks, route_steps, CHEV)
import recurrence_model as RM

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SAMPLE_GLOB = os.path.join(PP_DIR, 'sample', '*.sample.json')

# Storefront palette, taken from the live SQ/index.html so the sample reads as
# part of the shop rather than as a stray page: teal #0d9488, slate #0f172a.
SAMPLE_CSS = """
.sq-lock{margin:14px 0 4px;padding:16px 18px;border:1.5px solid #99f6e4;border-radius:12px;
  background:linear-gradient(180deg,#f0fdfa,#ffffff)}
.sq-lock-t{font-size:14px;font-weight:700;color:#0f766e;margin:0 0 4px}
.sq-lock-d{font-size:13px;color:#475569;line-height:1.55;margin:0 0 12px}
.sq-lock-d b{color:#0f172a}
.sq-cta{display:inline-block;background:#0d9488;color:#fff;text-decoration:none;
  padding:10px 20px;border-radius:8px;font-size:13px;font-weight:700}
.sq-cta:hover{background:#0f766e}
/* HOW-TO-USE block in the header */
.sq-how{max-width:900px;margin:20px auto 0;text-align:left;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:16px 18px}
.sq-how-t{color:#fff;font-size:12.5px;font-weight:800;text-transform:uppercase;
  letter-spacing:.05em;margin-bottom:6px}
.sq-how-lead{color:#cbd5e1;font-size:12.5px;line-height:1.6;margin:0 0 12px}
.sq-how-modes{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:10px}
.sq-how-modes>div{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10);
  border-radius:8px;padding:10px 12px}
.sq-how-modes b{display:block;color:#5eead4;font-size:12px;font-weight:800;margin-bottom:3px}
.sq-how-modes span{color:#cbd5e1;font-size:11.5px;line-height:1.5}
/* mid-page conversion strip */
.sq-mid{margin:26px 0;padding:18px 20px;border-radius:12px;
  background:linear-gradient(135deg,#0f2f2b,#134e4a);display:flex;align-items:center;
  justify-content:space-between;gap:16px;flex-wrap:wrap}
.sq-mid-t{color:#fff;font-size:14px;font-weight:800;margin:0 0 4px}
.sq-mid-d{color:#94a3b8;font-size:12.5px;margin:0;line-height:1.55}
.sq-demo-flag{display:inline-block;background:#16a34a;color:#fff;font-size:11px;
  font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.03em}
.sq-preview-flag{display:inline-block;background:#f1f5f9;color:#475569;font-size:11px;
  font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.03em}
.sq-depth{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.sq-depth span{font-size:11px;background:#f1f5f9;color:#475569;padding:3px 9px;border-radius:4px}
.sq-offer{max-width:1000px;margin:28px auto;padding:22px;border:2px solid #0d9488;
  border-radius:14px;background:#fff}
.sq-offer h2{margin:0 0 6px;font-size:1.15rem;color:#0f172a}
.sq-offer p{font-size:14px;color:#475569;line-height:1.6;margin:0 0 12px}
.sq-months{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.sq-months b{font-size:12px;background:#f0fdfa;color:#0f766e;border:1px solid #99f6e4;
  padding:4px 10px;border-radius:6px;font-weight:600}
.sq-newest{background:#0d9488 !important;color:#fff !important;border-color:#0d9488 !important}
"""


def load_specs():
    return [json.load(open(p, encoding='utf-8'))
            for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]


def newest_solved(specs):
    """The most recent sitting that actually has answers.

    Derived, never written down. The storefront says "newest solved paper:
    July 2026" today and will say August 2026 the day an August spec lands,
    with no edit anywhere. A hand-written 'latest' would be a lie on a
    schedule.
    """
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
    return max(solved, key=lambda d: (d['year'], RM.MONTH_NUM[d['month']])) if solved else None


def _depth_summary(q):
    steps = route_steps(q)
    points = sum(len(s.get('points') or []) for s in steps)
    cards = len(q.get('retrieval_cards') or [])
    return steps, points, cards


def _demo_card(q, paper, rel, out):
    """A full-demo question: the complete five-mode experience, unmodified.

    Deliberately NOT build_paper.build_card(). That function also emits the
    review-only production metadata block and the source copy's own recurrence
    table -- a third party's analysis that policy classes discovery-only and
    that the 2026 set proved wrong in both directions. Neither belongs on a
    public marketing page. Everything a learner actually sees is rendered by
    the imported view functions, so the answer itself cannot drift.
    """
    out.append('<article class="q-card" id="%s" data-qid="%s" data-demo="full">'
               % (q['anchor'], esc_attr(q['question_id'])))
    out.append('  <div class="q-head">')
    out.append('    <button class="q-toggle" type="button" aria-expanded="false" '
               'aria-controls="%s-body">' % esc_attr(q['anchor']))
    out.append('      <span class="q-num">%s</span>' % esc(q['q_no']))
    out.append('      <span class="q-main">')
    out.append('        <span class="q-title">%s <span class="sq-demo-flag">Complete worked '
               'example</span></span>' % esc(q.get('short_title', q['q_no'])))
    out.append('        <span class="q-meta">%s marks<span class="sep">&middot;</span>%s'
               '<span class="sep">&middot;</span>%s</span>'
               % (q['total_marks'], esc(paper['month_year']),
                  esc(q.get('primary_category', ''))))
    for line in q['text_verbatim'].split('\n'):
        out.append('        <span class="q-stem">%s</span>' % esc(line))
    for sp in (q.get('subparts') or []):
        out.append('        <span class="q-stem">%s %s%s</span>'
                   % (esc(sp.get('label') or sp.get('ref') or ''), esc(sp.get('text', '')),
                      ' <b>(%s)</b>' % sp['marks'] if sp.get('marks') else ''))
    out.append('        <span class="q-tags">')
    for t in (q.get('subject_tags') or []):
        out.append('          <span class="q-tag">%s</span>' % esc(t))
    out.append('        </span>')
    out.append('      </span>')
    out.append('      %s' % CHEV)
    out.append('    </button>')
    out.append('  </div>')

    out.append('  <div class="q-body" id="%s-body" hidden>' % esc_attr(q['anchor']))
    # learn bar, written here rather than imported because build_paper's version
    # is keyed to the paper page's markup contract; the five modes and their
    # order are the frozen V1 template and are reproduced exactly.
    out.append('  <div class="learn-bar" role="tablist" aria-label="How to study this question">')
    for mode, label in (('understand', 'Understand'), ('plan', 'Exam plan'),
                        ('answer', 'Answer'), ('guide', 'Study guide'), ('recall', 'Recall')):
        out.append('    <button class="learn-btn" type="button" role="tab" data-mode="%s" '
                   'aria-selected="%s">%s</button>'
                   % (mode, 'true' if mode == 'answer' else 'false', label))
    out.append('  </div>')

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
    out.append('  </div>')
    out.append('</article>')


def _preview_card(q, paper, cfg, nodes, relations, out):
    """A preview question: printed question, orientation, route TITLES, lock.

    Everything withheld is withheld by not being emitted. There is no hidden
    div, no data- attribute, no JSON island and no comment carrying the answer.
    """
    shown = int(cfg['preview_contract'].get('route_titles_shown', 3))
    steps, points, cards = _depth_summary(q)

    out.append('<article class="q-card" id="%s" data-qid="%s" data-demo="preview">'
               % (q['anchor'], esc_attr(q['question_id'])))
    out.append('  <div class="q-head">')
    out.append('    <button class="q-toggle" type="button" aria-expanded="false" '
               'aria-controls="%s-body">' % esc_attr(q['anchor']))
    out.append('      <span class="q-num">%s</span>' % esc(q['q_no']))
    out.append('      <span class="q-main">')
    out.append('        <span class="q-title">%s <span class="sq-preview-flag">Preview</span></span>'
               % esc(q.get('short_title', q['q_no'])))
    out.append('        <span class="q-meta">%s marks<span class="sep">&middot;</span>%s'
               '<span class="sep">&middot;</span>%s</span>'
               % (q['total_marks'], esc(paper['month_year']),
                  esc(q.get('primary_category', ''))))
    for line in q['text_verbatim'].split('\n'):
        out.append('        <span class="q-stem">%s</span>' % esc(line))
    for sp in (q.get('subparts') or []):
        out.append('        <span class="q-stem">%s %s%s</span>'
                   % (esc(sp.get('label') or sp.get('ref') or ''), esc(sp.get('text', '')),
                      ' <b>(%s)</b>' % sp['marks'] if sp.get('marks') else ''))
    out.append('        <span class="q-tags">')
    for t in (q.get('subject_tags') or []):
        out.append('          <span class="q-tag">%s</span>' % esc(t))
    out.append('        </span>')
    out.append('      </span>')
    out.append('      %s' % CHEV)
    out.append('    </button>')
    out.append('  </div>')

    out.append('  <div class="q-body" id="%s-body" hidden>' % esc_attr(q['anchor']))
    out.append('    <p class="rec-note">%s</p>'
               % RM.family_summary(nodes, relations, q['question_id']))
    if q.get('understand_first'):
        out.append('    <section class="layer uf" aria-label="Understand this question">')
        out.append('      <div class="layer-title">Understand this question first</div>')
        out.append('      <p>%s</p>' % esc(q['understand_first']))
        out.append('    </section>')
    if steps:
        out.append('    <section class="layer plan" aria-label="Exam plan preview">')
        out.append('      <div class="layer-title">The answer route &mdash; first %d of %d steps</div>'
                   % (min(shown, len(steps)), len(steps)))
        out.append('      <ol class="plan-list">')
        for s in steps[:shown]:
            out.append('        <li class="plan-limb">%s</li>' % esc(s['title']))
        out.append('      </ol>')
        if len(steps) > shown:
            out.append('      <p class="rec-note">&hellip; and %d more step%s, in the order the '
                       'examiner rewards.</p>'
                       % (len(steps) - shown, '' if len(steps) - shown == 1 else 's'))
        out.append('    </section>')
    out.append('    <div class="sq-depth"><span>%d-step route</span><span>%d core points</span>'
               '<span>%d flashcards</span><span>Full study guide</span><span>Recall test</span></div>'
               % (len(steps), points, cards))
    _lock_block(out, cfg,
                'Continue this solved question',
                'The complete <b>model written answer</b>, the <b>study guide</b>, all <b>%d '
                'flashcards</b> and the <b>recall test</b> for this question are part of MIW '
                'Solved QP.' % cards)
    out.append('  </div>')
    out.append('</article>')


def _price_suffix(cfg):
    """" &middot; <price>" once a price is approved, otherwise nothing.

    PRICE_TBD is a deliberate sentinel: the generator refuses to render a
    currency value while it is set, so a placeholder cannot reach a customer by
    accident. Everything that shows a price goes through here so there is one
    place that decision is made.
    """
    p = str(cfg.get('commercial', {}).get('price_display', 'PRICE_TBD')).strip()
    return '' if (not p or p == 'PRICE_TBD') else ' &middot; %s' % esc(p)


def _lock_block(out, cfg, title, detail):
    c = cfg['commercial']
    out.append('    <div class="sq-lock">')
    out.append('      <p class="sq-lock-t">%s</p>' % esc(title))
    out.append('      <p class="sq-lock-d">%s</p>' % detail)
    out.append('      <a class="sq-cta" href="%s">%s &rarr;</a>'
               % (esc_attr(c['cta_href']), esc(c['cta_label'])))
    out.append('    </div>')


def _sample_js():
    """Mode switching, expand/collapse, knowledge map, recall and flashcards.

    Replicates the four behaviours of template/paper.js that the five-mode
    experience depends on. paper.js itself is not reused because it also wires
    bookmarks, progress, per-paper search and a side index that this page does
    not have; loading it here would bind to elements that are absent.
    """
    return """
  var cards = Array.prototype.slice.call(document.querySelectorAll('.q-card'));

  function setOpen(card, open) {
    var btn = card.querySelector('.q-toggle');
    var body = card.querySelector('.q-body');
    if (!btn || !body) return;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    body.hidden = !open;
    card.classList.toggle('open', open);
  }

  function showMode(card, mode) {
    Array.prototype.forEach.call(card.querySelectorAll('.mode'), function (m) {
      m.hidden = m.getAttribute('data-mode') !== mode;
    });
    Array.prototype.forEach.call(card.querySelectorAll('.learn-btn'), function (b) {
      b.setAttribute('aria-selected', b.getAttribute('data-mode') === mode ? 'true' : 'false');
    });
  }

  cards.forEach(function (card) {
    var btn = card.querySelector('.q-toggle');
    if (btn) {
      btn.addEventListener('click', function () {
        setOpen(card, btn.getAttribute('aria-expanded') !== 'true');
      });
    }
    if (card.querySelector('.learn-bar')) {
      showMode(card, 'answer');
      Array.prototype.forEach.call(card.querySelectorAll('.learn-btn'), function (b) {
        b.addEventListener('click', function () { showMode(card, b.getAttribute('data-mode')); });
      });
    }
    // The two worked examples open on arrival: a visitor must not have to
    // discover the product by clicking before anything of value is on screen.
    if (card.getAttribute('data-demo') === 'full') setOpen(card, true);
  });

  Array.prototype.forEach.call(document.querySelectorAll('.kmap-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var map = btn.closest('.kmap');
      var hidden = map.classList.toggle('branches-hidden');
      btn.setAttribute('aria-pressed', hidden ? 'true' : 'false');
      btn.textContent = hidden ? 'Show branches' : 'Hide branches';
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.recall-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var sec = btn.closest('.recall');
      var list = sec.querySelector('.recall-list');
      var show = list.getAttribute('data-state') === 'hidden';
      list.setAttribute('data-state', show ? 'shown' : 'hidden');
      Array.prototype.forEach.call(sec.querySelectorAll('.recall-answer'), function (a) {
        a.hidden = !show;
      });
      Array.prototype.forEach.call(sec.querySelectorAll('.recall-blank'), function (a) {
        a.hidden = show;
      });
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
      btn.textContent = show ? 'Hide the structure' : 'Reveal the structure';
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.card-q'), function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var ans = document.getElementById(btn.getAttribute('aria-controls'));
      if (ans) ans.hidden = !open;
    });
  });

  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('q-card')) setOpen(target, true);
  }
"""


def build_sample(cfg, specs, publish_flag):
    """Render one projection.

    PUBLISH STATE IS A PROPERTY OF THE ARTEFACT, NOT OF THE INVOCATION.

    It used to come only from --publish. That flag lives in the memory of
    whoever last typed the command, so any later rebuild silently reverted a
    published page to a review copy -- and run_toolchain.py calls this script
    with no flags at all. That is exactly how the live January sample came to
    tell customers "Founder review copy -- not published, not indexable" with
    a PRICE_TBD placeholder, on the page the whole funnel pointed at. Nothing
    failed and nothing warned.

    `"publish": true` in the projection config now carries it, so a routine
    rebuild cannot un-publish a live page. --publish still works, as an
    override for a config that has not been switched over yet.
    """
    publish = bool(publish_flag or cfg.get('publish'))
    pid = cfg['paper_id']
    spec = next((d for d in specs if d['paper_id'] == pid), None)
    if spec is None:
        raise SystemExit('ERROR: sample config names %s but no such spec exists' % pid)

    nodes = RM.load_nodes(specs)
    relations = RM.build_families(nodes)

    demo_ids = list(cfg['full_demo_questions'])
    by_no = {q['q_no']: q for q in spec['questions']}

    # ---- the commercial guard -------------------------------------------
    #
    # A full demo normally may NOT belong to a recurrence family, because
    # publishing one member in full publishes its paid twins in later sittings.
    #
    # `allow_family_members` overrides that, and exists for one case only: a
    # build whose output is itself behind an entitlement gate, where the
    # audience is customers who have already paid rather than the open
    # internet. The override must carry a written reason AND name the
    # entitlement protecting the page, and it still prints every question it
    # unlocks, so the cost lands in the build log rather than staying buried in
    # a config file.
    override = bool(cfg.get('allow_family_members'))
    unlocked = []
    for qno in demo_ids:
        if qno not in by_no:
            raise SystemExit('ERROR: %s has no %s' % (pid, qno))
        qid = by_no[qno]['question_id']
        rel = relations[qid]
        if rel['family_size'] > 1:
            if not override:
                raise SystemExit(
                    'ERROR: %s (%s) is a full demo but belongs to a recurrence family with %s.\n'
                    '       Publishing it in full publishes those paid questions too.\n'
                    '       Choose a family singleton, or change this deliberately in the config.'
                    % (qid, by_no[qno].get('short_title', ''), ', '.join(rel['others'])))
            unlocked.extend(rel['others'])

    if override:
        if not cfg.get('allow_family_members_reason'):
            raise SystemExit(
                'ERROR: allow_family_members is set without allow_family_members_reason.\n'
                '       An override that gives away paid content must say why, in the config.')
        if not cfg.get('gated_behind'):
            raise SystemExit(
                'ERROR: allow_family_members is only permitted for a GATED output.\n'
                '       Set gated_behind to the entitlement that protects this page, or drop\n'
                '       the override. A public page must never carry it.')
        if cfg['output'].startswith('SQ/'):
            raise SystemExit(
                'ERROR: %s writes into SQ/, which is outside the middleware matcher and\n'
                '       therefore public. allow_family_members cannot apply to it.'
                % cfg['output'])
        if unlocked:
            print('  !! allow_family_members: this build publishes %d question(s) that also '
                  'appear in paid sittings:' % len(set(unlocked)))
            for other in sorted(set(unlocked)):
                print('       %s' % other)
        print('  !! output is gated behind %s' % cfg['gated_behind'])

    newest = newest_solved(specs)
    solved_papers = sorted(
        [d for d in specs if any(q.get('model_answer') for q in d['questions'])],
        key=lambda d: (d['year'], RM.MONTH_NUM[d['month']]))

    o = []
    a = o.append
    # Title and description describe THIS projection. A gated page is not a
    # "free sample", and the demo count is derived rather than hard-coded --
    # "two questions worked in full" was literal text that would have been
    # wrong the moment a config changed.
    n_demo = len(demo_ids)
    if cfg.get('gated_behind'):
        title = ('Solved MEO Class I written paper &mdash; %s | Marine Intelligence Weekly'
                 % spec['month_year'])
        desc = ('The complete %s MEO Class I Engineering Management written paper, every '
                'question worked in full using the MIW study method.' % spec['month_year'])
    else:
        title = ('Free solved MEO Class I written paper &mdash; %s | Marine Intelligence Weekly'
                 % spec['month_year'])
        desc = ('The complete %s MEO Class I Engineering Management written paper, with %s '
                'worked in full using the MIW study method.'
                % (spec['month_year'],
                   'every question' if n_demo == len(spec['questions'])
                   else '%d questions' % n_demo))
    # A GATED page is never indexable, whatever --publish says. Middleware
    # answers a crawler with a redirect, so "index, follow" would only invite
    # search engines to keep requesting a page they can never read, and to
    # surface the login bounce as if it were the content.
    o.extend(head_meta(strip_tags(title), strip_tags(desc),
                       '/%s' % cfg['output'],
                       publish and not cfg.get('gated_behind')))
    a('<style>')
    a(read_css())
    a(SAMPLE_CSS)
    a('</style>')
    a('</head>')
    a('<body>')
    a('<a class="skip" href="#s-main">Skip to the paper</a>')
    a('<nav class="topbar" aria-label="Primary">')
    a('  <span class="logo">&#9875; MIW</span>')
    a('  <span class="topbar-sub">Solved Written Papers &middot; free sample</span>')
    a('  <span class="topbar-links">')
    a('    <a href="/SQ/index.html">MEO Class I store</a>')
    a('    <a href="%s">Get full access%s</a>'
      % (esc_attr(cfg['commercial']['cta_href']), _price_suffix(cfg)))
    a('  </span>')
    a('</nav>')

    gated = cfg.get('gated_behind')
    every = len(demo_ids) == len(spec['questions'])

    a('<header class="page-header"><div class="wrap">')
    # A page behind an entitlement is not a "free sample" to the person reading
    # it -- they have already paid for the product that opens it. Calling it one
    # reads as a downgrade of what they bought.
    a('  <span class="badge">%s &middot; %s</span>'
      % ('Included with your Oral access' if gated else 'Free sample',
         esc(spec['month_year'])))
    a('  <h1>%s &mdash; %s</h1>' % (esc(spec['subject']), esc(spec['month_year'])))
    if every:
        a('  <p class="sub">This is a complete examination sitting: all %d questions exactly as '
          'printed, and <b>every one worked in full</b> &mdash; Understand, Exam plan, Answer, '
          'Study guide, Recall.</p>' % len(spec['questions']))
    else:
        a('  <p class="sub">This is a complete examination sitting: all %d questions exactly as '
          'printed. <b>%s and %s are worked in full</b>, so you can see the whole MIW method '
          '&mdash; Understand, Exam plan, Answer, Study guide, Recall. The remaining questions '
          'show how each one is structured.</p>'
          % (len(spec['questions']), demo_ids[0], demo_ids[-1]))
    a('  <div class="header-meta"><span>%s</span><span>%s</span><span>%d questions &middot; '
      'answer six</span><span>%d worked in full</span></div>'
      % (esc(spec['class']), esc(spec['time_allowed']), len(spec['questions']), len(demo_ids)))

    # HOW TO USE THIS PAGE. The five modes are the product; a reader who does
    # not know what they are cannot tell a worked answer from a long one. This
    # is the same copy as the "How every question is worked" section on
    # solvedQP/index.html -- if one changes, change both.
    a('  <div class="sq-how">')
    a('    <div class="sq-how-t">How every question is worked</div>')
    a('    <p class="sq-how-lead">The same five modes on every question, in the same order. '
      'The route through an answer is written once and reused by the plan, the guide and '
      'the recall.</p>')
    a('    <div class="sq-how-modes">')
    for label, blurb in (
            ('Understand', 'What the examiner is actually asking, and the trap in the wording.'),
            ('Exam plan', 'How to spend the marks &mdash; the shape of the answer before you write it.'),
            ('Answer', 'The full model written answer, regulation-referenced.'),
            ('Study guide', 'The background you need if the topic is not yet solid.'),
            ('Recall', 'Fifteen-second revision &mdash; route, critical number, major trap.')):
        a('      <div><b>%s</b><span>%s</span></div>' % (label, blurb))
    a('    </div>')
    a('  </div>')
    a('</div></header>')
    if not publish:
        a('<div class="review-banner"><strong>Founder review copy &mdash; not published, not '
          'indexable.</strong> Generated by <code>tools/pastpapers/build_sample.py</code> from '
          '<code>specs/%s.json</code> and <code>sample/%s.sample.json</code>. '
          'Pricing is <code>%s</code>; no currency value is rendered.</div>'
          % (pid, pid, esc(cfg['commercial']['price_display'])))

    a('<main id="s-main" style="max-width:1000px;margin:0 auto;padding:20px;">')
    a('<section aria-label="Examination instructions" class="reg-ref-box">')
    a('  <div class="rrb-title">Examination instructions, as printed</div>')
    a('  <ul>')
    for i in spec['instructions']:
        a('    <li>%s</li>' % esc(i))
    a('  </ul>')
    a('  <p class="rec-note">%s</p>' % esc(spec.get('marks_note', '')))
    a('</section>')

    # A mid-page conversion strip, placed once, roughly a third of the way in.
    # It goes AFTER a question rather than before one, so a reader always meets
    # real worked content before an offer; leading with the offer is what makes
    # a sample feel like an advert. Suppressed for a gated build, where the
    # reader already holds the entitlement being sold.
    mid_at = max(1, len(spec['questions']) // 3)
    for idx, q in enumerate(spec['questions'], start=1):
        if q['q_no'] in demo_ids:
            _demo_card(q, spec, relations, o)
        else:
            _preview_card(q, spec, cfg, nodes, relations, o)
        a('')
        if idx == mid_at and not cfg.get('gated_behind'):
            a('<div class="sq-mid">')
            a('  <div>')
            a('    <p class="sq-mid-t">Every sitting, worked exactly like this</p>')
            a('    <p class="sq-mid-d">%d solved papers &middot; %d questions &middot; '
              'all five modes on every one%s</p>'
              % (len(solved_papers), sum(len(d['questions']) for d in solved_papers),
                 _price_suffix(cfg)))
            a('  </div>')
            a('  <a class="sq-cta" href="%s">%s &rarr;</a>'
              % (esc_attr(cfg['commercial']['cta_href']),
                 esc(cfg['commercial']['cta_label'])))
            a('</div>')

    # ---- paper-level offer ----------------------------------------------
    # The year label is DERIVED, not hard-coded. It read "2026" while every
    # solved paper was from 2026; the first 2025 paper to be solved made that
    # heading false while listing the 2025 sitting immediately beneath it.
    # "every N sitting" was also ungrammatical for every N.
    yrs = sorted({d['year'] for d in solved_papers})
    span = str(yrs[0]) if len(yrs) == 1 else '%d&ndash;%d' % (yrs[0], yrs[-1])
    a('<section class="sq-offer" id="unlock">')
    a('  <h2>The complete %s solved paper set</h2>' % span)
    a('  <p>January is your free sample. MIW Solved QP covers all %d sitting%s we have solved, '
      'each question with the same five-mode treatment you have just used.</p>'
      % (len(solved_papers), '' if len(solved_papers) == 1 else 's'))
    a('  <div class="sq-months">')
    for d in solved_papers:
        newest_flag = (newest is not None and d['paper_id'] == newest['paper_id'])
        a('    <b%s>%s%s</b>' % (' class="sq-newest"' if newest_flag else '',
                                 esc(d['month_year']),
                                 ' &middot; newest solved paper' if newest_flag else ''))
    a('  </div>')
    if newest is not None:
        a('  <p>The <b>newest solved paper is %s</b>, and it is included with full access. '
          'Every paper MIW solves after that is added to the same library.</p>'
          % esc(newest['month_year']))
    a('  <p class="rec-note">Questions are reproduced for study. Answers are MIW&rsquo;s own work, '
      'written against primary sources and dated to the sitting.</p>')
    _lock_block(o, cfg, 'Unlock the complete solved papers%s' % _price_suffix(cfg),
                'Every solved question: <b>model written answer</b>, <b>exam plan</b>, '
                '<b>knowledge map</b>, <b>study guide</b>, <b>flashcards</b> and <b>recall '
                'test</b>, plus the recurrence intelligence across the whole year.')
    a('</section>')

    a('</main>')
    a('<footer class="page-footer">')
    a('  Marine Intelligence Weekly &mdash; MEO Class I Solved Written Papers '
      '&middot; Compiled by Nixon Antony, 2/E, Maersk A/S<br>')
    a('  Examination questions are reproduced for study purposes. For personal exam-preparation '
      'use. Not for redistribution. Corrections: <a href="mailto:%s">%s</a>' % (CONTACT, CONTACT))
    a('</footer>')
    a('<script>')
    a(_sample_js())
    a('</script>')
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def write(path, text):
    prev = open(path, encoding='utf-8', newline='').read() if os.path.exists(path) else None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true')
    args = ap.parse_args()

    specs = load_specs()
    configs = sorted(glob.glob(SAMPLE_GLOB))
    if not configs:
        print('ERROR: no sample projection config under %s' % SAMPLE_GLOB)
        sys.exit(1)
    for cpath in configs:
        cfg = json.load(open(cpath, encoding='utf-8'))
        out = os.path.join(REPO_ROOT, cfg['output'].replace('/', os.sep))
        st = write(out, build_sample(cfg, specs, args.publish))
        print('%-46s %s' % (cfg['output'], st))


if __name__ == '__main__':
    main()
