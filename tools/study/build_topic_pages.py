#!/usr/bin/env python3
"""Generate the candidate-facing study surfaces from the governed study model.

    study_spine.json / study_mappings.json / official_syllabus.json
    official_crosswalk.json / coverage_matrix.json
    written_evidence_horizon.json / study_progress.json
            |
            v   build_topic_pages.py
            |
    meoclass1/topics.html   Oral study BY TOPIC  (the "what should I learn?" view)
    meoclass1/study.html    the MEO Class I study roadmap landing

WHY GENERATED
-------------
Ten hand-authored topic cards would have to be edited every time a paper, a
question or the historical Written QI layer lands. Nothing here is typed: every
count is `len()` of the records rendered, and the evidence sentence is produced
by `evidence_model.public_evidence_claim()`, so the page cannot claim a wider
corpus than the repository stores. When historical QI is validated, these pages
strengthen themselves on the next run.

GATING
------
Both outputs live under `meoclass1/`, which `middleware.js` protects with the
wildcard matcher `/meoclass1/:path*`. They inherit the paywall by path, so the
question text they carry is no more exposed than the QB pages it comes from.
No answer content is rendered here -- only question stems that already appear
on the gated QB pages, plus links to them.

CROSS-PRODUCT LINKS GO TO THE STOREFRONT, NEVER TO THE OTHER PAID SURFACE
-------------------------------------------------------------------------
"Written by topic" links to /SQ/ (public), NOT to /solvedQP/topics.html.
`render_common.delivery_links()` already records why in the other direction:
ORAL_QB_NOTES and SOLVED_QP are separate entitlements, so a customer who owns
one and not the other would be bounced to a login page by their own product's
navigation. Linking a gated page across the product boundary is a support
ticket, not a convenience -- which is also why this generator does not add
reciprocal links into the Written surface.

Determinism: no clock, no hash seed dependence; ids are sorted. Output bytes
are LF.

Usage:
    python tools/study/build_topic_pages.py            # write
    python tools/study/build_topic_pages.py --check    # fail if stale
"""
import argparse, collections, html, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import evidence_model as EM
import export_roadmap_xlsx as RX

D = os.path.join(ROOT, 'docs', 'study')
EXAMINERS = os.path.join(ROOT, 'meoclass1', 'oral-intelligence', 'examiner-audit',
                         'CURRENT_EXAMINER_RELATIONSHIPS.jsonl')
TOPICS_OUT = os.path.join(ROOT, 'meoclass1', 'topics.html')
STUDY_OUT = os.path.join(ROOT, 'meoclass1', 'study.html')

E = html.escape
GA4 = 'G-0YEE2CBNP5'

