#!/usr/bin/env python3
"""Build the Study Topic Map at /solvedQP/topics.html.

    specs/*.json  --(topic_taxonomy)-->  solvedQP/topics.html

The one candidate question this page answers is "what do I have to study?"

    DOMAIN  ->  STUDY TOPIC  ->  SOLVED QUESTIONS  ->  the five learning modes

It is a PROJECTION of the canonical specs, exactly like the product home:
primary_category is the domain, normalised subject_tags are the study topics,
and every count on the page is recomputed here from the solved specs. It is
SOLVED-ONLY by design -- no intelligence-only sitting is read, so the map can
never imply coverage of a paper MIW has not solved.

Fully static HTML. Native <details>/<summary> disclosure, no runtime fetch,
no tree widget: ~85 nodes do not need a payload, and a page that renders with
JavaScript off is a page every candidate can read.

Deliberately NOT shown: recurrence_class, reused_from, adjudication or any
authoring field; no "high priority", likelihood or six-year appearance claim.
A study topic shows three generated facts -- solved question count, sitting
count, latest sitting -- and the questions themselves.

Determinism: no clock read. The generated date is the newest spec `updated`,
the same convention as the delivery manifest.
"""
import argparse, io, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, esc, esc_attr, strip_tags, read_css, topbar,
                           head_meta, footer, GATE_STUB, delivery_links,
                           STICKY_SYNC_JS)
import recurrence_model as RM
import topic_taxonomy as TT
# Solved-state and spec loading are defined ONCE, by the home builder.
from build_solvedqp_home import load_specs, solved_sittings, write, MODES

OUT_REL = os.path.join('solvedQP', 'topics.html')
NAV_LABEL = 'What should I study?'

