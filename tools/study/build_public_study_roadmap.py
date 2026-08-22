#!/usr/bin/env python3
"""Generate the PUBLIC study roadmap teaser at SQ/study-roadmap.html.

    GOVERNED STUDY INTELLIGENCE          PUBLIC-SAFE PROJECTION        PAGE
    study_spine.json          --.
    study_mappings.json         |
    official_syllabus.json      +-> RX.build_model() -> project() -> render()
    official_crosswalk.json     |                        (whitelist)      |
    written_evidence_horizon.json                                        v
    study_progress.json       --'  (read by the model, DROPPED here)  SQ/study-roadmap.html

WHY A SEPARATE GENERATOR RATHER THAN A FLAG ON build_topic_pages.py
-------------------------------------------------------------------
The gated pages and this one answer to different rules, and a shared renderer
with an `if public:` branch is exactly how a paid field eventually reaches a
public page. Here the projection is a WHITELIST: a field must be named in
PUBLIC_TOPIC_FIELDS to survive, so a new column added to the workbook model
lands on the public page only when someone writes its name down. Everything
else -- Nixon's study progress, the priority score, the diagnostic coverage
bands, the hand-recorded topic gaps -- is dropped by default, not by exclusion.

WHY IT LIVES UNDER /SQ/
-----------------------
middleware.js declares `matcher: ["/meoclass1/:path*", "/solvedQP/:path*"]`.
Edge Middleware is never INVOKED off-matcher, so a page under /SQ/ is public
because the gate does not run, not because a rule inside the gate allows it.
That is the strongest form the guarantee comes in, and it is why this file
refuses to emit a single /meoclass1/ or /solvedQP/ link: a public visitor
following one would be bounced to a login for a product they have not bought,
and a Written-only customer following one would be bounced by the OTHER
product's paywall. Cross-product routing goes to the storefront. Always.

NO HAND-COUNTED NUMBER MAY APPEAR HERE
--------------------------------------
Every figure is read from a governed artefact and the evidence claim sentence
is produced by evidence_model.public_evidence_claim() via the workbook model.
The historical Written QI layer is a socket that currently reports NOT_STARTED;
when it reaches VALIDATED_RANGE the same code widens the wording by itself. No
marketing copy has to be rewritten for that transition, which is the point --
copy that has to be rewritten is copy that eventually is not.

SAFETY IS ASSERTED ON THE RENDERED BYTES, NOT ON INTENT
-------------------------------------------------------
assert_public_safe() runs over the finished HTML: forbidden evidence claims,
gated links, answer markers, private values and sample-quota overruns all fail
the build. A generator that only promises to be safe is a generator that is
unsafe on the day someone edits it.

Determinism: no clock; ids sorted; LF bytes.

Usage:
    python tools/study/build_public_study_roadmap.py            # write
    python tools/study/build_public_study_roadmap.py --check    # fail if stale
"""
import argparse, html, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import evidence_model as EM          # noqa: E402,F401  (contract owner)
import export_roadmap_xlsx as RX     # noqa: E402

D = os.path.join(ROOT, 'docs', 'study')
OUT = os.path.join(ROOT, 'SQ', 'study-roadmap.html')

E = html.escape
GA4 = 'G-0YEE2CBNP5'
SITE = 'https://marineintelligenceweekly.com'
CANONICAL = SITE + '/SQ/study-roadmap.html'

# ---------------------------------------------------------------------------
# The public contract.
#
# PUBLIC_TOPIC_FIELDS is the whole of what a topic card may know about itself.
# It is deliberately shorter than the workbook model. Anything absent here is
# not "hidden", it never enters the projection at all.
# ---------------------------------------------------------------------------
PUBLIC_TOPIC_FIELDS = (
    'topic_id', 'topic', 'study_order', 'prerequisites', 'unlocks',
    'oral_questions', 'examiner_evidenced_oral', 'distinct_examiners',
    'current_written_questions', 'current_written_papers',
    'current_written_recurrence_families', 'official_syllabus_items',
    'official_supporting_items',
)

