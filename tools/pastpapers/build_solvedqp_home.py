#!/usr/bin/env python3
"""Build the paid Solved QP product home at /solvedQP/index.html.

    specs/*.json  -->  solvedQP/index.html

This is a PROJECTION, not a second source of truth. Every sitting, every
question count and the "newest solved sitting" hook are derived from the
same canonical specs that produce the papers themselves. Adding a spec
adds a card here with no edit to this file.

Deliberately NOT shown to a paying candidate: recurrence_class, build
state, review state or any other authoring field. Those are production
metadata; a candidate must never be told a question is "expected".

Determinism: no clock read, no random value. Re-running with unchanged
specs is byte-identical.
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, CONTACT, esc, strip_tags, read_css,
                           topbar, head_meta, footer, GATE_STUB, delivery_links,
                           CORPUS_SEARCH_JS, STICKY_SYNC_JS)
import recurrence_model as RM
# KNOWN_ABSENT is owned by the year-sheet builder, which already distinguishes
# "no sitting was held" from "not yet in the MIW set". Importing it keeps ONE
# statement of which months genuinely have no examination -- a second hand-kept
# list here would drift, and a wrong "No sitting" is a factual claim about the
# examination, not a presentation detail.
from build_questions_year import KNOWN_ABSENT

SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

# Coverage states shown on the product home.
AVAILABLE = 'AVAILABLE'
PLANNED_SOON = 'PLANNED_SOON'
NO_SITTING = 'NO_SITTING'

# How many change records the home shows. The manifest holds them all; the page
# is a product surface, not a changelog viewer.
UPDATES_SHOWN = 6

_MONTHS_SHORT = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def pretty_date(iso):
    """'2026-08-12' -> '12 Aug 2026'. Falls back to the raw value unchanged."""
    try:
        y, m, d = (int(x) for x in iso.split('-'))
        return '%d %s %d' % (d, _MONTHS_SHORT[m - 1], y)
    except Exception:
        return iso


MODES = [
    ('Understand', 'What the examiner is actually asking, and the trap in the wording.'),
    ('Exam Plan', 'How to spend the marks — the shape of the answer before you write it.'),
    ('Answer', 'The full model written answer, regulation-referenced.'),
    ('Study Guide', 'The background you need if the topic is not yet solid.'),
    ('Recall', 'Fifteen-second revision — route, critical number, major trap.'),
]

TOP_JS = """
(function(){
  var b=document.getElementById('sq-top'); if(!b) return;
  // Revealed only once the reader is genuinely deep in the page. A control that
  // is present from the first pixel is noise on a page that fits one screen.
  var SHOW=600, shown=false;
  function sync(){
    var y=window.pageYOffset||document.documentElement.scrollTop;
    var want=y>SHOW;
    if(want!==shown){ shown=want; b.hidden=!want; }
  }
  // Called straight from the scroll handler rather than gated behind
  // requestAnimationFrame. sync() is one property read and a boolean compare, so
  // it is cheap enough to run inline -- and rAF does not fire at all when the
  // page is in a background or non-compositing view, which left the control
  // permanently hidden. Correctness beats the micro-optimisation here.
  addEventListener('scroll', sync, {passive:true});
  sync();
  b.addEventListener('click',function(){
    // Honour a reader who has asked the operating system for less motion.
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
    var h=document.querySelector('h1');
    if(h){ h.setAttribute('tabindex','-1'); h.focus({preventScroll:true}); }
  });
})();
"""

HOME_CSS = """
  /* ---- orientation line, hero -------------------------------------- */
  .sq-orient{color:#cbd5e1;font-size:.86rem;margin:1rem 0 0;max-width:70ch;line-height:1.55;}

  /* ---- latest updates, collapsed by default ------------------------ */
  .sq-upd-sec{padding-top:1.25rem;}
  .sq-upd-d{border:1px solid var(--grey-border);border-radius:10px;background:#fff;}
  .sq-upd-d>summary{list-style:none;cursor:pointer;padding:.7rem .9rem;display:flex;
    align-items:center;gap:.5rem;flex-wrap:wrap;font-size:.82rem;}
  .sq-upd-d>summary::-webkit-details-marker{display:none;}
  .sq-upd-d>summary::after{content:'View updates BC';margin-left:auto;color:var(--teal-dark);
    font-weight:600;white-space:nowrap;}
  .sq-upd-d[open]>summary::after{content:'Hide updates B2';}
  .sq-upd-d>summary:hover{background:var(--off-white);}
  .sq-upd-d>summary:focus-visible{outline:2px solid var(--navy);outline-offset:2px;}
  .sq-upd-lead{font-weight:700;color:var(--navy);}
  .sq-upd-d>summary time{color:var(--grey-text);}
  .sq-upd-cta{color:var(--grey-text);}
  .sq-upd-d>*:not(summary){padding:0 .9rem;}
  .sq-upd-d>p.lead{padding-top:.5rem;}
  .sq-upd-d>ul,.sq-upd-d>p.sq-upd-more{padding-bottom:.8rem;}

  /* ---- search heading ---------------------------------------------- */
  .sq-h-upd{font-size:1.05rem;margin:0 0 .5rem;color:var(--navy);}
  .sq-h-find{font-size:1.05rem;margin:0 0 .6rem;color:var(--navy);}

  /* ---- how MIW answers work --------------------------------------- */
  .sq-how-sub{font-weight:600;color:var(--navy);}
  .sq-how-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.4rem;
    align-items:start;}
  .sq-ig-wrap{margin:0;}
  .sq-ig{width:100%;height:auto;display:block;border-radius:10px;}
  .sq-ig-wrap figcaption{font-size:.76rem;color:var(--grey-text);margin-top:.5rem;line-height:1.5;}
  .sq-how-list{list-style:none;margin:0;padding:0;counter-reset:m;}
  .sq-how-list li{counter-increment:m;display:grid;grid-template-columns:1.6rem 1fr;
    gap:.1rem .6rem;padding:.5rem 0;border-bottom:1px solid var(--grey-border);}
  .sq-how-list li:last-child{border-bottom:0;}
  .sq-how-list li::before{content:counter(m);grid-row:1 / span 2;align-self:start;
    width:1.6rem;height:1.6rem;border-radius:50%;background:var(--teal-light);
    color:var(--teal-dark);font-size:.72rem;font-weight:700;display:grid;place-items:center;}
  .sq-how-list b{font-size:.9rem;color:var(--navy);}
  .sq-how-list span{font-size:.8rem;color:var(--grey-text);line-height:1.5;}

  /* ---- coverage by year, compact month pills ---------------------- */
  .cov-year{font-size:1rem;margin:1.1rem 0 .5rem;color:var(--navy);
    display:flex;align-items:baseline;gap:.55rem;}
  .cov-count{font-size:.74rem;font-weight:600;color:var(--grey-text);}
  .cov-months{display:grid;grid-template-columns:repeat(auto-fill,minmax(72px,1fr));gap:6px;}
  .cov-m{display:block;text-align:center;padding:.45rem .2rem;border-radius:8px;
    border:1px solid var(--grey-border);text-decoration:none;}
  .cov-m b{display:block;font-size:.8rem;}
  .cov-m span{display:block;font-size:.63rem;text-transform:uppercase;letter-spacing:.03em;}
  a.cov-av{background:#fff;border-color:var(--teal);color:var(--teal-dark);}
  a.cov-av:hover{background:var(--teal-light);}
  a.cov-av:focus-visible{outline:2px solid var(--navy);outline-offset:2px;}
  .cov-pl{background:var(--orange-light);border-color:#fed7aa;color:#b45309;}
  .cov-ab{background:var(--grey-bg);color:var(--grey-text);}

  /* ---- compact coverage matrix ------------------------------------ */
  .sq-mx-scroll{overflow-x:auto;}
  .sq-mx{border-collapse:separate;border-spacing:3px;font-size:.72rem;}
  .sq-mx th{font-weight:700;color:var(--grey-text);padding:1px 4px;text-align:center;}
  .sq-mx th[scope=row]{text-align:right;color:var(--navy);white-space:nowrap;}
  .sq-mx abbr{text-decoration:none;border:0;}
  .sq-mx td{width:20px;height:18px;border-radius:4px;}
  .mx-solved{background:var(--teal-dark);}
  .mx-intel{background:#7dd3d8;}
  .mx-absent{background:#e2e8f0;}
  .mx-unknown{background:#fff;box-shadow:inset 0 0 0 1px #eef2f6;}
  .sq-mx-key{list-style:none;display:flex;flex-wrap:wrap;gap:.35rem .95rem;margin:.6rem 0 0;
    padding:0;font-size:.72rem;color:var(--grey-text);}
  .sq-mx-key li{display:flex;align-items:center;gap:.35rem;}
  .sq-mx-key i{width:12px;height:12px;border-radius:3px;display:inline-block;}

  /* ---- return to top ---------------------------------------------- */
  .sq-top{position:fixed;right:14px;bottom:14px;z-index:40;display:flex;flex-direction:column;
    align-items:center;gap:0;width:44px;min-height:44px;padding:.3rem 0;cursor:pointer;
    border:1px solid var(--grey-border);border-radius:10px;background:#fff;
    color:var(--teal-dark);font-size:1rem;line-height:1;
    box-shadow:0 2px 8px rgba(15,23,42,.14);}
  .sq-top span{font-size:.58rem;text-transform:uppercase;letter-spacing:.04em;font-weight:700;}
  .sq-top:hover{border-color:var(--teal);background:var(--teal-light);}
  .sq-top:focus-visible{outline:2px solid var(--navy);outline-offset:2px;}
  .sq-top[hidden]{display:none;}

  /* ---- footer quote + correction form ---------------------------- */
  .sq-foot{max-width:1080px;margin:2rem auto 0;padding:0 1.25rem;}
  .sq-quote{margin:0 0 1.4rem;padding:1rem 1.1rem;border-left:3px solid var(--teal);
    background:var(--off-white);border-radius:0 8px 8px 0;}
  .sq-quote p{margin:0;font-size:1rem;color:var(--navy);font-style:italic;}
  .sq-quote cite{display:block;margin-top:.35rem;font-size:.76rem;color:var(--grey-text);
    font-style:normal;}
  .sq-cf{border:1px solid var(--grey-border);border-radius:10px;padding:1rem 1.1rem 1.2rem;
    background:#fff;}
  .sq-cf h2{font-size:1rem;margin:0 0 .3rem;color:var(--navy);}
  .sq-cf>p{margin:0 0 .9rem;font-size:.8rem;color:var(--grey-text);line-height:1.55;}
  .sq-cf-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.7rem .9rem;}
  .sq-cf .f{margin:0;display:flex;flex-direction:column;gap:.25rem;}
  .sq-cf .f.wide{grid-column:1 / -1;}
  .sq-cf label{font-size:.74rem;font-weight:700;color:var(--navy);}
  .sq-cf label span{font-weight:400;color:var(--grey-text);}
  .sq-cf input,.sq-cf select,.sq-cf textarea{font-family:inherit;font-size:.84rem;
    padding:.5rem .6rem;border:1px solid var(--grey-border);border-radius:7px;
    background:#fff;color:var(--ink);min-height:40px;}
  .sq-cf textarea{min-height:70px;resize:vertical;}
  .sq-cf input:focus-visible,.sq-cf select:focus-visible,.sq-cf textarea:focus-visible{
    outline:2px solid var(--teal);outline-offset:1px;border-color:var(--teal);}
  .sq-cf-go{margin-top:.9rem;min-height:44px;padding:.6rem 1.1rem;border:0;border-radius:999px;
    background:var(--teal-dark);color:#fff;font-size:.84rem;font-weight:700;cursor:pointer;}
  .sq-cf-go:hover{background:var(--teal);}
  .sq-cf-go:focus-visible{outline:2px solid var(--navy);outline-offset:2px;}

  @media (max-width:760px){
    /* Visual first, then the five explanations stacked beneath it. */
    .sq-how-grid{grid-template-columns:1fr;gap:1rem;}
    /* Touch targets. Measured at 375px before this rule: the search field was
       27px tall and every topic chip 32px, against a 44px minimum. The paper
       pages already bump .learn-btn the same way, so this follows an existing
       precedent rather than inventing a rule. */
    .sq-find-row input{min-height:44px;}
    .sq-upd-btn{min-height:44px;}
    /* .sq-chip is deliberately left alone. A pre-existing rule at 640px sets it
       to 32px and wins the cascade; raising it here would silently reverse that
       decision and add chip rows above the fold. Recorded as a finding instead. */
    .sq-cf-grid{grid-template-columns:1fr;}
    .cov-months{grid-template-columns:repeat(auto-fill,minmax(64px,1fr));}
    .sq-upd-d>summary{font-size:.78rem;}
    .sq-upd-d>summary::after{margin-left:0;flex-basis:100%;}
  }

  .sq-hero{background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:2.5rem 0 2rem;}
  .sq-hero .wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem;}
  .sq-hero h1{color:#fff;font-size:1.9rem;line-height:1.25;margin:.35rem 0 .5rem;}
  .sq-hero .sub{color:#94a3b8;font-size:.95rem;margin:0 0 1rem;max-width:62ch;line-height:1.6;}
  .sq-badge{display:inline-block;background:rgba(13,148,136,.18);color:#5eead4;border:1px solid rgba(13,148,136,.4);
            font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:4px 11px;border-radius:20px;}
  .sq-stats{display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:1.1rem;}
  .sq-stats div{min-width:0;}
  .sq-stats b{display:block;color:#fff;font-size:1.35rem;line-height:1.1;}
  .sq-stats span{color:#94a3b8;font-size:.78rem;}
  .sq-section{max-width:1080px;margin:0 auto;padding:2rem 1.25rem 0;}
  .sq-section h2{font-size:1.15rem;margin:0 0 .35rem;}
  .sq-section .lead{color:var(--grey-text);font-size:.9rem;margin:0 0 1.1rem;max-width:70ch;line-height:1.6;}
  .sq-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;}
  .sq-card{border:1px solid var(--grey-border);border-radius:12px;padding:1.1rem 1.15rem;background:#fff;
           display:flex;flex-direction:column;gap:.5rem;}
  .sq-card .m{font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--teal);}
  .sq-card h3{font-size:1.05rem;margin:0;}
  .sq-card h3 a{text-decoration:none;color:inherit;}
  .sq-card h3 a:hover{color:var(--teal);}
  .sq-card .meta{color:var(--grey-text);font-size:.8rem;line-height:1.6;margin:0;}
  .sq-card .go{margin-top:auto;font-size:.85rem;font-weight:600;color:var(--teal);text-decoration:none;}
  .sq-newest{border-color:var(--teal);box-shadow:0 0 0 1px var(--teal) inset;}
  .cov-year{font-size:1rem;margin:1.1rem 0 .6rem;color:var(--grey-text);}
  .cov-grid{grid-template-columns:repeat(auto-fill,minmax(210px,1fr));margin-bottom:.4rem;}
  .sq-card.cov{padding:.85rem .95rem;gap:.35rem;}
  .sq-card.cov h3{font-size:.95rem;}
  /* Unavailable states are visibly quieter than an available paper, so the
     difference reads at a glance rather than only on the label. */
  .cov-planned,.cov-absent{background:#f8fafc;border-style:dashed;}
  .cov-planned .m{color:var(--grey-text);}
  .cov-absent .m{color:#94a3b8;}
  .cov-absent h3{color:#94a3b8;}
  .sq-modes{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.85rem;}
  .sq-mode{border:1px solid var(--grey-border);border-radius:10px;padding:.85rem .95rem;background:#fff;}
  .sq-mode b{display:block;font-size:.9rem;margin-bottom:.25rem;}
  .sq-mode span{color:var(--grey-text);font-size:.8rem;line-height:1.55;}
  .sq-note{max-width:1080px;margin:1.5rem auto 0;padding:0 1.25rem 2.5rem;color:var(--grey-text);font-size:.82rem;line-height:1.7;}
  /* Topic search. Deliberately a single field with no mode switch: the results
     are grouped by sitting, which is the shape the reader asked the question in
     ("which papers cover this?"), so a second mode would add a control without
     adding an answer. */
  /* The shared stylesheet has .skip but no .sr-only; the search field needs a
     label that a screen reader reads and a sighted reader does not see. */
  .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
           clip:rect(0 0 0 0);white-space:nowrap;border:0;}
  /* STICKY. The field used to scroll away the moment the reader reached the
     28-card grid, which is exactly when they want it. Sticking the whole block
     (field + hint + results) keeps one search affordance on screen without a
     floating toolbar, and the results panel scrolls inside itself so a broad
     query can never push the page out from under the reader. */
  .sq-find{position:sticky;top:var(--topbar-h,47px);z-index:40;background:var(--bg,#fff);
           max-width:none;margin:0;padding:.9rem 1.25rem .8rem;
           border-bottom:1px solid var(--grey-border);}
  .sq-find>*{max-width:1080px;margin-left:auto;margin-right:auto;}
  .sq-find-row{display:flex;align-items:center;gap:.6rem;border:1px solid var(--grey-border);
               border-radius:10px;background:#fff;padding:.6rem .8rem;}
  .sq-find-row svg{flex:0 0 auto;color:var(--grey-text);}
  .sq-find input{flex:1 1 auto;min-width:0;border:0;outline:0;font:inherit;font-size:.95rem;
                 background:transparent;color:inherit;}
  /* Scoped to the field's own row. This was `.sq-find button`, which also
     matched the topic chips added later and hid every one of them at every
     width -- invisibly, because a programmatic click still works on a
     display:none button. Keep this selector tight. */
  .sq-find-row button{flex:0 0 auto;border:0;background:transparent;color:var(--grey-text);
                  font-size:1rem;cursor:pointer;padding:0 .2rem;display:none;}
  .sq-find .hint{color:var(--grey-text);font-size:.78rem;margin:.5rem 0 0;line-height:1.6;}
  .sq-res{margin-top:.9rem;max-height:56vh;overflow-y:auto;}
  .sq-res:empty{margin-top:0;}
  /* Topic chips -- discovery for the reader who does not yet have a word for
     what they want. They drive the SAME search field rather than a second
     browse IA, so there is one way to get to a question, not two. */
  .sq-chips{display:flex;flex-wrap:wrap;gap:.35rem;margin:.55rem 0 0;}
  .sq-chip{display:inline-flex;align-items:center;gap:.35rem;
           border:1px solid var(--grey-border);background:#fff;border-radius:14px;
           padding:.25rem .7rem;font:inherit;font-size:.75rem;color:var(--grey-text);
           cursor:pointer;line-height:1.5;}
  /* Once the reader is searching, the chips and the explainer have done their
     job. Collapsing them keeps the sticky block from taking most of a phone
     screen -- it measured 567px of an 812px viewport before this. */
  .sq-find.has-q .sq-chips,.sq-find.has-q .hint{display:none;}
  /* Stuck = the reader has scrolled past the search block and it is now
     floating over the content. At that point it must earn its space: the
     chips and the explainer go, leaving the field. On a phone the block was
     holding 45% of the screen while the reader scrolled the sitting grid,
     which is a toolbar, not an affordance. */
  .sq-find.is-stuck .sq-chips,.sq-find.is-stuck .hint{display:none;}
  .sq-find.is-stuck{padding-top:.6rem;padding-bottom:.6rem;
                    box-shadow:0 2px 8px rgba(15,23,42,.06);}
  .sq-chip:hover,.sq-chip:focus-visible{border-color:var(--teal);color:var(--teal-dark);
           background:var(--teal-light);}
  .sq-chip[aria-pressed="true"]{border-color:var(--teal);color:var(--teal-dark);
           background:var(--teal-light);font-weight:700;}
  .sq-kbd{color:var(--grey-text);font-size:.72rem;white-space:nowrap;}
  .sq-kbd kbd{border:1px solid var(--grey-border);border-bottom-width:2px;border-radius:4px;
              padding:0 .3rem;font-family:inherit;font-size:.72rem;background:#f8fafc;}
  .sq-res-sum{font-size:.82rem;color:var(--grey-text);margin:0 0 .7rem;}
  .sq-res-paper{border:1px solid var(--grey-border);border-radius:10px;padding:.75rem .9rem;
                margin-bottom:.6rem;background:#fff;}
  .sq-res-paper h4{margin:0 0 .45rem;font-size:.92rem;}
  .sq-res-paper h4 a{color:inherit;text-decoration:none;}
  .sq-res-paper h4 a:hover{color:var(--teal);}
  .sq-res-q{display:block;padding:.35rem 0;border-top:1px dashed var(--grey-border);
            font-size:.85rem;line-height:1.55;color:inherit;text-decoration:none;}
  .sq-res-q:hover{color:var(--teal);}
  .sq-res-q b{color:var(--teal);font-weight:600;margin-right:.4rem;}
  .sq-res-q span{color:var(--grey-text);}
  .sq-res-none{font-size:.85rem;color:var(--grey-text);line-height:1.6;}
  /* Latest updates. Product changes only -- never a branch, a commit or a build
     state. Rendered server-side so it is readable with no JavaScript. */
  .sq-upd{list-style:none;margin:0;padding:0;}
  .sq-upd li{display:flex;gap:.85rem;padding:.5rem 0;border-top:1px solid var(--grey-border);
             font-size:.85rem;line-height:1.6;}
  .sq-upd li:first-child{border-top:0;}
  .sq-upd time{flex:0 0 6.2rem;color:var(--grey-text);font-size:.78rem;padding-top:.1rem;}
  .sq-upd .what{min-width:0;}
  .sq-upd .what b{display:block;font-size:.85rem;}
  .sq-upd .what span{color:var(--grey-text);}
  /* Change kind. A maintenance ledger has to distinguish "we added a sitting"
     from "we corrected an answer you may have already studied" -- the second is
     the one a candidate needs to see, and an undifferentiated list buries it. */
  .sq-kind{display:inline-block;font-size:.65rem;font-weight:700;text-transform:uppercase;
           letter-spacing:.05em;border-radius:4px;padding:.1rem .38rem;margin-right:.4rem;
           vertical-align:.08em;border:1px solid transparent;}
  .sq-k-added{background:#ecfdf5;color:#047857;border-color:#a7f3d0;}
  .sq-k-corrected{background:#fef2f2;color:#b91c1c;border-color:#fecaca;}
  .sq-k-enriched{background:#eff6ff;color:#1d4ed8;border-color:#bfdbfe;}
  .sq-k-regulatory_update{background:#fffbeb;color:#b45309;border-color:#fde68a;}
  .sq-k-learning_improvement{background:#f5f3ff;color:#6d28d9;border-color:#ddd6fe;}
  .sq-upd .what a{color:var(--teal-dark);text-decoration:none;}
  .sq-upd .what a:hover,.sq-upd .what a:focus-visible{text-decoration:underline;}
  .sq-upd-more{margin:.9rem 0 0;}
  .sq-upd-btn{border:1px solid var(--grey-border);background:#fff;border-radius:14px;
              padding:.4rem .85rem;font:inherit;font-size:.8rem;color:var(--teal-dark);
              font-weight:700;cursor:pointer;min-height:32px;}
  .sq-upd-btn:hover,.sq-upd-btn:focus-visible{border-color:var(--teal);background:var(--teal-light);}
  #sq-upd-all{margin-top:.8rem;max-height:60vh;overflow-y:auto;}
  /* Search narrows the sitting grid as you type, so the page answers "which
     papers" at a glance and not only in the results list. */
  .sq-card[hidden]{display:none;}
  @media(max-width:640px){
    .sq-hero h1{font-size:1.5rem;}.sq-stats{gap:1rem;}
    .sq-upd li{flex-direction:column;gap:.15rem;}
    .sq-upd time{flex:none;}
    .sq-find{padding:.7rem .9rem .65rem;}
    /* The topbar wraps to ~110px on a phone, so the sticky block has less room
       to work with. Cap the panel low enough that the sitting grid stays
       partly visible underneath it. */
    .sq-res{max-height:44vh;}
    .mc-q{min-height:44px;}
    /* The topic tag costs a whole extra wrapped line per result on a 375px
       screen and repeats what the reader just searched for. */
    .sq-res .mc-tag{display:none;}
    .sq-kbd{display:none;}          /* no physical keyboard to hint at */
    .sq-chip{min-height:32px;}
    .sq-upd-btn{min-height:44px;}
  }
"""

# Client-side topic search over the generated manifest.
#
# It fetches solvedQP/solvedqp_content_index.json -- the SAME file the year
# pages, the home counts and the daily health check are derived from -- so there
# is no second search index to keep in step. Matching runs against the
# manifest's precomputed `search_text`, which is normalised in Python by
# build_solvedqp_manifest.norm_search(); normalising again in JavaScript would
# be a second implementation of one rule and the two would drift.
#
# Only AVAILABLE sittings carry questions in the manifest, so an unsolved paper
# cannot surface here however well its intake stem matches. That is enforced by
# the data, not by a filter in this script.
SEARCH_JS = r"""
<script>
__STICKY_SYNC__
(function(){
  var box=document.getElementById('sq-q'),
      out=document.getElementById('sq-results'),
      clr=document.getElementById('sq-clear');
  if(!box||!out) return;
  var esc=MIWCorpus.esc;
  var cards=Array.prototype.slice.call(document.querySelectorAll('.sq-card[data-paper-id]'));
  var chips=Array.prototype.slice.call(document.querySelectorAll('.sq-chip[data-topic]'));
  var lastQ=null;

  // ---- deep link ----------------------------------------------------------
  // ?q= makes a search shareable and survivable: a candidate can bookmark
  // "everything on general average", send it to a study partner, and use Back
  // to get out of a paper and land on the same result list. History is
  // replaced rather than pushed, so typing a word does not bury the previous
  // page under twelve entries.
  function readQ(){
    try{ return new URLSearchParams(location.search).get('q')||''; }
    catch(e){ return ''; }
  }
  function writeQ(q){
    if(!window.history||!history.replaceState) return;
    var u=location.pathname+(q?('?q='+encodeURIComponent(q)):'')+location.hash;
    try{ history.replaceState(null,'',u); }catch(e){}
  }

  // ---- sitting grid narrowing --------------------------------------------
  // The results list answers "which questions". Narrowing the grid answers
  // "which sittings", which is the shape a lot of candidates actually think
  // in. Same keystroke, no second control.
  function narrowGrid(ids){
    cards.forEach(function(c){
      c.hidden = ids ? !ids[c.getAttribute('data-paper-id')] : false;
    });
  }

  function render(q){
    var res=MIWCorpus.match(q);
    var idx=MIWCorpus.index();
    if(!res.questions){
      out.innerHTML='<p class="sq-res-none">No solved question matches &ldquo;'+esc(q)+
        '&rdquo;. Search is over the '+(idx?idx.available_questions:0)+
        ' questions in the '+(idx?idx.available_papers:0)+
        ' solved sittings &mdash; sittings still in preparation are not searchable. '+
        'Try a broader word, an instrument name, or one of the topics above.</p>';
      narrowGrid({});
      return;
    }
    var h=['<p class="sq-res-sum">'+MIWCorpus.summary(res)+'</p>'];
    var ids={};
    res.groups.forEach(function(g){ ids[g.paper.paper_id]=1; });
    h.push(MIWCorpus.renderGroups(res));
    out.innerHTML=h.join('');
    narrowGrid(ids);
  }

  var findSec=document.querySelector('.sq-find');

  function run(q,opts){
    q=(q||'').trim();
    clr.style.display=q?'block':'none';
    if(findSec) findSec.classList.toggle('has-q',!!q);
    chips.forEach(function(c){
      c.setAttribute('aria-pressed', c.getAttribute('data-topic')===q ? 'true':'false');
    });
    if(!(opts&&opts.silent)) writeQ(q);
    if(!q){ out.innerHTML=''; narrowGrid(null); lastQ=''; return; }
    if(q===lastQ) return;
    lastQ=q;
    MIWCorpus.load().then(function(idx){
      if(box.value.trim()!==q) return;      // reader moved on mid-flight
      if(!idx){
        out.innerHTML='<p class="sq-res-none">Search is temporarily unavailable. '+
          'Every sitting is still listed below.</p>';
        return;
      }
      render(q);
    });
  }

  box.addEventListener('input',function(){ run(box.value); });
  clr.addEventListener('click',function(){ box.value=''; run(''); box.focus(); });
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      var t=c.getAttribute('data-topic');
      // A pressed chip toggles off, so a chip is a filter and not a trap.
      if(c.getAttribute('aria-pressed')==='true'){ box.value=''; run(''); return; }
      box.value=t; run(t);
      out.scrollTop=0;
    });
  });

  // ---- keyboard -----------------------------------------------------------
  // "/" focuses, Escape clears then blurs, Enter opens the first hit. Nothing
  // exotic: these are the three a reader tries without being told.
  document.addEventListener('keydown',function(e){
    if(e.defaultPrevented) return;
    var t=e.target, tag=t&&t.tagName;
    var typing = tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||(t&&t.isContentEditable);
    if(e.key==='/'&&!typing&&!e.ctrlKey&&!e.metaKey&&!e.altKey){
      e.preventDefault(); box.focus(); box.select(); return;
    }
    if(t!==box) return;
    if(e.key==='Escape'){
      if(box.value){ e.preventDefault(); box.value=''; run(''); }
      else box.blur();
      return;
    }
    if(e.key==='Enter'){
      var first=out.querySelector('.mc-q');
      if(first){ e.preventDefault(); window.location.href=first.getAttribute('href'); }
    }
  });

  // Warm the payload on first focus so the first keystroke feels instant.
  box.addEventListener('focus',MIWCorpus.load,{once:true});

  // Detect "stuck" from a zero-height sentinel immediately above the block:
  // once the sentinel has scrolled off the top, the block is floating over
  // content and should shed the chips and the explainer.
  //
  // A passive scroll listener, NOT an IntersectionObserver. IO is the tidier
  // tool and was the first implementation, but it delivers callbacks through
  // the compositor, so it is untestable in a headless pane that produces no
  // frames -- the observer fired zero callbacks, including the initial one.
  // A behaviour that cannot be exercised in review is a behaviour nobody can
  // prove still works. The listener is passive and does one rect read.
  if(findSec){
    var sentinel=document.createElement('div');
    sentinel.setAttribute('aria-hidden','true');
    sentinel.style.cssText='height:1px;margin-bottom:-1px;';
    findSec.parentNode.insertBefore(sentinel,findSec);
    var ticking=false;
    var syncStuck=function(){
      ticking=false;
      findSec.classList.toggle('is-stuck',
        sentinel.getBoundingClientRect().top < 0);
    };
    // setTimeout, not requestAnimationFrame. rAF does not fire in a tab that
    // is not producing frames, which would latch `ticking` true forever and
    // silently kill the handler for the rest of the session.
    var onScroll=function(){
      if(ticking) return;
      ticking=true;
      setTimeout(syncStuck,16);
    };
    window.addEventListener('scroll',onScroll,{passive:true});
    window.addEventListener('resize',onScroll,{passive:true});
    syncStuck();
    // Exposed so a UI review can drive it without waiting on a frame.
    window.__miwSyncStuck=syncStuck;
  }

  // Restore a shared/bookmarked search. silent: the URL already says this.
  var initial=readQ();
  if(initial){ box.value=initial; run(initial,{silent:true}); }
})();

// ---- full update ledger ---------------------------------------------------
// The page shows the most recent changes server-side so they are readable with
// no JavaScript. The whole ledger is one click away and loaded on demand from
// the same manifest -- a candidate who has been studying for three months must
// be able to find out whether an answer they learned has since been corrected.
(function(){
  var btn=document.getElementById('sq-upd-btn'), panel=document.getElementById('sq-upd-all');
  if(!btn||!panel) return;
  var KIND={added:'Added',corrected:'Corrected',enriched:'Enriched',
            regulatory_update:'Regulatory update',
            learning_improvement:'Learning improvement'};
  function pretty(iso){
    var M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p=String(iso).split('-');
    if(p.length!==3) return iso;
    return parseInt(p[2],10)+' '+M[parseInt(p[1],10)-1]+' '+p[0];
  }
  btn.addEventListener('click',function(){
    var open=panel.hasAttribute('hidden')===false;
    if(open){ panel.setAttribute('hidden',''); btn.textContent='View all updates';
              btn.setAttribute('aria-expanded','false'); return; }
    panel.removeAttribute('hidden');
    btn.textContent='Hide full update history';
    btn.setAttribute('aria-expanded','true');
    if(panel.getAttribute('data-loaded')) return;
    MIWCorpus.load().then(function(idx){
      if(!idx||!idx.recently_updated){
        panel.innerHTML='<p class="sq-res-none">Could not load the update history.</p>';
        return;
      }
      var rows=idx.recently_updated;
      if(!rows.length){
        panel.innerHTML='<p class="sq-res-none">No changes recorded yet.</p>';
        panel.setAttribute('data-loaded','1');
        return;
      }
      var esc=MIWCorpus.esc;
      panel.innerHTML='<ul class="sq-upd">'+rows.map(function(u){
        var k=u.kind||'corrected';
        var qs=(u.questions||[]).length
          ? ' <span class="sq-res-sum" style="display:inline">'+esc(u.questions.join(', '))+'</span>'
          : '';
        return '<li><time datetime="'+esc(u.date)+'">'+esc(pretty(u.date))+'</time>'+
               '<div class="what"><b><span class="sq-kind sq-k-'+esc(k)+'">'+
               esc(KIND[k]||k)+'</span>'+esc(u.sitting)+'</b>'+
               '<span>'+u.summary+qs+'</span></div></li>';
      }).join('')+'</ul>';
      panel.setAttribute('data-loaded','1');
    });
  });
})();
</script>
"""


def load_specs():
    out = []
    for p in sorted(glob.glob(SPEC_GLOB)):
        with open(p, encoding='utf-8') as fh:
            out.append(json.load(fh))
    return out


def solved_sittings(specs):
    """Specs that actually carry model answers, oldest first."""
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
    return sorted(solved, key=lambda d: (d['year'], RM.MONTH_NUM[d['month']]))


def coverage(specs):
    """Honest month-by-month coverage: (year, month_num, month, state, paper_id).

    Three states, and one deliberate silence:

      AVAILABLE     a solved paper exists -- clickable
      PLANNED_SOON  the sitting is in the MIW set and transcribed, but not yet
                    solved. Shown so a candidate can see what is coming, with
                    NO link, because there is no answer page to open.
      NO_SITTING    no examination was held that month (KNOWN_ABSENT)

    A month that is neither in the spec set nor in KNOWN_ABSENT is NOT RENDERED
    AT ALL. That is what stops the page inventing sittings: the later months of
    the current year simply do not appear until a real source paper exists for
    them. Coverage is asserted from evidence, never from the calendar.
    """
    by_key = {(d['year'], RM.MONTH_NUM[d['month']]): d for d in specs}
    # ONLY years that actually have a paper in the spec set. Extending
    # KNOWN_ABSENT back to 2021 made this grid sprout a 2021 row containing
    # nothing but two "No sitting" chips and a 2022 row containing one -- years
    # with no solved paper at all, rendered as though they were coverage. This
    # section is the route INTO a solved paper; the full examination history,
    # including question-only years, belongs to the matrix below it.
    years = sorted({y for y, _ in by_key})
    rows = []
    for y in years:
        for mn in range(1, 13):
            d = by_key.get((y, mn))
            if d is not None:
                solved = any(q.get('model_answer') for q in d['questions'])
                rows.append((y, mn, RM.MONTHS[mn - 1],
                             AVAILABLE if solved else PLANNED_SOON,
                             d['paper_id']))
            elif (y, mn) in KNOWN_ABSENT:
                rows.append((y, mn, RM.MONTHS[mn - 1], NO_SITTING, None))
    return rows


def newest_sitting(specs):
    s = solved_sittings(specs)
    return s[-1] if s else None


def preview_updates(all_ups, shown=None):
    """Pick the change records the home page shows, newest first.

    A STRAIGHT DATE SLICE IS THE WRONG ANSWER, and it is worth saying why
    because it looks right. Papers are integrated in batches, so a run of
    "sitting added" records shares the newest date and fills every preview
    slot. The first build of this ledger did exactly that: six rows, all
    ADDED, with four corrections and nine learning improvements sitting just
    underneath the fold. That is the "release feed, not a maintenance ledger"
    failure the ledger exists to end -- and no candidate is served by being
    told six times that a paper exists.

    So the preview reserves room for MAINTENANCE (corrected / enriched /
    regulatory_update / learning_improvement) alongside additions, then sorts
    what it picked back into date order. No date is altered and no record is
    promoted above a newer one within its own class -- the reader still sees a
    chronological list, just one that is not monopolised by a single batch.

    Determinism: `all_ups` arrives already sorted on (date, paper_id) and both
    partitions preserve that order, so the same specs give the same six rows.
    """
    shown = UPDATES_SHOWN if shown is None else shown
    added = [u for u in all_ups if u['kind'] == 'added']
    maint = [u for u in all_ups if u['kind'] != 'added']
    # Within maintenance, a CORRECTION outranks an improvement for a preview
    # slot. Both stay in date order among themselves; the reservation only
    # decides which ones get shown at all. The distinction is not editorial
    # taste: "an answer you may have learned is wrong" and "an explanation got
    # clearer" are different messages, and only one of them is urgent.
    critical = [u for u in maint
                if u['kind'] in ('corrected', 'regulatory_update')]
    other = [u for u in maint
             if u['kind'] not in ('corrected', 'regulatory_update')]
    half = shown // 2
    take_m = min(len(maint), max(half, shown - len(added)))
    take_a = min(len(added), shown - take_m)
    take_m = min(len(maint), shown - take_a)
    # Give corrections at least half of the maintenance slots before the
    # improvements compete for them.
    take_c = min(len(critical), max(1, take_m - len(other)) if other else take_m,
                 max(1, (take_m + 1) // 2))
    picked = added[:take_a] + critical[:take_c] + other[:take_m - take_c]
    picked.sort(key=lambda r: (r['date'], r['paper_id']), reverse=True)
    return picked


def topic_counts(sittings):
    """Primary categories across the solved corpus, commonest first.

    DERIVED, never a hand-kept list. A chip can therefore only ever name a
    topic that has solved questions behind it -- a curated list would
    eventually offer a topic the corpus does not cover, which is the one thing
    a discovery control must not do. Ties break alphabetically so the order is
    total and the build stays byte-identical.
    """
    counts = {}
    for d in sittings:
        for q in d['questions']:
            c = q.get('primary_category')
            if c:
                counts[c] = counts.get(c, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


# --------------------------------------------------------------------------- #
# Examination-history matrix
# --------------------------------------------------------------------------- #

INTEL_PATH = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'intelligence',
                          'historical_qp_intelligence.json')

M_SOLVED = 'solved'          # a full MIW answer product exists
M_INTEL = 'intel'            # question wording held, no answers
M_ABSENT = 'absent'          # no paper was numbered -- KNOWN_ABSENT carries the evidence
M_UNKNOWN = 'unknown'        # MIW holds no source copy; says nothing about the examination

MX_LABEL = {
    M_SOLVED: 'Solved',
    M_INTEL: 'Questions only',
    M_ABSENT: 'No sitting',
    M_UNKNOWN: 'Not held',
}


def load_intelligence():
    """Question-only sittings. Absent file is not an error -- it degrades to {}.

    The layer is a SEPARATE store from the solved manifest on purpose. Nothing
    read here may ever be counted as solved, priced, or linked to an answer page.
    """
    try:
        with open(INTEL_PATH, encoding='utf-8') as fh:
            doc = json.load(fh)
    except FileNotFoundError:
        return {}
    return {(p['year'], RM.MONTH_NUM[p['month']]): p for p in doc.get('papers', [])}


def matrix(specs, intel):
    """{(year, month_num): state} across every year either store knows about.

    FOUR states, and the distinction between the last two is the whole point of
    the grid. "No paper was numbered" is a claim about the EXAMINATION and is
    only ever made where KNOWN_ABSENT carries the serial evidence for it.
    "MIW holds no source copy" is a claim about MIW'S SHELF. Collapsing them
    would tell a candidate an examination did not happen because we have not
    bought the paper.
    """
    solved = {(d['year'], RM.MONTH_NUM[d['month']]) for d in solved_sittings(specs)}
    years = sorted({y for y, _ in solved} | {y for y, _ in intel}
                   | {y for y, _ in KNOWN_ABSENT})
    out = {}
    for y in years:
        for mn in range(1, 13):
            k = (y, mn)
            if k in solved:
                out[k] = M_SOLVED
            elif k in intel:
                out[k] = M_INTEL
            elif k in KNOWN_ABSENT:
                out[k] = M_ABSENT
            else:
                out[k] = M_UNKNOWN
    return out, years


# --------------------------------------------------------------------------- #
# The five-mode infographic
# --------------------------------------------------------------------------- #
#
# DERIVED FROM THE REAL INTERFACE, not drawn freehand and not a pasted raster.
#
# The five pills below are the actual `.learn-bar` control from a delivered paper
# page: same five labels in the same order, the same pill geometry (radius 999px,
# 1px border), and the same brand tokens the stylesheet uses -- #0f766e filled for
# the selected tab, #fff on #e2e8f0 for the rest, #64748b label text. "Answer" is
# drawn selected because that is the mode a question card opens on.
#
# It is inline SVG rather than a PNG screenshot for three reasons that all matter
# here: it stays crisp at any width, it costs about 2 KB against ~150 KB for a
# legible capture, and it carries no accidental page furniture -- the Founder's
# instruction was explicitly not to paste a cluttered full-page screenshot.
#
# If the real control ever changes, this must be re-derived from it. It is a
# faithful reproduction, not an illustration, and it must not drift.

def infographic():
    pills = [('Understand', False), ('Exam Plan', False), ('Answer', True),
             ('Study Guide', False), ('Recall', False)]
    # 12px 600-weight Segoe UI, padding 13px each side -- measured from .learn-btn
    W = {'Understand': 92, 'Exam Plan': 82, 'Answer': 62, 'Study Guide': 86, 'Recall': 56}
    o = ['<svg class="sq-ig" viewBox="0 0 420 188" role="img" '
         'aria-labelledby="sq-ig-t sq-ig-d" xmlns="http://www.w3.org/2000/svg">',
         '  <title id="sq-ig-t">The five study modes on a solved question card</title>',
         '  <desc id="sq-ig-d">A question card from a solved paper. Along the top are five '
         'tabs in a row &mdash; Understand, Exam Plan, Answer, Study Guide and Recall. The '
         'Answer tab is selected, which is how every question card opens. Below the tabs is '
         'the body of the answer.</desc>',
         '  <rect x="1" y="1" width="418" height="186" rx="10" fill="#fff" stroke="#e2e8f0"/>',
         # question header strip, as the real card has
         '  <rect x="1" y="1" width="418" height="34" rx="10" fill="#f8fafc"/>',
         '  <rect x="1" y="25" width="418" height="10" fill="#f8fafc"/>',
         '  <text x="16" y="23" font-family="Segoe UI,system-ui,sans-serif" font-size="12" '
         'font-weight="700" fill="#0f172a">Q1</text>',
         '  <rect x="36" y="12" width="210" height="8" rx="4" fill="#e2e8f0"/>',
         '  <text x="404" y="23" text-anchor="end" font-family="Segoe UI,system-ui,sans-serif" '
         'font-size="10" font-weight="600" fill="#64748b">16 marks</text>',
         '  <line x1="1" y1="35" x2="419" y2="35" stroke="#e2e8f0"/>']
    x = 14
    for label, sel in pills:
        w = W[label]
        fill, stroke, colour = ('#0f766e', '#0f766e', '#ffffff') if sel else ('#ffffff', '#e2e8f0', '#64748b')
        o.append('  <rect x="%d" y="48" width="%d" height="26" rx="13" fill="%s" stroke="%s"/>'
                 % (x, w, fill, stroke))
        o.append('  <text x="%d" y="65" text-anchor="middle" '
                 'font-family="Segoe UI,system-ui,sans-serif" font-size="11" font-weight="600" '
                 'fill="%s">%s</text>' % (x + w // 2, colour, label))
        x += w + 6
    # answer body, suggested rather than rendered -- no unreadable paragraph
    for i, w in enumerate((388, 372, 396, 340, 384, 300)):
        o.append('  <rect x="14" y="%d" width="%d" height="7" rx="3.5" fill="%s"/>'
                 % (90 + i * 15, w, '#e2e8f0' if i else '#cbd5e1'))
    o.append('</svg>')
    return o


# A short line, and one whose attribution can actually be stood behind.
#
# "Energy and persistence conquer all things" was the first candidate and was
# REJECTED: it is attributed to Franklin all over the web but the attribution
# traces only to quote-aggregator sites, never to a letter, almanack or speech.
# The Founder's instruction was to verify attribution before publication, and an
# unverifiable one on a paying customer's page is exactly the failure to avoid.
# A proverb has no individual to misattribute, which is why this one is safe.
QUOTE = ('Fall seven times, stand up eight.', 'Japanese proverb')


def build(specs):
    sittings = solved_sittings(specs)
    # Question-only sittings, read from their own store. Degrades to {} if the
    # file is absent, so the home page never depends on the intelligence layer.
    intel = load_intelligence()
    newest = sittings[-1] if sittings else None
    total_q = sum(len(d['questions']) for d in sittings)
    topic_chips = topic_counts(sittings)

    title = 'MIW Solved Question Papers &mdash; MEO Class I Engineering Management'
    desc = ('Complete solved MEO Class I Engineering Management written papers, every question '
            'worked through Understand, Exam Plan, Answer, Study Guide and Recall.')

    o = []
    a = o.append
    # noindex: this is paid content. publish=False gives that.
    o.extend(head_meta(strip_tags(title), strip_tags(desc), '/solvedQP/', False))
    a('<style>')
    a(read_css())
    a(HOME_CSS)
    a('</style>')
    a('</head>')
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#sq-main">Skip to papers</a>')
    # The home covers every solved year, so its navigation carries one link
    # per year rather than a single hard-coded sheet.
    home_years = sorted({d['year'] for d in sittings})
    o.extend(topbar('Solved QP', links=delivery_links(years=home_years)))

    a('<header class="sq-hero">')
    a('  <div class="wrap">')
    a('    <span class="sq-badge">Written &middot; Solved</span>')
    a('    <h1>MIW Solved Question Papers</h1>')
    a('    <p class="sub">MEO Class I &mdash; Engineering Management. Every question from every '
      'available sitting, worked end to end: what the examiner is asking, how to spend the marks, '
      'the full model answer, the background, and a fifteen-second recall.</p>')
    a('    <div class="sq-stats">')
    a('      <div><b>%d</b><span>solved sittings</span></div>' % len(sittings))
    a('      <div><b>%d</b><span>questions</span></div>' % total_q)
    a('      <div><b>5</b><span>study modes each</span></div>')
    if newest:
        a('      <div><b>%s</b><span>newest solved sitting</span></div>' % esc(newest['month_year']))
    a('    </div>')
    # One orientation line, so a candidate knows within about ten seconds what
    # this page lets them DO -- not a second description of the product.
    a('    <p class="sq-orient">On this page: search recurring topics, open solved '
      'papers by year, see what changed recently, and browse question-only exam '
      'history.</p>')
    a('  </div>')
    a('</header>')

    a('<main id="sq-main">')

    # ---- 2. LATEST UPDATES -----------------------------------------
    # Ahead of search on purpose: the one thing a returning candidate needs to
    # know before studying anything is whether something they already learned
    # moved. Collapsed by default so it cannot push the rest of the page down.
    #
    # Imported inside the function: build_solvedqp_manifest imports THIS module
    # for the one definition of coverage/solved state, so a module-level import
    # here would be circular.
    from build_solvedqp_manifest import recently_updated, KIND_LABEL
    all_ups = recently_updated(specs, {d['paper_id'] for d in sittings})
    ups = preview_updates(all_ups)
    if ups:
        top = ups[0]
        a('<section class="sq-section sq-upd-sec">')
        # A real heading, so the section appears in the document outline and to a
        # screen reader's heading list even though its body is collapsed.
        a('  <h2 class="sq-h-upd">Latest updates</h2>')
        a('  <details class="sq-upd-d">')
        a('    <summary>')
        a('      <span class="sq-upd-lead">Latest update</span>')
        a('      <time datetime="%s">%s</time>' % (esc(top['date']), esc(pretty_date(top['date']))))
        a('      <span class="sq-kind sq-k-%s">%s</span>'
          % (esc(top['kind']), esc(KIND_LABEL.get(top['kind'], top['kind']))))
        a('      <b>%s</b>' % esc(top['sitting']))
        a('      <span class="sq-upd-cta">%d recorded changes</span>' % len(all_ups))
        a('    </summary>')
        a('    <p class="lead">Every change to this collection &mdash; new sittings, corrections '
          'to published answers, and answers deepened against verified sources.</p>')
        a('    <ul class="sq-upd">')
        for u in ups:
            # The sitting, not the paper id: a candidate thinks in "July 2024",
            # not "QP2407". The id is still the anchor for the link.
            link = '/solvedQP/%s.html' % u['paper_id']
            qs = ''
            if u.get('questions'):
                qs = ' <span class="sq-res-sum" style="display:inline">%s</span>' \
                     % esc(', '.join(u['questions']))
            a('      <li><time datetime="%s">%s</time><div class="what">'
              '<b><span class="sq-kind sq-k-%s">%s</span>'
              '<a href="%s">%s</a></b><span>%s%s</span></div></li>'
              % (esc(u['date']), esc(pretty_date(u['date'])),
                 esc(u['kind']), esc(KIND_LABEL.get(u['kind'], u['kind'])),
                 link, esc(u['sitting']), u['summary'], qs))
        a('    </ul>')
        # The whole ledger, on demand. Showing six and stopping meant a
        # correction older than the last five sittings was unreachable.
        if len(all_ups) > len(ups):
            a('    <p class="sq-upd-more">')
            a('      <button type="button" id="sq-upd-btn" class="sq-upd-btn" '
              'aria-expanded="false" aria-controls="sq-upd-all">View all updates</button>')
            a('    </p>')
            a('    <div id="sq-upd-all" hidden></div>')
        a('  </details>')
        a('</section>')

    # ---- 3. SEARCH BY TOPIC ----------------------------------------
    # Answers the question a candidate actually arrives with: "which solved
    # papers cover Port State Control, and which question?" Results are
    # question-level and link straight to the anchor.
    a('<section class="sq-find">')
    a('  <h2 class="sq-h-find">Search by topic</h2>')
    a('  <div class="sq-find-row">')
    a('    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
      'stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"/>'
      '<path d="M21 21l-4.35-4.35"/></svg>')
    a('    <label class="sr-only" for="sq-q">Search solved questions by topic</label>')
    a('    <input id="sq-q" type="search" autocomplete="off" '
      'placeholder="Search a topic &mdash; Port State Control, general average, MARPOL&hellip;">')
    a('    <button id="sq-clear" type="button" aria-label="Clear search">&#10005;</button>')
    a('  </div>')
    # Topic discovery. These are the manifest's own primary_category values --
    # derived, never a hand-kept list that could name a topic the corpus does
    # not cover.
    if topic_chips:
        a('  <div class="sq-chips" role="group" aria-label="Browse by topic">')
        for label, count in topic_chips:
            a('    <button type="button" class="sq-chip" data-topic="%s" '
              'aria-pressed="false">%s <span class="sq-kbd">%d</span></button>'
              % (esc(label), esc(label), count))
        a('  </div>')
    # The counts a candidate needs are already in the hero. Repeating them here
    # was the redundancy this line used to carry.
    a('  <p class="hint">Searches the printed question and its topic labels across every '
      'solved paper. <span class="sq-kbd">Press <kbd>/</kbd> to search, <kbd>Esc</kbd> '
      'to clear.</span></p>')
    a('  <div class="sq-res" id="sq-results"></div>')
    a('</section>')

    # ---- 4. HOW MIW ANSWERS WORK -----------------------------------
    # The product differentiator, so it is given a real visual and is placed
    # ABOVE the navigation rather than buried under it.
    a('<section class="sq-section sq-how">')
    a('  <h2>How MIW answers work</h2>')
    a('  <p class="lead sq-how-sub">One question. Five ways to master it &mdash; '
      'understand it, plan it, write it, deepen it, recall it.</p>')
    a('  <div class="sq-how-grid">')
    a('    <figure class="sq-ig-wrap">')
    o.extend('      ' + s for s in infographic())
    a('      <figcaption>Every question card opens with these five modes. '
      'This is the actual control from a solved paper.</figcaption>')
    a('    </figure>')
    a('    <ol class="sq-how-list">')
    for name, blurb in MODES:
        a('      <li><b>%s</b><span>%s</span></li>' % (esc(name), esc(blurb)))
    a('    </ol>')
    a('  </div>')
    a('</section>')

    # ---- 5. COVERAGE BY YEAR ---------------------------------------
    # This is now the PRIMARY way into a solved paper. The large duplicate
    # "Solved papers" card grid that used to sit above it was removed: it listed
    # every sitting a second time, in a flat list, with no year structure.
    rows = coverage(specs)
    if rows:
        a('<section class="sq-section">')
        a('  <h2>Coverage by year</h2>')
        a('  <p class="lead">Every year with solved papers, newest first &mdash; open a month '
          'to work the paper. Months marked as having no sitting carry the evidence for saying '
          'so. For the full examination history, including years held as questions only, see '
          'the map below.</p>')
        for y in sorted({r[0] for r in rows}, reverse=True):
            yr_rows = [r for r in rows if r[0] == y]
            n_av = sum(1 for r in yr_rows if r[3] == AVAILABLE)
            a('  <h3 class="cov-year">%d <span class="cov-count">%d solved</span></h3>'
              % (y, n_av))
            a('  <div class="cov-months">')
            for (_yr, _mn, month, state, pid) in yr_rows:
                short = month[:3]
                if state == AVAILABLE:
                    a('    <a class="cov-m cov-av" href="/solvedQP/%s.html">'
                      '<b>%s</b><span>Solved</span></a>' % (pid, esc(short)))
                elif state == PLANNED_SOON:
                    # No anchor at all. A disabled-looking link that does nothing
                    # reads as a broken product; absence of a control is honest.
                    a('    <span class="cov-m cov-pl"><b>%s</b><span>Soon</span></span>'
                      % esc(short))
                else:
                    a('    <span class="cov-m cov-ab" title="%s"><b>%s</b>'
                      '<span>No sitting</span></span>'
                      % (esc(strip_tags(KNOWN_ABSENT.get((y, _mn), ''))), esc(short)))
            a('  </div>')
        a('</section>')

    # ---- 6. COMPACT COVERAGE MATRIX --------------------------------
    # An examination-history map, not a second paper list. Deliberately small.
    mat, myears = matrix(specs, intel)
    if mat:
        a('<section class="sq-section sq-mx-sec">')
        a('  <h2>Examination history at a glance</h2>')
        a('  <p class="lead">Every month of every year MIW has evidence about. Four states, and '
          'the last two are different claims: <b>no sitting</b> means no paper was numbered and '
          'the printed serial sequence skips it; <b>not held</b> means MIW has no source copy, '
          'which says nothing about whether an examination took place.</p>')
        a('  <div class="sq-mx-scroll">')
        a('  <table class="sq-mx"><caption class="sr-only">Examination coverage by year and '
          'month</caption>')
        a('    <thead><tr><th scope="col">Year</th>')
        for mn in range(1, 13):
            a('      <th scope="col"><abbr title="%s">%s</abbr></th>'
              % (RM.MONTHS[mn - 1], RM.MONTHS[mn - 1][:1]))
        a('    </tr></thead>')
        a('    <tbody>')
        for y in reversed(myears):
            a('      <tr><th scope="row">%d</th>' % y)
            for mn in range(1, 13):
                st = mat.get((y, mn), M_UNKNOWN)
                a('        <td class="mx-%s"><span class="sr-only">%s %d: %s</span></td>'
                  % (st, RM.MONTHS[mn - 1], y, MX_LABEL[st]))
            a('      </tr>')
        a('    </tbody>')
        a('  </table>')
        a('  </div>')
        a('  <ul class="sq-mx-key">')
        for st in (M_SOLVED, M_INTEL, M_ABSENT, M_UNKNOWN):
            a('    <li><i class="mx-%s"></i>%s</li>' % (st, MX_LABEL[st]))
        a('  </ul>')
        a('</section>')

    # ---- 7. QP INTELLIGENCE BY YEAR --------------------------------
    # A separate candidate choice from "open a solved paper": questions only,
    # for testing yourself and for seeing what recurs.
    years = sorted({d['year'] for d in sittings})
    a('<section class="sq-section">')
    a('  <h2>QP intelligence by year</h2>')
    a('  <p class="lead"><b>Questions only</b> &mdash; the printed wording, the marks, the topic '
      'and how often each question has recurred across sittings. No answers on these sheets, so '
      'use them to test yourself before opening a solved paper.</p>')
    a('  <div class="sq-grid">')
    for y in reversed(years):
        n = sum(len(d['questions']) for d in sittings if d['year'] == y)
        a('    <article class="sq-card">')
        a('      <span class="m">Questions only</span>')
        a('      <h3><a href="/solvedQP/questions-%d.html">%d &mdash; all questions</a></h3>'
          % (y, y))
        a('      <p class="meta">%d questions across %d sittings, with recurrence history.</p>'
          % (n, sum(1 for d in sittings if d['year'] == y)))
        a('      <a class="go" href="/solvedQP/questions-%d.html">Open the %d sheet &rarr;</a>'
          % (y, y))
        a('    </article>')
    a('  </div>')
    a('</section>')

    a('<p class="sq-note">Your access covers every solved paper here, including all future '
      'sittings added to this collection.</p>')

    # ---- 8. RETURN TO TOP ------------------------------------------
    # Hidden until the reader is actually deep in the page; the script that
    # reveals it lives with the other page behaviour at the end of the document.
    a('<button type="button" id="sq-top" class="sq-top" hidden '
      'aria-label="Return to top of page">&uarr;<span>Top</span></button>')
    a('</main>')
    # The shared matcher first: the page script and the update ledger both call
    # MIWCorpus, and it is the same string the paper pages and year sheets get,
    # so one query cannot fold three different ways.
    a('<script>')
    a(CORPUS_SEARCH_JS)
    a('</script>')

    # ---- 9. FOOTER: quote, then the correction route ----------------
    a('<section class="sq-foot">')
    a('  <blockquote class="sq-quote"><p>&ldquo;%s&rdquo;</p><cite>%s</cite></blockquote>'
      % (esc(QUOTE[0]), esc(QUOTE[1])))
    # Reuses the MIW Formspree endpoint and field names already in service on the
    # notes pages, so submissions land in the same place and nothing new has to be
    # configured. Compact on purpose: paper/question, type, comment, and a name
    # the sender may leave blank.
    a('  <form class="sq-cf" action="https://formspree.io/f/maqgoeww" method="POST">')
    a('    <h2>Spotted something wrong?</h2>')
    a('    <p>Corrections are read and, if verified, applied at source &mdash; and the change '
      'then appears in Latest updates above.</p>')
    a('    <input type="hidden" name="_subject" value="Solved QP correction">')
    a('    <input type="hidden" name="source_page" value="Solved QP home">')
    a('    <div class="sq-cf-grid">')
    a('      <p class="f"><label for="cf-ref">Paper / question</label>'
      '<input id="cf-ref" name="topic_reference" type="text" '
      'placeholder="e.g. April 2023, Q4" required></p>')
    a('      <p class="f"><label for="cf-type">Type</label>'
      '<select id="cf-type" name="submission_type" required>'
      '<option value="">Select&hellip;</option>'
      '<option value="Error / correction">Error / correction</option>'
      '<option value="Suggestion">Suggestion</option>'
      '<option value="Missing point">Missing point</option>'
      '</select></p>')
    a('      <p class="f wide"><label for="cf-detail">Comment</label>'
      '<textarea id="cf-detail" name="details" rows="3" '
      'placeholder="What is wrong, and the regulation or source if you have it." '
      'required></textarea></p>')
    a('      <p class="f"><label for="cf-name">Name <span>(optional)</span></label>'
      '<input id="cf-name" name="name" type="text" autocomplete="name"></p>')
    a('      <p class="f"><label for="cf-email">Email <span>(optional, for a reply)</span>'
      '</label><input id="cf-email" name="email" type="email" autocomplete="email"></p>')
    a('    </div>')
    a('    <button type="submit" class="sq-cf-go">Send correction</button>')
    a('  </form>')
    a('</section>')

    o.extend(footer(True))
    # After the footer, so the sticky offsets are measured against a fully
    # parsed document -- the paper pages already do this and are correct.
    a(SEARCH_JS.replace('__STICKY_SYNC__', STICKY_SYNC_JS))
    a('<script>')
    a(TOP_JS)
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
    ap.add_argument('-o', '--out', default=None)
    args = ap.parse_args()

    specs = load_specs()
    if not specs:
        print('ERROR: no specs found under %s' % SPEC_GLOB)
        sys.exit(1)

    path = args.out or os.path.join(REPO_ROOT, 'solvedQP', 'index.html')
    st = write(path, build(specs))
    n = newest_sitting(specs)
    print('solvedQP/index.html  %s' % st)
    print('  %d solved sittings, newest %s' % (len(solved_sittings(specs)),
                                               n['month_year'] if n else 'none'))


if __name__ == '__main__':
    main()