CSS = """
  .sq-hero{background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:2.3rem 0 1.8rem;}
  .sq-hero .wrap{max-width:900px;margin:0 auto;padding:0 1.25rem;}
  .sq-hero h1{color:#fff;font-size:1.9rem;line-height:1.25;margin:.35rem 0 .5rem;}
  .sq-hero .sub{color:#94a3b8;font-size:.95rem;margin:0 0 1rem;max-width:62ch;line-height:1.6;}
  .sq-badge{display:inline-block;background:rgba(13,148,136,.18);color:#5eead4;border:1px solid rgba(13,148,136,.4);
    border-radius:999px;padding:.15rem .7rem;font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;}
  .sq-stats{display:flex;flex-wrap:wrap;gap:1.2rem 1.5rem;margin-top:1.1rem;}
  .sq-stats b{display:block;color:#fff;font-size:1.35rem;line-height:1.1;}
  .sq-stats span{color:#94a3b8;font-size:.78rem;}
  .tm-scope{color:#cbd5e1;font-size:.86rem;margin:1rem 0 0;max-width:70ch;line-height:1.55;}

  .tm-wrap{max-width:900px;margin:0 auto;padding:1.4rem 1.25rem 2.5rem;}
  .tm-how{margin:0 0 1.2rem;padding:.9rem 1.1rem;border:1px solid var(--grey-border);border-radius:10px;
    background:#fff;font-size:.86rem;line-height:1.6;color:var(--grey-text);}
  .tm-how ol{margin:.35rem 0 0 1.1rem;padding:0;}
  .tm-how li{margin:.15rem 0;}
  .tm-how b{color:var(--navy);}
  .tm-note{font-size:.8rem;color:var(--grey-text);margin:0 0 1rem;line-height:1.55;}

  /* Domain: the seven roots. Collapsed by default; a summary is one tap. */
  .tm-dom{border:1px solid var(--grey-border);border-radius:12px;background:#fff;margin:0 0 .8rem;}
  .tm-dom>summary{list-style:none;cursor:pointer;padding:.9rem 1.1rem;min-height:44px;
    display:flex;align-items:flex-start;gap:.7rem;}
  .tm-dom>summary::-webkit-details-marker{display:none;}
  .tm-dom>summary::before{content:'';flex:0 0 auto;width:.55rem;height:.55rem;margin-top:.5rem;
    border-right:2px solid var(--teal-dark);border-bottom:2px solid var(--teal-dark);
    transform:rotate(-45deg);transition:transform .15s;}
  .tm-dom[open]>summary::before{transform:rotate(45deg);}
  .tm-dom>summary:hover,.tm-dom>summary:focus-visible{background:var(--teal-light);border-radius:12px;}
  .tm-dom[open]>summary{border-bottom:1px solid var(--grey-border);border-radius:12px 12px 0 0;}
  .tm-dom h2{margin:0;font-size:1.05rem;line-height:1.3;color:var(--navy);}
  .tm-cnt{display:block;margin-top:.2rem;font-size:.78rem;color:var(--grey-text);line-height:1.5;}
  .tm-cnt b{color:var(--teal-dark);font-weight:700;}
  .tm-body{padding:.4rem .6rem .8rem;}
  .tm-topics{list-style:none;margin:0;padding:0;}
  .tm-topics>li{border-bottom:1px dashed var(--grey-border);}
  .tm-topics>li:last-child{border-bottom:0;}

  /* Study topic: one disclosure per topic, its questions inside. */
  .tm-topic>summary{list-style:none;cursor:pointer;padding:.65rem .5rem;min-height:44px;
    display:flex;align-items:flex-start;gap:.6rem;}
  .tm-topic>summary::-webkit-details-marker{display:none;}
  .tm-topic>summary::before{content:'';flex:0 0 auto;width:.45rem;height:.45rem;margin-top:.45rem;
    border-right:2px solid var(--grey-text);border-bottom:2px solid var(--grey-text);transform:rotate(-45deg);}
  .tm-topic[open]>summary::before{transform:rotate(45deg);}
  .tm-topic>summary:hover,.tm-topic>summary:focus-visible{background:#f8fafc;}
  .tm-topic h3{margin:0;font-size:.95rem;line-height:1.35;color:var(--navy);font-weight:700;}
  .tm-topic.tm-other h3{font-weight:600;color:var(--grey-text);}
  .tm-tbody{padding:.2rem .5rem .8rem 1.55rem;}
  .tm-also{margin:0 0 .5rem;font-size:.8rem;color:var(--grey-text);line-height:1.5;}
  .tm-also b{color:var(--navy);font-weight:600;}
  .tm-qs{list-style:none;margin:0;padding:0;}
  .tm-qs li{margin:0;border-top:1px dashed var(--grey-border);}
  .tm-qs li:first-child{border-top:0;}
  .tm-qs a{display:flex;flex-wrap:wrap;align-items:baseline;gap:.15rem .6rem;padding:.5rem 0;
    min-height:44px;color:inherit;text-decoration:none;font-size:.86rem;line-height:1.5;}
  .tm-qs a:hover .tm-title,.tm-qs a:focus-visible .tm-title{color:var(--teal);text-decoration:underline;}
  .tm-sit{flex:0 0 auto;font-weight:700;color:var(--teal-dark);font-size:.78rem;white-space:nowrap;}
  .tm-title{flex:1 1 16rem;min-width:0;}
  .tm-rec{flex:0 0 auto;font-size:.72rem;color:var(--grey-text);border:1px solid var(--grey-border);
    border-radius:999px;padding:0 .5rem;white-space:nowrap;}
  .tm-go{display:inline-flex;align-items:center;min-height:44px;margin-top:.5rem;padding:.45rem .95rem;
    border-radius:999px;background:var(--teal-dark);color:#fff;font-weight:700;font-size:.82rem;text-decoration:none;}
  .tm-go:hover,.tm-go:focus-visible{background:var(--teal);}
  .tm-go.alt{background:#fff;color:var(--teal-dark);border:1px solid var(--teal);}
  .tm-go.alt:hover,.tm-go.alt:focus-visible{background:var(--teal-light);}
  .tm-modes{margin:1.6rem 0 0;padding:1rem 1.1rem;border:1px solid var(--grey-border);border-radius:10px;background:#fff;}
  .tm-modes h2{margin:0 0 .3rem;font-size:1rem;color:var(--navy);}
  .tm-modes p{margin:0 0 .5rem;font-size:.84rem;color:var(--grey-text);line-height:1.55;}
  .tm-modes ol{margin:0;padding-left:1.15rem;font-size:.84rem;line-height:1.55;}
  .tm-modes li b{color:var(--navy);}
  @media (max-width:640px){
    .sq-hero{padding:1.7rem 0 1.4rem;}
    .sq-hero h1{font-size:1.5rem;}
    .tm-wrap{padding:1rem .9rem 2rem;}
    .tm-dom>summary{padding:.8rem .9rem;}
    .tm-body{padding:.3rem .35rem .6rem;}
    .tm-tbody{padding-left:1.1rem;}
    .tm-sit{flex-basis:100%;}
    .tm-rec{margin-left:0;}
  }
"""