# Named so the guard can prove they are gone rather than trusting the loop.
PRIVATE_TOPIC_FIELDS = (
    'priority_rank', 'priority_score',          # internal scoring
    'study_status', 'sessions_completed',       # Nixon's own progress
    'notes_written', 'last_touched',
    'gaps',                                     # hand-recorded weaknesses
    'coverage',                                 # coverage_matrix: DIAGNOSTIC ONLY
    'official_node_ids', 'links',               # internal ids / gated paths
)

SAMPLES_PER_TOPIC = 3      # 30 stems of 721 -- a teaser, not the corpus
SAMPLE_MAX_CHARS = 180
FAMILIES_PER_TOPIC = 3
MIN_FAMILY_SIZE = 2        # one sighting is not a recurrence

GATED_PREFIXES = ('/meoclass1/', '/solvedQP/', 'meoclass1/', 'solvedqp/')
# Markers that only ever appear in answer bodies on the QB/QP pages.
ANSWER_MARKERS = ('ce oral tip', 'class="answer', 'id="answer', 'model-answer',
                  'cheatsheet')

# Public product routes. Every one of these is off the middleware matcher.
ROUTE_STORE = '/SQ/index.html'
ROUTE_ORAL_TRIAL = '/SQ/trial.html?product=ORAL_QB_NOTES'
ROUTE_WRITTEN_TRIAL = '/SQ/trial.html?product=SOLVED_QP'
ROUTE_ORAL_SAMPLE = '/SQ/QB1_A.html'
ROUTE_WRITTEN_SAMPLE = '/SQ/solved-qp-sample-january-2026.html'
ROUTE_EXAMINER = '/SQ/examiner-index.html'


def _load(name):
    return json.load(open(os.path.join(D, name), encoding='utf-8'))