CSS = """
:root{--navy:#0f2942;--teal:#0d9488;--teal-dark:#0f766e;--orange:#f97316;--ink:#1e293b;--grey-bg:#f8fafc;--grey-border:#e2e8f0;--grey-text:#64748b;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--grey-bg);color:var(--ink);line-height:1.5;}
.topbar{position:sticky;top:0;background:var(--navy);color:#fff;z-index:100;display:flex;align-items:center;gap:1rem;padding:.6rem 1.2rem;border-bottom:3px solid var(--teal);}
.topbar a{color:#94a3b8;font-size:.85rem;text-decoration:none;}
.topbar a:hover{color:#fff;}
.topbar a.here{color:#fff;font-weight:700;}
.topbar-logo{font-size:1.2rem;font-weight:800;color:var(--teal);text-decoration:none;}
.topbar nav{display:flex;flex-wrap:wrap;gap:1rem;margin-left:auto;}
.page-header{background:var(--navy);color:#fff;padding:1.6rem 1.5rem 1.2rem;}
.page-header h1{font-size:1.5rem;margin-bottom:.4rem;}
.page-header p{color:#cbd5e1;font-size:.85rem;max-width:760px;}
.summary-bar{display:flex;flex-wrap:wrap;gap:.9rem;padding:.8rem 1.5rem;background:#fff;border-bottom:1px solid var(--grey-border);font-size:.78rem;color:var(--grey-text);}
.summary-bar strong{color:var(--ink);}
.mininav{position:sticky;top:46px;z-index:90;display:flex;flex-wrap:wrap;gap:.5rem;padding:.7rem 1.5rem;background:#fff;border-bottom:2px solid var(--grey-border);}
.mini-pill{background:var(--grey-bg);border:1px solid var(--grey-border);border-radius:20px;padding:.35rem .9rem;font-size:.8rem;font-weight:700;text-decoration:none;color:var(--ink);}
.mini-pill span{color:var(--grey-text);font-weight:400;}
.mini-pill:hover{background:var(--teal);color:#fff;}
.mini-pill:hover span{color:#e0f2f1;}
main{max-width:960px;margin:0 auto;padding:1.5rem;}
.t-section{background:#fff;border:1px solid var(--grey-border);border-radius:10px;margin-bottom:1.1rem;overflow:hidden;scroll-margin-top:110px;}
.t-head{background:var(--navy);color:#fff;padding:.9rem 1.2rem;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:.9rem;}
.t-order{background:var(--teal);color:#fff;font-weight:800;font-size:1rem;width:2rem;height:2rem;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;}
.t-head h2{font-size:1.08rem;color:var(--teal);}
.t-id{font-size:.7rem;color:#94a3b8;font-weight:400;}
.t-sub{font-size:.78rem;color:#cbd5e1;margin-top:.2rem;}
.t-stats{font-size:.72rem;color:#94a3b8;white-space:nowrap;text-align:right;}
.t-body{padding:1rem 1.2rem;}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:.8rem;}
.chip{font-size:.7rem;padding:.2rem .6rem;border-radius:12px;background:var(--grey-bg);border:1px solid var(--grey-border);color:var(--grey-text);}
.chip.strong{background:#ecfdf5;border-color:#a7f3d0;color:#047857;}
.chip.partial{background:#fffbeb;border-color:#fde68a;color:#b45309;}
.chip.weak{background:#fef2f2;border-color:#fecaca;color:#b91c1c;}
.chip.official{background:#eff6ff;border-color:#bfdbfe;color:#1d4ed8;}
.blocklabel{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:var(--grey-text);font-weight:700;margin:.9rem 0 .4rem;}
.off-item{border-left:3px solid var(--teal);padding:.45rem .7rem;margin-bottom:.45rem;background:var(--grey-bg);font-size:.8rem;}
.off-item b{color:var(--teal-dark);}
.q-list{list-style:none;}
.q-list li{border-top:1px solid var(--grey-border);padding:.5rem 0;font-size:.83rem;}
.q-list li:first-child{border-top:none;}
.q-list a{color:var(--navy);text-decoration:none;font-weight:600;}
.q-list a:hover{color:var(--teal);text-decoration:underline;}
.q-ex{font-size:.7rem;color:var(--orange);margin-left:.4rem;}
.q-more{font-size:.76rem;color:var(--grey-text);padding-top:.5rem;}
.prereq{font-size:.78rem;color:var(--grey-text);margin-bottom:.5rem;}
.prereq b{color:var(--ink);}
.gaps{font-size:.78rem;background:#fffbeb;border:1px solid #fde68a;border-radius:6px;padding:.5rem .7rem;margin-top:.7rem;color:#92400e;}
.note{font-size:.76rem;color:var(--grey-text);margin-top:1.2rem;padding:.8rem 1rem;background:#fff;border:1px solid var(--grey-border);border-radius:8px;}
.evidence{font-size:.78rem;color:var(--grey-text);}
footer{max-width:960px;margin:0 auto;padding:1.2rem 1.5rem 2.5rem;font-size:.74rem;color:var(--grey-text);}
"""