def part_year_note(sittings):
    """'2026 is a part year.' when the newest solved year is not yet complete.

    Rule: the newest solved year is a part year unless its newest solved
    sitting is December. Earlier years are stated as they stand; a month with
    no examination is not a gap in coverage.
    """
    newest = sittings[-1]
    if RM.MONTH_NUM[newest['month']] < 12:
        return '%d is a part year.' % newest['year']
    return ''


def scope_line(sittings, questions):
    first, last = sittings[0], sittings[-1]
    s = ('Built from the %d sittings MIW has solved &mdash; %d questions, %s %d to %s %d. %s'
         % (len(sittings), questions, first['month'], first['year'],
            last['month'], last['year'], part_year_note(sittings))).strip()
    return s


def q_line(qid, meta):
    d, q, label = meta[qid]
    anchor = q.get('anchor') or ('q%s' % str(q['q_no']))
    href = '/solvedQP/%s.html#%s' % (d['paper_id'], anchor)
    qn = q['q_no'] if str(q['q_no']).upper().startswith('Q') else 'Q%s' % q['q_no']
    title = strip_tags(q.get('short_title') or '')
    return ('<li><a href="%s"><span class="tm-sit">%s %d &middot; %s</span>'
            '<span class="tm-title">%s</span><span class="tm-rec">%s</span></a></li>'
            % (href, esc(d['month']), d['year'], esc(qn), esc(title), esc(label)))