# ---------------------------------------------------------------------------
# Projection
# ---------------------------------------------------------------------------
def project():
    """Governed model -> the public-safe subset. Drops by whitelist."""
    model = RX.build_model()
    spine = _load('study_spine.json')
    horizon = _load('written_evidence_horizon.json')
    mappings = _load('study_mappings.json')['mappings']

    by_id = {d['domain_id']: d for d in spine['domains']}

    # Sample stems. ORAL only -- WRITTEN records carry no text, and inventing
    # one would be a second corpus. VALID_MAPPED only, so nothing still in
    # adjudication is advertised. Sorted ids: same page every run.
    samples = {}
    for qid, rec in sorted(mappings.items()):
        if rec['content_type'] != 'ORAL' or rec['mapping_status'] != 'VALID_MAPPED':
            continue
        tid, text = rec.get('topic_id'), (rec.get('text') or '').strip()
        if not tid or not text or len(text) > SAMPLE_MAX_CHARS:
            continue
        bucket = samples.setdefault(tid, [])
        if len(bucket) < SAMPLES_PER_TOPIC:
            bucket.append(text)

    topics = []
    for row in model['topics']:
        d = by_id[row['topic_id']]
        pub = {k: row[k] for k in PUBLIC_TOPIC_FIELDS}
        pub['why'] = d['rationale']
        pub['unlocks_count'] = len(d['dependants'])
        pub['prerequisite_names'] = [by_id[p]['short'] for p in d['prerequisites']]
        pub['families'] = [
            {'name': n, 'sightings': c}
            for n, c in d['written_question_intelligence']['largest_families']
            if c >= MIN_FAMILY_SIZE
        ][:FAMILIES_PER_TOPIC]
        pub['samples'] = samples.get(row['topic_id'], [])
        topics.append(pub)

    hist = horizon['layers']['historical_written_qi']
    cur = horizon['layers']['current_solved_written']

    # The evidence sentence is COMPUTED here, not taken on trust.
    #
    # build_model() reads the STORED string horizon['public_claim']
    # ['derived_sentence'], which build_evidence_horizon.py wrote. That is one
    # step upstream of this page, and the two can drift: a socket edited by
    # hand widens the layer while the stored sentence stays narrow. Drift in
    # that direction is fail-safe -- it understates -- but drift in the other
    # direction would put an unearned claim on a PUBLIC page, so neither is
    # tolerated. public_evidence_claim() is the authority; a mismatch means the
    # horizon artefact is stale and the build stops.
    derived = EM.public_evidence_claim(cur, hist)
    if derived != model['public_claim']:
        raise Unsafe(
            'evidence claim drift -- docs/study/written_evidence_horizon.json '
            'is stale. Re-run tools/study/build_evidence_horizon.py.\n'
            f'  stored:   {model["public_claim"]}\n'
            f'  computed: {derived}')

    return {
        'generated_from': model['generated_from'],
        'evidence_sentence': derived,
        'forbidden': horizon['public_claim']['forbidden_until_validated'],
        'current': {
            'papers': cur['papers_total'],
            'questions': cur['questions_total'],
            'earliest': cur['earliest_sitting'],
            'latest': cur['latest_sitting'],
        },
        'historical_status': hist['status'],
        'historical_integrated': hist['status'] in ('VALIDATED_RANGE', 'COMPLETE'),
        'oral_total': spine['totals']['oral_questions_total'],
        'oral_mapped': spine['totals']['oral_questions_mapped'],
        'official': model['official_source'],
        'official_effective_from': spine['official_syllabus']['effective_from'],
        'official_status': spine['official_syllabus']['status'],
        'official_items': len(_load('official_syllabus.json')['nodes']),
        'examiners': sorted({e for d in spine['domains']
                             for e in d['examiner_intelligence']['examiners']}),
        'topics': topics,
    }


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
CSS = """
:root{--navy:#0f172a;--teal:#0d9488;--teal-dark:#0f766e;--ink:#1e293b;
--bg:#f8fafc;--line:#e2e8f0;--muted:#64748b;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);
color:var(--ink);line-height:1.55}
nav.top{background:var(--navy);padding:.9rem 1.5rem;display:flex;align-items:center;
justify-content:space-between;gap:1rem;flex-wrap:wrap}
nav.top a.brand{color:var(--teal);font-weight:700;font-size:1.05rem;text-decoration:none}
nav.top a.back{color:#94a3b8;font-size:13px;text-decoration:none}
nav.top a.back:hover{color:#e2e8f0}
header.hero{background:var(--navy);color:#f8fafc;padding:2.6rem 1.5rem 2.2rem;text-align:center}
header.hero h1{font-size:clamp(1.5rem,4.2vw,2.2rem);font-weight:700;line-height:1.2;margin-bottom:.7rem}
header.hero h1 span{color:var(--teal)}
header.hero p.lead{font-size:1rem;color:#cbd5e1;max-width:640px;margin:0 auto 1rem}
header.hero p.evidence{font-size:.8rem;color:#94a3b8;max-width:640px;margin:0 auto}
.stats{display:flex;justify-content:center;gap:2rem;padding:1.15rem;background:#1e293b;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:1.35rem;font-weight:700;color:var(--teal)}
.stat-label{font-size:11.5px;color:#94a3b8;margin-top:2px}
main{max-width:880px;margin:0 auto;padding:1.6rem 1.25rem 0}
section{margin-bottom:2rem}
h2{font-size:1.15rem;font-weight:700;color:var(--navy);margin-bottom:.5rem}
h2 .h2sub{display:block;font-size:.8rem;font-weight:400;color:var(--muted);margin-top:.2rem}
p.body{font-size:.92rem;color:#334155;margin-bottom:.7rem}
.how{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1.1rem 1.2rem}
.how ol{margin:.5rem 0 0 1.1rem;font-size:.88rem;color:#334155}
.how li{margin-bottom:.35rem}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;margin-bottom:1rem;overflow:hidden}
.card.first{border:2px solid var(--teal)}
.card-head{background:var(--navy);color:#fff;padding:.85rem 1.1rem;display:grid;
grid-template-columns:auto 1fr;align-items:center;gap:.9rem}
.order{background:var(--teal);color:#fff;font-weight:800;font-size:.95rem;width:2rem;height:2rem;
border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}
.card-head h3{font-size:1.02rem;color:var(--teal);font-weight:700;line-height:1.3}
.card-head .tid{font-size:.68rem;color:#94a3b8;font-weight:400;letter-spacing:.04em}
.card-body{padding:1rem 1.1rem}
.why{font-size:.88rem;color:#334155;margin-bottom:.8rem}
.prereq{font-size:.78rem;color:var(--muted);margin-bottom:.8rem}
.prereq b{color:var(--ink)}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));gap:.5rem;margin-bottom:.9rem}
.metric{background:var(--bg);border:1px solid var(--line);border-radius:7px;padding:.5rem .6rem}
.metric .m-num{font-size:1.02rem;font-weight:700;color:var(--teal-dark)}
.metric .m-lab{font-size:10.5px;color:var(--muted);line-height:1.35;margin-top:1px}
.blocklabel{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
font-weight:700;margin:.9rem 0 .4rem}
ul.samples{list-style:none}
ul.samples li{border-top:1px solid var(--line);padding:.45rem 0;font-size:.84rem;color:#334155}
ul.samples li:first-child{border-top:none}
ul.fams{list-style:none}
ul.fams li{font-size:.82rem;color:#334155;padding:.28rem 0}
ul.fams .n{color:var(--teal-dark);font-weight:700}
.locked{font-size:.76rem;color:var(--muted);margin-top:.55rem;padding-top:.5rem;border-top:1px dashed var(--line)}
.firstwhy{background:#f0fdfa;border:1px solid #99f6e4;border-radius:8px;padding:.8rem .95rem;margin-bottom:.9rem}
.firstwhy b{color:var(--teal-dark)}
.firstwhy ul{margin:.4rem 0 0 1.05rem;font-size:.85rem;color:#134e4a}
.firstwhy li{margin-bottom:.2rem}
.threeway{display:grid;grid-template-columns:repeat(auto-fit,minmax(238px,1fr));gap:.9rem}
.way{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1rem}
.way h3{font-size:.95rem;color:var(--navy);margin-bottom:.3rem}
.way .q{font-size:.78rem;color:var(--teal-dark);font-weight:600;margin-bottom:.4rem}
.way p{font-size:.84rem;color:#334155;margin-bottom:.6rem}
.way a{font-size:.83rem;color:var(--teal-dark);font-weight:600;text-decoration:none}
.way a:hover{text-decoration:underline}
.horizon{background:#fff;border:1px solid var(--line);border-left:4px solid var(--teal);
border-radius:8px;padding:1rem 1.1rem;font-size:.87rem;color:#334155}
.horizon b{color:var(--navy)}
.official{background:#fff;border:1px solid var(--line);border-left:4px solid #1d4ed8;
border-radius:8px;padding:1rem 1.1rem;font-size:.87rem;color:#334155}
.official b{color:#1e3a8a}
.official .note{display:block;margin-top:.55rem;font-size:.82rem;color:var(--muted)}
.ctas{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}
.cta{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1.15rem;text-align:center}
.cta h3{font-size:1rem;color:var(--navy);margin-bottom:.35rem}
.cta p{font-size:.83rem;color:var(--muted);margin-bottom:.85rem}
.btn{display:inline-block;padding:.6rem 1.3rem;border-radius:7px;font-size:.87rem;
font-weight:600;text-decoration:none;background:var(--teal);color:#fff}
.btn:hover{background:var(--teal-dark)}
.btn.ghost{background:transparent;border:1.5px solid var(--teal);color:var(--teal-dark)}
.btn.ghost:hover{background:var(--teal);color:#fff}
.cta .alt{display:block;margin-top:.55rem;font-size:.79rem;color:var(--muted);text-decoration:none}
.cta .alt:hover{color:var(--teal-dark);text-decoration:underline}
footer{max-width:880px;margin:0 auto;padding:1.5rem 1.25rem 2.5rem;font-size:.76rem;color:var(--muted)}
footer a{color:var(--muted)}
@media(max-width:520px){
main{padding:1.2rem .9rem 0}
.stats{gap:1.2rem}
.card-head{gap:.65rem;padding:.75rem .85rem}
.card-body{padding:.85rem}
}
"""