TOPBAR = """<div class="topbar">
<a class="topbar-logo" href="index.html">MIW</a>
<nav>
<a href="study.html"{study_here}>Study Roadmap</a>
<a href="topics.html"{topics_here}>Oral by Topic</a>
<a href="/SQ/index.html#solved-qp">Solved Written Papers</a>
<a href="examiner-index.html">Examiner Index</a>
<a href="index.html">Question Bank</a>
<a href="oralnotes/index.html">Notes</a>
</nav>
</div>"""


def load_all():
    m = RX.build_model()
    mappings = json.load(open(os.path.join(D, 'study_mappings.json'),
                              encoding='utf-8'))['mappings']
    official = json.load(open(os.path.join(D, 'official_syllabus.json'),
                              encoding='utf-8'))
    ex = collections.defaultdict(set)
    if os.path.exists(EXAMINERS):
        for line in open(EXAMINERS, encoding='utf-8'):
            line = line.strip()
            if not line:
                continue
            rel = json.loads(line)
            qid = rel.get('question_id') or rel.get('id')
            name = rel.get('examiner') or rel.get('examiner_name')
            if qid and name:
                ex[qid].add(name)
    return m, mappings, official, ex


def head(title, description):
    # GA4 is not optional decoration: tools/security/ga_coverage.test.mjs
    # asserts that EVERY served page carries exactly one canonical
    # installation, and these two shipped without it. The snippet must stay
    # byte-identical to the house form -- the analyser matches the loader and
    # the config separately and counts the id literally twice.
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            f'<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">\n'
            f'<meta name="description" content="{E(description)}">\n'
            f'<title>{E(title)}</title>\n'
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>\n'
            f'<script>window.dataLayer=window.dataLayer||[];'
            f'function gtag(){{dataLayer.push(arguments);}}'
            f"gtag('js',new Date());gtag('config','{GA4}');</script>\n"
            f'<style>{CSS}</style>\n</head>\n<body>\n')


def coverage_chips(bands):
    out = []
    for band, cls in (('STRONG', 'strong'), ('PARTIAL', 'partial'),
                      ('WEAK', 'weak'), ('NONE', 'weak')):
        n = bands.count(band)
        if n:
            out.append(f'<span class="chip {cls}">{n} {band.title()}</span>')
    return ''.join(out)