def build(specs):
    sittings = solved_sittings(specs)
    tmap = TT.build_topic_map(sittings)
    nodes = RM.load_nodes(specs)
    rel = RM.build_families(nodes)
    meta = {}
    for d in sittings:
        for q in d['questions']:
            qid = q['question_id']
            meta[qid] = (d, q, RM.STATUS_LABEL_PLAIN[rel[qid]['status']])

    n_dom = len(tmap['domains'])
    n_topics = sum(len(x['topics']) for x in tmap['domains'])
    total_q = tmap['questions']

    title = 'What should I study? &mdash; MIW Solved QP study roadmap'
    desc = ('The MEO Class I Engineering Management study roadmap: every domain, the '
            'study topics inside it, and the solved questions behind each one.')

    o = []
    a = o.append
    o.extend(head_meta(strip_tags(title), strip_tags(desc), '/solvedQP/topics.html', False))
    a('<style>')
    a(read_css())
    a(CSS)
    a('</style>')
    a('</head>')
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#tm-main">Skip to the study roadmap</a>')
    years = sorted({d['year'] for d in sittings})
    o.extend(topbar(NAV_LABEL, links=delivery_links(years=years)))

    a('<header class="sq-hero">')
    a('  <div class="wrap">')
    a('    <span class="sq-badge">Written &middot; Study roadmap</span>')
    a('    <h1>What should I study?</h1>')
    a('    <p class="sub">The study roadmap for MEO Class I Engineering Management, drawn from '
      'the papers MIW has solved. Open a domain, pick a study topic, and go straight to the '
      'solved questions behind it &mdash; each one worked through the five learning modes.</p>')
    a('    <div class="sq-stats">')
    a('      <div><b>%d</b><span>domains</span></div>' % n_dom)
    a('      <div><b>%d</b><span>study topics</span></div>' % n_topics)
    a('      <div><b>%d</b><span>solved questions</span></div>' % total_q)
    a('      <div><b>%d</b><span>solved sittings</span></div>' % len(sittings))
    a('    </div>')
    a('    <p class="tm-scope">%s Sittings MIW has not solved are not on this map.</p>'
      % scope_line(sittings, total_q))
    a('  </div>')
    a('</header>')

    a('<main id="tm-main" class="tm-wrap">')
    a('  <div class="tm-how">')
    a('    <b>How to use this page.</b>')
    a('    <ol>')
    a('      <li>Open a <b>domain</b> to see the study topics the examiners have actually set.</li>')
    a('      <li>Open a <b>study topic</b> to see its solved questions, newest sitting first.</li>')
    a('      <li>Open a question, or <b>Study these questions</b> to work the whole set on the '
      'search page.</li>')
    a('    </ol>')
    a('  </div>')
    a('  <p class="tm-note">Each solved question belongs to one domain. Inside a domain a question '
      'may sit under more than one study topic, so topic counts overlap and do not add up to '
      'the domain total.</p>')

    a('  <nav aria-label="Study roadmap by domain">')
    for dom in tmap['domains']:
        dq = len(dom['question_ids'])
        a('  <details class="tm-dom" id="%s">' % esc_attr(_slug(dom['label'])))
        a('    <summary>')
        a('      <div>')
        a('        <h2>%s</h2>' % esc(dom['label']))
        a('        <span class="tm-cnt"><b>%d</b> solved question%s &middot; asked in <b>%d</b> of %d '
          'solved sittings &middot; latest %s &middot; %d study topic%s</span>'
          % (dq, '' if dq == 1 else 's', dom['sitting_count'], len(sittings),
             esc(dom['latest']), len(dom['topics']), '' if len(dom['topics']) == 1 else 's'))
        a('      </div>')
        a('    </summary>')
        a('    <div class="tm-body">')
        a('    <ul class="tm-topics">')
        for t in dom['topics']:
            tq = len(t['question_ids'])
            a('      <li><details class="tm-topic">')
            a('        <summary><div><h3>%s</h3>' % esc(t['label']))
            a('        <span class="tm-cnt"><b>%d</b> solved question%s &middot; asked in <b>%d</b> of %d '
              'solved sittings &middot; latest %s</span></div></summary>'
              % (tq, '' if tq == 1 else 's', t['sitting_count'], len(sittings), esc(t['latest'])))
            a('        <div class="tm-tbody">')
            if t['also_covers']:
                a('        <p class="tm-also"><b>Also covers:</b> %s</p>'
                  % ' &middot; '.join(esc(x) for x in t['also_covers']))
            a('        <ul class="tm-qs">')
            for qid in t['question_ids']:
                a('          ' + q_line(qid, meta))
            a('        </ul>')
            a('        <a class="tm-go" href="%s">Study these %d questions &rarr;</a>'
              % (esc_attr(TT.topic_query(t['label'], dom['label'])), tq))
            a('        </div>')
            a('      </details></li>')
        oth = dom['other']['question_ids']
        if oth:
            a('      <li><details class="tm-topic tm-other">')
            a('        <summary><div><h3>%s</h3>' % esc(dom['other']['label']))
            a('        <span class="tm-cnt"><b>%d</b> solved question%s whose study topic is set '
              'less often in this domain</span></div></summary>' % (len(oth), '' if len(oth) == 1 else 's'))
            a('        <div class="tm-tbody">')
            a('        <ul class="tm-qs">')
            for qid in oth:
                a('          ' + q_line(qid, meta))
            a('        </ul>')
            a('        <a class="tm-go alt" href="%s">All %d questions in this domain &rarr;</a>'
              % (esc_attr(TT.domain_query(dom['label'])), dq))
            a('        </div>')
            a('      </details></li>')
        a('    </ul>')
        a('    </div>')
        a('  </details>')
    a('  </nav>')

    a('  <section class="tm-modes">')
    a('    <h2>Every solved question opens in five modes</h2>')
    a('    <p>This page is the route in. The learning happens on the question itself.</p>')
    a('    <ol>')
    for name, blurb in MODES:
        a('      <li><b>%s</b> &mdash; %s</li>' % (esc(name), esc(blurb)))
    a('    </ol>')
    a('  </section>')
    a('</main>')

    o.extend(footer(True))
    a('<script>')
    a(STICKY_SYNC_JS)
    a('</script>')
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def _slug(label):
    import re
    return 'dom-' + re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--out', default=None)
    args = ap.parse_args()
    specs = load_specs()
    if not specs:
        print('ERROR: no specs found')
        sys.exit(1)
    path = args.out or os.path.join(REPO_ROOT, OUT_REL)
    html = build(specs)
    st = write(path, html)
    tmap = TT.build_topic_map(solved_sittings(specs))
    print('%s  %s  (%d bytes)' % (OUT_REL.replace(os.sep, '/'), st, len(html.encode('utf-8'))))
    print('  %d domains, %d study topics, %d other buckets, %d questions, %d sittings'
          % (len(tmap['domains']),
             sum(len(d['topics']) for d in tmap['domains']),
             sum(1 for d in tmap['domains'] if d['other']['question_ids']),
             tmap['questions'], tmap['sittings']))


if __name__ == '__main__':
    main()