JS = """
(function(){
  function ev(name,params){ if(typeof gtag==='function'){ gtag('event',name,params||{}); } }
  ev('study_roadmap_view',{page_location:location.pathname});
  document.addEventListener('click',function(e){
    var a=e.target.closest ? e.target.closest('a[data-ev]') : null; if(!a) return;
    ev(a.getAttribute('data-ev'),{topic:a.getAttribute('data-topic')||'',
                                  link_url:a.getAttribute('href')||''});
  });
  var seen={};
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(en){
        var id=en.target.id;
        if(en.isIntersecting && id && !seen[id]){ seen[id]=1; ev('study_topic_preview',{topic:id}); }
      });
    },{threshold:.5});
    document.querySelectorAll('.card[id]').forEach(function(c){ io.observe(c); });
  }
})();
"""

TITLE = 'MEO Class I Study Roadmap — Oral, Written & Examiner Intelligence | MIW'


def description(p):
    return (f"Topic-by-topic MEO Class I study roadmap built from MIW's mapped "
            f"Oral question corpus, {p['current']['questions']} solved Written "
            f"questions across {p['current']['papers']} papers, examiner evidence "
            f"and official DGMA syllabus scope.")


def head(p):
    desc = description(p)
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{E(TITLE)}</title>\n'
        f'<meta name="description" content="{E(desc)}">\n'
        f'<link rel="canonical" href="{CANONICAL}">\n'
        '<meta name="robots" content="index, follow">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="MEO Class I Study Roadmap '
        '&mdash; Marine Intelligence Weekly">\n'
        f'<meta property="og:description" content="{E(desc)}">\n'
        f'<meta property="og:url" content="{CANONICAL}">\n'
        '<meta name="twitter:card" content="summary">\n'
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>\n'
        '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
        f"gtag('js',new Date());gtag('config','{GA4}');</script>\n"
        f'<style>{CSS}</style>\n</head>\n<body>\n')