def build_topics_html(model, mappings, official, ex):
    by_node = {n['official_node_id']: n for n in official['nodes']}
    cov_bands = collections.defaultdict(list)
    for row in json.load(open(os.path.join(D, 'coverage_matrix.json'),
                              encoding='utf-8'))['nodes']:
        cov_bands[row['primary_topic']].append(row['coverage'])

    orals = collections.defaultdict(list)
    for qid, rec in sorted(mappings.items()):
        if rec['content_type'] != 'ORAL' or not rec.get('topic_id'):
            continue
        orals[rec['topic_id']].append(rec)

    total_oral = sum(len(v) for v in orals.values())
    parts = [head('Oral Study by Topic — MEO Class 1 | Marine Intelligence Weekly',
                  'Every mapped MEO Class I oral question, grouped by study topic '
                  'and aligned to the official DGMA syllabus.')]
    parts.append(TOPBAR.format(study_here='', topics_here=' class="here"'))
    parts.append(
        '<div class="page-header">'
        '<h1>Oral Study by Topic</h1>'
        '<p>Every mapped oral question, grouped into the ten MIW study topics and '
        'aligned to the official DGMA syllabus. Topics appear in <b>recommended '
        'study order</b> &mdash; prerequisites first, so you are never sent to a '
        'topic that assumes one you have not covered.</p></div>')
    parts.append(
        f'<div class="summary-bar">'
        f'<span><strong>{total_oral}</strong> mapped oral questions</span>'
        f'<span><strong>{len(model["topics"])}</strong> study topics</span>'
        f'<span><strong>{len(official["nodes"])}</strong> official syllabus items</span>'
        f'<span class="evidence">{E(model["public_claim"])}</span>'
        f'</div>')

    parts.append('<div class="mininav">')
    for t in model['topics']:
        parts.append(f'<a class="mini-pill" href="#{t["topic_id"]}">'
                     f'{t["topic_id"]} <span>{len(orals.get(t["topic_id"], ()))}</span></a>')
    parts.append('</div>\n<main>')

    for t in model['topics']:
        tid = t['topic_id']
        qs = orals.get(tid, [])
        parts.append(f'<section class="t-section" id="{tid}">')
        parts.append(
            f'<div class="t-head"><div class="t-order">{t["study_order"]}</div>'
            f'<div><h2>{E(t["topic"])} <span class="t-id">{tid}</span></h2>'
            f'<div class="t-sub">Prerequisites: {E(t["prerequisites"])} '
            f'&middot; Unlocks: {E(t["unlocks"])}</div></div>'
            f'<div class="t-stats">{len(qs)} oral<br>'
            f'{t["current_written_questions"]} written<br>'
            f'{t["examiner_evidenced_oral"]} examiner-evidenced</div></div>')
        parts.append('<div class="t-body">')

        parts.append('<div class="chips">')
        parts.append(f'<span class="chip official">{t["official_syllabus_items"]}'
                     f' official item(s)</span>')
        parts.append(coverage_chips(cov_bands.get(tid, [])))
        parts.append(f'<span class="chip">{t["current_written_papers"]} written papers</span>')
        parts.append(f'<span class="chip">{t["distinct_examiners"]} examiners</span>')
        parts.append('</div>')

        nodes = [n for n in t['official_node_ids'].split(', ') if n != '—']
        if nodes:
            parts.append('<div class="blocklabel">Official DGMA syllabus scope</div>')
            for nid in nodes:
                n = by_node[nid]
                parts.append(f'<div class="off-item"><b>Item {n["official_number"]}</b> '
                             f'&mdash; {E(n["official_text"][:190].rstrip())}&hellip;</div>')

        if qs:
            parts.append(f'<div class="blocklabel">Oral questions ({len(qs)})</div>')
            parts.append('<ul class="q-list">')
            for rec in qs:
                names = sorted(ex.get(rec['canonical_question_id'], ()))
                tag = (f'<span class="q-ex">{E(", ".join(names))}</span>'
                       if names else '')
                text = (rec.get('text') or '').strip()
                parts.append(
                    f'<li><a href="{E(rec["source_file"])}#{E(rec["anchor"])}">'
                    f'{E(text) if text else E(rec["canonical_question_id"])}</a>{tag}</li>')
            parts.append('</ul>')
        else:
            parts.append('<div class="q-more">No oral questions are mapped to this '
                         'topic yet &mdash; its evidence is written-only.</div>')

        if t['gaps'] != '—':
            parts.append(f'<div class="gaps"><b>Known gaps:</b> {E(t["gaps"])}</div>')
        parts.append('</div></section>')

    parts.append('</main>')
    parts.append(
        '<footer>Questions are grouped by governed mapping, not by page. '
        'A question appears under the topic its mapping record names, which is '
        'why some questions sit under a different topic from the question-bank '
        'page they live on. '
        f'Official scope: {E(model["official_source"]["circular"])}, Annexure III '
        '&mdash; adopted, effective 2027-01-01.</footer>')
    parts.append('\n</body>\n</html>\n')
    return ''.join(parts)