def metric(num, label):
    return (f'<div class="metric"><div class="m-num">{num}</div>'
            f'<div class="m-lab">{E(label)}</div></div>')


def render_card(t, p):
    n_topics = len(p['topics'])
    first = t['study_order'] == 1
    out = [f'<div class="card{" first" if first else ""}" id="{t["topic_id"]}">',
           '<div class="card-head">',
           f'<div class="order">{t["study_order"]}</div>',
           f'<div><h3>{E(t["topic"])}</h3>'
           f'<div class="tid">{t["topic_id"]} &middot; study order '
           f'{t["study_order"]} of {n_topics}</div></div>',
           '</div>',
           '<div class="card-body">']

    if first:
        out.append(
            '<div class="firstwhy"><b>Why this topic comes first.</b>'
            '<ul>'
            '<li>It has no prerequisites &mdash; it is a topic you can start '
            'cold.</li>'
            f'<li>{t["unlocks_count"]} of the other {n_topics - 1} topics list it '
            f'as a prerequisite.</li>'
            f'<li>It carries {t["current_written_questions"]} solved Written '
            f'questions across {t["current_written_papers"]} papers.</li>'
            f'<li>{t["examiner_evidenced_oral"]} of its Oral questions are tied to '
            f'a named examiner by recorded evidence, across '
            f'{t["distinct_examiners"]} examiners.</li>'
            f'<li>It is the leading MIW topic for {t["official_syllabus_items"]} '
            f'items of the official Annexure III syllabus and supports '
            f'{t["official_supporting_items"]} more.</li>'
            '</ul></div>')

    out.append(f'<div class="why">{E(t["why"])}</div>')

    pre = (', '.join(E(n) for n in t['prerequisite_names'])
           if t['prerequisite_names'] else 'none &mdash; start here')
    out.append(f'<div class="prereq"><b>Prerequisites:</b> {pre} &nbsp;&middot;&nbsp; '
               f'<b>Unlocks:</b> {t["unlocks_count"]} later '
               f'topic{"s" if t["unlocks_count"] != 1 else ""}</div>')

    out.append('<div class="metrics">')
    out.append(metric(t['oral_questions'], 'mapped Oral questions'))
    out.append(metric(t['examiner_evidenced_oral'], 'Oral questions with examiner evidence'))
    out.append(metric(t['distinct_examiners'], 'examiners evidenced'))
    out.append(metric(t['current_written_questions'], 'solved Written questions'))
    out.append(metric(t['current_written_papers'], 'Written papers touched'))
    out.append(metric(t['current_written_recurrence_families'],
                      'recurring Written question families'))
    out.append(metric(t['official_syllabus_items'], 'Annexure III items led'))
    out.append('</div>')

    if t['families']:
        out.append('<div class="blocklabel">Recurring Written question families</div>')
        out.append('<ul class="fams">')
        for f in t['families']:
            out.append(f'<li>{E(f["name"])} &mdash; '
                       f'<span class="n">{f["sightings"]}&times;</span></li>')
        out.append('</ul>')

    if t['samples']:
        out.append(f'<div class="blocklabel">Sample Oral questions '
                   f'({len(t["samples"])} of {t["oral_questions"]})</div>')
        out.append('<ul class="samples">')
        for s in t['samples']:
            out.append(f'<li>{E(s)}</li>')
        out.append('</ul>')
        out.append('<div class="locked">Worked answers, examiner attribution and '
                   'the full question set for this topic are part of the Question '
                   'Bank.</div>')

    out.append('</div></div>')
    return ''.join(out)