def build_study_html(model, official):
    hist = model['evidence_horizon']['historical_written_qi']
    cur = model['evidence_horizon']['current_solved_written']
    parts = [head('MEO Class 1 Study Roadmap | Marine Intelligence Weekly',
                  'Study MEO Class I by connected topic in a dependency-ordered '
                  'roadmap built from oral questions, solved written papers, '
                  'examiner evidence and the official DGMA syllabus.')]
    parts.append(TOPBAR.format(study_here=' class="here"', topics_here=''))
    parts.append(
        '<div class="page-header"><h1>MEO Class I Study Roadmap</h1>'
        '<p>Study by connected topic instead of moving randomly through hundreds '
        'of questions. Each topic below joins its oral questions, solved written '
        'questions, examiner evidence and official DGMA syllabus scope &mdash; '
        'and they are ordered so that prerequisites come first.</p></div>')
    parts.append(
        f'<div class="summary-bar">'
        f'<span><strong>{len(model["topics"])}</strong> topics in study order</span>'
        f'<span><strong>{cur["papers_total"]}</strong> solved written papers</span>'
        f'<span><strong>{cur["questions_total"]}</strong> written questions</span>'
        f'<span><strong>{len(official["nodes"])}</strong> official syllabus items</span>'
        f'<span><strong>{cur["earliest_sitting"]}&ndash;{cur["latest_sitting"]}</strong> '
        f'written evidence</span></div>')
    parts.append('<main>')

    for t in model['topics']:
        tid = t['topic_id']
        parts.append(f'<section class="t-section" id="{tid}">')
        parts.append(
            f'<div class="t-head"><div class="t-order">{t["study_order"]}</div>'
            f'<div><h2>{E(t["topic"])} <span class="t-id">{tid}</span></h2>'
            f'<div class="t-sub">{E(t["study_status"].replace("_", " ").title())}'
            f'</div></div>'
            f'<div class="t-stats">{t["oral_questions"]} oral<br>'
            f'{t["current_written_questions"]} written</div></div>')
        parts.append('<div class="t-body">')
        parts.append(
            f'<div class="prereq"><b>Prerequisites:</b> {E(t["prerequisites"])} '
            f'&nbsp;&middot;&nbsp; <b>Unlocks:</b> {E(t["unlocks"])}</div>')
        parts.append('<div class="chips">')
        parts.append(f'<span class="chip official">{t["official_syllabus_items"]} '
                     f'official item(s)</span>')
        parts.append(f'<span class="chip">{t["examiner_evidenced_oral"]} '
                     f'examiner-evidenced orals</span>')
        parts.append(f'<span class="chip">{t["distinct_examiners"]} examiners</span>')
        parts.append(f'<span class="chip">{t["current_written_papers"]} papers</span>')
        parts.append(f'<span class="chip">{t["current_written_recurrence_families"]} '
                     f'recurring written families</span>')
        parts.append('</div>')
        parts.append(
            f'<div class="q-more"><a href="topics.html#{tid}">Oral questions for '
            f'this topic &rarr;</a> &nbsp;&middot;&nbsp; '
            f'<a href="/SQ/index.html#solved-qp">Solved written papers &rarr;</a>'
            f'</div>')
        if t['gaps'] != '—':
            parts.append(f'<div class="gaps"><b>Known gaps:</b> {E(t["gaps"])}</div>')
        parts.append('</div></section>')

    parts.append(f'<div class="note"><b>What this roadmap rests on.</b> '
                 f'{E(model["public_claim"])} Historical written question '
                 f'intelligence is <b>{E(hist["status"].replace("_", " ").lower())}</b> '
                 f'and contributes nothing to the figures above; when it is '
                 f'validated these pages will widen by themselves.</div>')
    parts.append('</main>')
    parts.append(
        f'<footer>Official scope: {E(model["official_source"]["circular"])} '
        f'({E(model["official_source"]["issue_date"])}), Annexure III &mdash; '
        f'Syllabus for MEO Class I Preparatory Course. Adopted; it takes effect '
        f'on 2027-01-01 and does not govern earlier sittings.</footer>')
    parts.append('\n</body>\n</html>\n')
    return ''.join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    model, mappings, official, ex = load_all()
    pages = {
        TOPICS_OUT: build_topics_html(model, mappings, official, ex),
        STUDY_OUT: build_study_html(model, official),
    }

    if args.check:
        for path, text in pages.items():
            rel = os.path.relpath(path, ROOT)
            if not os.path.exists(path):
                print(f'FAIL: {rel} is missing')
                return 1
            if open(path, encoding='utf-8', newline='').read() != text:
                print(f'FAIL: {rel} is stale')
                return 1
        print(f'topic pages -- {len(pages)} pages up to date')
        return 0

    for path, text in pages.items():
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
        print(f'wrote {os.path.relpath(path, ROOT)} ({len(text):,} bytes)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