def render(p):
    parts = [head(p)]
    parts.append(
        '<nav class="top">'
        f'<a class="brand" href="{SITE}">Marine Intelligence Weekly</a>'
        f'<a class="back" href="{ROUTE_STORE}">MEO Class 1 products &rarr;</a>'
        '</nav>')

    parts.append(
        '<header class="hero">'
        '<h1>MEO Class I <span>Study Roadmap</span></h1>'
        '<p class="lead">Do not study hundreds of Oral and Written questions at '
        'random. Study the connected topics, in the order that gives the most '
        'leverage &mdash; prerequisites first.</p>'
        f'<p class="evidence">{E(p["evidence_sentence"])}</p>'
        '</header>')

    parts.append('<div class="stats">')
    for num, lab in (
        (len(p['topics']), 'study topics'),
        (p['oral_mapped'], 'mapped Oral questions'),
        (p['current']['questions'], 'solved Written questions'),
        (p['current']['papers'], 'Written papers'),
        (len(p['examiners']), 'examiners evidenced'),
        (p['official_items'], 'official syllabus items'),
    ):
        parts.append(f'<div class="stat"><div class="stat-num">{num}</div>'
                     f'<div class="stat-label">{E(lab)}</div></div>')
    parts.append('</div>')

    parts.append('<main>')

    parts.append(
        '<section><h2>How the order is decided'
        '<span class="h2sub">The ordering is MIW-derived from examination '
        'evidence. It is not an official ordering.</span></h2>'
        '<div class="how">'
        '<p class="body">Every MEO Class I Oral and solved Written question in '
        'MIW is mapped to one of ten study topics. Each topic then carries its '
        'own evidence &mdash; how often it is asked orally, how many examiners '
        'are recorded asking it, how much of the solved Written corpus it '
        'accounts for, how many Written question families recur in it, and how '
        'much of the official syllabus it leads.</p>'
        '<ol>'
        '<li>Topics are scored on that evidence, not on opinion.</li>'
        '<li>A topic is only released into the order once every topic it depends '
        'on is already placed, so you are never sent to a subject that assumes '
        'one you have not covered.</li>'
        '<li>Among the topics you <i>could</i> start next, the highest-scoring '
        'one goes first.</li>'
        '</ol>'
        '<p class="body" style="margin-top:.7rem">That is why the heaviest topic '
        'by raw score is not always the earliest: leverage is worth nothing if '
        'you cannot yet read the material.</p>'
        '</div></section>')

    parts.append('<section><h2>The ten topics, in study order'
                 '<span class="h2sub">Every count below is generated from the '
                 'current governed corpus &mdash; corpus state '
                 f'{E(p["generated_from"])}.</span></h2>')
    for t in p['topics']:
        parts.append(render_card(t, p))
    parts.append('</section>')

    parts.append(
        '<section><h2>Three ways into the same corpus</h2>'
        '<div class="threeway">'
        '<div class="way"><div class="q">What should I learn?</div>'
        '<h3>Study by topic</h3>'
        '<p>The roadmap above: ten connected topics in dependency order, each '
        'carrying its own Oral, Written and examiner evidence.</p></div>'
        '<div class="way"><div class="q">What does this examiner ask?</div>'
        '<h3>Browse by examiner</h3>'
        f'<p>Questions recorded against {len(p["examiners"])} named examiners, '
        'built from candidate-reported sittings.</p>'
        f'<a href="{ROUTE_EXAMINER}" data-ev="study_examiner_cta">'
        'Open the Examiner Index &rarr;</a></div>'
        '<div class="way"><div class="q">How is it answered under exam conditions?</div>'
        '<h3>Solved Written papers</h3>'
        f'<p>{p["current"]["papers"]} papers worked question by question, '
        f'{p["current"]["questions"]} answers, with marks and sub-parts kept as '
        'the paper set them.</p>'
        f'<a href="{ROUTE_WRITTEN_SAMPLE}" data-ev="study_written_sample">'
        'See a solved paper &rarr;</a></div>'
        '</div></section>')

    hist_phrase = ('is being expanded' if not p['historical_integrated']
                   else 'is integrated')
    parts.append(
        '<section><h2>What these numbers rest on</h2>'
        '<div class="horizon">'
        f'<b>Current evidence.</b> {E(p["evidence_sentence"])} The Written figures '
        'above come from that mapped, solved corpus &mdash; sittings '
        f'{E(p["current"]["earliest"])} to {E(p["current"]["latest"])} &mdash; and '
        'from nothing else.'
        f'<br><br><b>Historical Written question intelligence {hist_phrase}.</b> '
        'Older question papers are not yet part of the governed evidence layer, '
        'so no figure on this page is drawn from them and no claim here reaches '
        'further back than the sittings named above. As that layer is validated '
        'and integrated, the recurrence and coverage figures on this page widen '
        'from the data &mdash; the page is generated, so the numbers move when '
        'the evidence does.'
        '</div></section>')

    o = p['official']
    parts.append(
        '<section><h2>Official syllabus alignment</h2>'
        '<div class="official">'
        f'<b>Cross-walked to {E(o["circular"])}, Annexure III, effective '
        f'{E(p["official_effective_from"])}.</b> Each topic above records how many '
        f'of the {p["official_items"]} official Annexure III items it leads and how '
        'many it supports.'
        '<span class="note">The circular is adopted but not yet in force: it takes '
        f'effect on {E(p["official_effective_from"])} and does not govern sittings '
        'before that date. The study order itself is MIW-derived from examination '
        'evidence &mdash; the official syllabus is one evidence layer among '
        'several, not the reason for the ordering.</span>'
        '</div></section>')

    parts.append(
        '<section><h2>Start on the roadmap</h2>'
        '<div class="ctas">'
        '<div class="cta"><h3>Oral Question Bank</h3>'
        f'<p>{p["oral_total"]} MEO Class I oral questions with worked answers, '
        'examiner attribution and topic navigation.</p>'
        f'<a class="btn" href="{ROUTE_ORAL_TRIAL}" data-ev="study_oral_cta">'
        'Explore the Oral Question Bank</a>'
        f'<a class="alt" href="{ROUTE_ORAL_SAMPLE}" data-ev="study_oral_sample">'
        'or read a free sample chapter first</a></div>'
        '<div class="cta"><h3>Solved Written Papers</h3>'
        f'<p>{p["current"]["papers"]} papers, {p["current"]["questions"]} worked '
        f'answers, {E(p["current"]["earliest"])} to {E(p["current"]["latest"])}.</p>'
        f'<a class="btn" href="{ROUTE_WRITTEN_TRIAL}" data-ev="study_written_cta">'
        'Explore Solved Written Papers</a>'
        f'<a class="alt" href="{ROUTE_WRITTEN_SAMPLE}" data-ev="study_written_sample">'
        'or read a free solved paper first</a></div>'
        '<div class="cta"><h3>All MEO Class I tools</h3>'
        '<p>Both products, the free trials and what each one includes, on one '
        'page.</p>'
        f'<a class="btn ghost" href="{ROUTE_STORE}" data-ev="study_store_cta">'
        'See MIW MEO Class I tools</a></div>'
        '</div></section>')

    parts.append('</main>')
    parts.append(
        f'<footer>Official scope: {E(o["circular"])} ({E(o["issue_date"])}), '
        'Annexure III &mdash; Syllabus for MEO Class I Preparatory Course; '
        f'effective {E(p["official_effective_from"])}. Topic structure and study '
        'order are MIW-derived from examination evidence and are not an official '
        'DGMA ordering. Counts generated from the governed MIW corpus at state '
        f'{E(p["generated_from"])}. '
        '<a href="/terms.html">Terms</a> &middot; '
        '<a href="/privacy.html">Privacy</a></footer>')
    parts.append(f'<script>{JS}</script>\n</body>\n</html>\n')
    return ''.join(parts)


# ---------------------------------------------------------------------------
# Guards -- run against the rendered bytes
# ---------------------------------------------------------------------------
class Unsafe(Exception):
    pass


def assert_public_safe(doc, p):
    low = doc.lower()

    for phrase in p['forbidden']:
        if phrase.lower() in low:
            raise Unsafe(f'forbidden evidence claim present: {phrase!r}')
    # The specific overclaims the brief names, in the forms they would take.
    for phrase in ('16 years', '2010-2026', '2010–2026', 'all historical papers',
                   'since 2010', 'years of question-paper intelligence'):
        if phrase.lower() in low:
            raise Unsafe(f'unsupported historical span claim: {phrase!r}')
    if not p['historical_integrated']:
        for phrase in ('historical written question intelligence is complete',
                       'complete historical'):
            if phrase in low:
                raise Unsafe('historical QI claimed complete while the socket is '
                             f'{p["historical_status"]}')

    for pref in GATED_PREFIXES:
        if pref in low:
            raise Unsafe(f'link into gated product surface: {pref!r}')

    for marker in ANSWER_MARKERS:
        if marker in low:
            raise Unsafe(f'answer-surface marker present: {marker!r}')

    # Private model fields must not have been projected at all.
    for t in p['topics']:
        leaked = [f for f in PRIVATE_TOPIC_FIELDS if f in t]
        if leaked:
            raise Unsafe(f'{t["topic_id"]} carries private fields: {leaked}')

    # Internal review machinery must not be reachable from the page.
    for token in ('mapping_review_queue', 'review_pending', 'accidentally_unmapped',
                  'mapping_confidence', 'study_progress', 'priority_score',
                  'adjudication', 'not_started', 'sessions_completed'):
        if token in low:
            raise Unsafe(f'internal governance token present: {token!r}')

    ids = [t['topic_id'] for t in p['topics']]
    if len(ids) != 10 or len(set(ids)) != 10:
        raise Unsafe(f'expected 10 unique topics, got {ids}')
    if sorted(t['study_order'] for t in p['topics']) != list(range(1, 11)):
        raise Unsafe('study order is not a 1..10 permutation')

    for t in p['topics']:
        if len(t['samples']) > SAMPLES_PER_TOPIC:
            raise Unsafe(f'{t["topic_id"]} exceeds the per-topic sample quota')
    total = sum(len(t['samples']) for t in p['topics'])
    if total > SAMPLES_PER_TOPIC * len(p['topics']):
        raise Unsafe(f'{total} sampled stems exceeds the global quota')
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    p = project()
    doc = render(p)
    samples = assert_public_safe(doc, p)
    rel = os.path.relpath(OUT, ROOT)

    if args.check:
        if not os.path.exists(OUT):
            print(f'FAIL: {rel} is missing')
            return 1
        if open(OUT, encoding='utf-8', newline='').read() != doc:
            print(f'FAIL: {rel} is stale')
            return 1
        print(f'public study roadmap -- up to date ({len(p["topics"])} topics, '
              f'{samples} sampled stems)')
        return 0

    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        fh.write(doc)
    print(f'wrote {rel} ({len(doc):,} bytes; {len(p["topics"])} topics, '
          f'{samples} sampled stems)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
