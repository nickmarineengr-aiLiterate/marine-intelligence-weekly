"""Examiner Index V2 - deterministic generator.

Implements EXAMINER_INDEX_V2_GENERATOR_SPEC.md (approved by the Laptop final
release review f78e2c7 sJ). One resolved canonical snapshot drives BOTH
candidate surfaces:

    meoclass1/examiner-index.html   the full, gated candidate index
    SQ/examiner-index.html          the public storefront teaser
    SQ/index.html                   ONE card only: the examiner-index sample
                                    card's description and examiner tags

and is itself written as EXAMINER_INDEX_SNAPSHOT.json so a validator can
prove the two pages and the data agree.

Inputs (records, never a rendered page)
--------------------------------------
  live QB HTML                         question text, anchor, url; parsed on
                                       every run through oral_lib. Display
                                       text is never stored.
  EXAMINER_ALIAS_REGISTER.json         the examiner universe and slugs
  CURRENT_EXAMINER_RELATIONSHIPS.jsonl the 862 published relationships with
                                       research_best_tier = the approved
                                       honest re-tiering
  QB card data-examiner attributes     a page-declared attribution authored
                                       on the card itself (EXPLICIT_QCARD)
  RELEASE_A_PUBLICATION.json           the finalised Release A: new
                                       relationships, and evidence that
                                       merges into existing ones
  STRONG_CE_TIP_REVIEW_DECISIONS.json  human/evidence review of the ten
                                       Release-A pairs held below the floor
                                       on CE-tip prose; APPROVE_* rows only,
                                       at their decided candidate tier
  examiner_index_config.json           prose and tier policy; no numbers

Rules the spec makes non-negotiable and this file enforces
----------------------------------------------------------
  * every count is len() of the records rendered - header total, mini-nav
    pill, section count, tier sub-count, teaser stat. No literal anywhere.
  * a relationship renders once; evidence collapses into it.
  * an unresolvable relationship, an empty display text, an examiner without
    a slug, a tier without a policy entry, or a tier literal without a filter
    toggle is a BUILD FAILURE, not a skipped row.
  * output bytes are LF, contain no timestamp, and are identical across
    PYTHONHASHSEED values.

Portability: repo-relative through oral_lib (ORAL_REPO_ROOT overrides).
    PYTHONIOENCODING=utf-8 python tools/oral/build_examiner_index.py [--check]
--check builds every governed artefact in memory, compares the bytes with
what is on disk, runs the semantic validator, and writes NOTHING. It exits
0 only when every artefact is byte-current AND validation passes
(3 = stale/missing output, 1 = semantic failure, 2 = build failure).
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

HERE = Path(__file__).resolve().parent
TPL = HERE / "templates"
OUT = L.OUT
INDEX_PATH = L.MEO / "examiner-index.html"
SQ_PATH = L.REPO / "SQ" / "examiner-index.html"
SQ_HOME_PATH = L.REPO / "SQ" / "index.html"
SNAPSHOT_NAME = "EXAMINER_INDEX_SNAPSHOT.json"

CONFIG = json.loads((HERE / "examiner_index_config.json").read_text(encoding="utf-8"))
TIERS = CONFIG["tiers"]
TIER_ORDER = sorted(TIERS, key=lambda t: -TIERS[t]["rank"])
R2L = CONFIG["research_tier_to_literal"]


class BuildFailure(Exception):
    pass


def fail(msg):
    raise BuildFailure(msg)


def esc(s):
    return html.escape(s, quote=True)


def natural_file_key(fname):
    """QB1_A.html < QB1_B.html < QB1_supplementary.html < QB2_A.html < QB10_A.html"""
    parts = re.split(r"(\d+)", fname)
    return [int(p) if p.isdigit() else p for p in parts]


# ------------------------------------------------------------------ inputs

def jl(name):
    with (OUT / name).open(encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def js(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def card_attributions():
    """(examiner_name, canonical_question_id) declared on a QB card via
    data-examiner=... . A page-declared attribution: EXPLICIT_QCARD tier."""
    out = []
    for p in L.qb_files():
        h = p.read_text(encoding="utf-8", errors="replace")
        for m in L.CARD.finditer(h):
            attrs = dict(L.ATTR.findall(m.group(1)))
            ex = attrs.get("data-examiner")
            cid = attrs.get("id", "")
            if ex and re.fullmatch(r"q\d+", cid):
                out.append((ex.strip(), p.stem + "#" + cid,
                            attrs.get("data-examiner-confidence", "")))
    return out


REVIEW_NAME = "STRONG_CE_TIP_REVIEW_DECISIONS.json"
# outcome -> the only candidate tier literal that outcome may publish at
REVIEW_OUTCOME_TIER = {
    "APPROVE_CE_TIP_RELATIONSHIP": "ce_tip",
    "APPROVE_REPORTED_RELATIONSHIP": "reported",
    "APPROVE_CONFIRMED_RELATIONSHIP": "confirmed",
}
REVIEW_HOLD_OUTCOMES = {"HOLD_WEAK_ASSERTION", "HOLD_TARGET_AMBIGUOUS",
                        "REJECT_WRONG_MATCH"}


def review_approved_ce_tip():
    """APPROVE_* rows of the strong CE-tip review, structurally checked.

    The generator refuses (BuildFailure) rather than skips: a decision with an
    unknown outcome, an approved row without evidence ids, a candidate tier
    that is not the one its outcome permits, or a target that does not name
    its own relation. Evidence resolution and wording pinning are proven by
    validate_ce_tip_review.py; here the build only refuses to publish what is
    malformed on its face."""
    p = OUT / REVIEW_NAME
    if not p.exists():
        return []
    dec = json.loads(p.read_text(encoding="utf-8"))
    out, seen = [], set()
    for d in dec["decisions"]:
        rid = d["relation_id"]
        if rid in seen:
            fail("duplicate relation in %s: %s" % (REVIEW_NAME, rid))
        seen.add(rid)
        outcome = d["decision"]
        if outcome in REVIEW_HOLD_OUTCOMES:
            if d.get("candidate_tier"):
                fail("held/rejected review row %s carries a candidate tier" % rid)
            continue
        if outcome not in REVIEW_OUTCOME_TIER:
            fail("unknown review outcome %r on %s" % (outcome, rid))
        allowed = REVIEW_OUTCOME_TIER[outcome]
        if d.get("candidate_tier") != allowed:
            fail("review row %s: outcome %s may only publish at %r, got %r"
                 % (rid, outcome, allowed, d.get("candidate_tier")))
        if allowed not in TIERS:
            fail("review tier literal %r has no policy entry (%s)" % (allowed, rid))
        if not d.get("evidence_ids"):
            fail("approved review row %s carries no evidence ids" % rid)
        qid = d["canonical_question_id"]
        tgt = d.get("reviewed_target") or {}
        if (qid != "%s#%s" % (Path(tgt.get("file", "")).stem, tgt.get("anchor"))
                or rid != "RELA-%s-%s" % (d["examiner"].upper(), qid.replace("#", "-"))):
            fail("review row %s: target/relation id mismatch (%s, %s)" % (rid, qid, tgt))
        out.append(d)
    return out


# ---------------------------------------------------------------- resolve

def resolve_snapshot():
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()
    reg = js("EXAMINER_ALIAS_REGISTER.json")
    examiners = {e["canonical_name"]: e for e in reg["examiners"]}

    def literal_of(research_tier, where):
        lit = R2L.get(research_tier)
        if lit is None:
            fail("no candidate tier policy for research tier %r (%s)"
                 % (research_tier, where))
        if lit not in TIERS:
            fail("tier literal %r has no policy entry (%s)" % (lit, where))
        return lit

    rels = {}   # (examiner, qid) -> record

    def upsert(examiner, qid, literal, source, ref, evidence_n):
        key = (examiner, qid)
        r = rels.get(key)
        if r is None:
            r = rels[key] = {
                "examiner": examiner, "canonical_question_id": qid,
                "tier": literal, "sources": [], "refs": [], "evidence_count": 0,
            }
        elif TIERS[literal]["rank"] > TIERS[r["tier"]]["rank"]:
            r["tier"] = literal
        r["sources"].append(source)
        r["refs"].append(ref)
        r["evidence_count"] += evidence_n

    # 1. the published universe, at its approved honest tier
    for r in jl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl"):
        upsert(r["examiner"], r["question_id"],
               literal_of(r["research_best_tier"], r["relationship_id"]),
               "INDEX", r["relationship_id"], max(1, int(r.get("evidence_count") or 1)))

    # 2. attributions authored on the QB card itself
    for ex, qid, _conf in card_attributions():
        upsert(ex, qid, literal_of("EXPLICIT_QCARD", qid), "QCARD", qid, 1)

    # 3. finalised Release A
    pub = js("RELEASE_A_PUBLICATION.json")
    for c in pub["connections"]:
        upsert(c["examiner"], c["canonical_question_id"],
               literal_of(c["strongest_evidence_tier"], c["relation_id"]),
               "RELEASE_A", c["relation_id"], len(c["evidence_ids"]))

    # 4. review-approved CE-tip relationships. STRONG_CE_TIP_REVIEW_DECISIONS.json
    #    is the human/evidence adjudication of the Release-A pairs that were held
    #    below the release floor on page-prose evidence alone. Only APPROVE_*
    #    decisions publish, at exactly the candidate tier the decision policy
    #    allows for that outcome, and only with evidence ids attached. Held and
    #    rejected rows publish nothing. Anything malformed is a build failure.
    for c in review_approved_ce_tip():
        upsert(c["examiner"], c["canonical_question_id"], c["candidate_tier"],
               "CE_TIP_REVIEW", c["relation_id"], len(c["evidence_ids"]))

    # 5. resolve every relationship against the live QB, or fail the build
    rows = []
    for (ex, qid), r in rels.items():
        e = examiners.get(ex)
        if e is None:
            fail("examiner %r is not in the alias register (%s)" % (ex, qid))
        if not e.get("slug"):
            fail("examiner %r has no slug in the alias register" % ex)
        q = inv.get(qid)
        if q is None:
            fail("relationship %s/%s does not resolve to a live question" % (ex, qid))
        if q["anchor"] not in anchors.get(q["file"], set()):
            fail("anchor %s missing on %s" % (q["anchor"], q["file"]))
        text = q["question_text"].strip()
        if not text:
            fail("empty display text for %s" % qid)
        rows.append({
            "examiner": ex, "slug": e["slug"], "examiner_status": e["status"],
            "canonical_question_id": qid, "file": q["file"], "anchor": q["anchor"],
            "q_number": q["q_number"], "url": q["url"], "display_text": text,
            "tier": r["tier"], "tier_rank": TIERS[r["tier"]]["rank"],
            "sources": sorted(set(r["sources"])), "refs": sorted(set(r["refs"])),
            "evidence_count": r["evidence_count"],
        })

    # deterministic order: examiner presentation order, tier strength,
    # then file (natural) and question number
    order = {s: i for i, s in enumerate(CONFIG["examiner_order"])}
    for row in rows:
        if row["slug"] not in order:
            fail("examiner slug %r is not in examiner_order" % row["slug"])
    rows.sort(key=lambda r: (order[r["slug"]], -r["tier_rank"],
                             natural_file_key(r["file"]), r["q_number"]))

    # counts - all len()
    per_ex = defaultdict(list)
    for r in rows:
        per_ex[r["slug"]].append(r)
    sections = []
    for slug in CONFIG["examiner_order"]:
        rs = per_ex.get(slug, [])
        if not rs:
            continue
        name = rs[0]["examiner"]
        by_tier = {t: sum(1 for r in rs if r["tier"] == t) for t in TIER_ORDER}
        sections.append({
            "slug": slug, "name": name, "status": rs[0]["examiner_status"],
            "blurb": CONFIG["examiner_blurbs"].get(slug, ""),
            "count": len(rs), "by_tier": by_tier,
        })
    totals = {
        "relationships": len(rows),
        "examiners": len(sections),
        "by_tier": {t: sum(1 for r in rows if r["tier"] == t) for t in TIER_ORDER},
        "qb_files": len(L.qb_files()),
        "canonical_questions": len(inv),
    }
    return {
        "note": ("Resolved canonical snapshot for the Examiner Index V2. Both "
                 "meoclass1/examiner-index.html and SQ/examiner-index.html are "
                 "rendered from exactly this object in one pass; every number "
                 "on either page is a len() over these rows."),
        "tier_policy": {t: {k: v for k, v in TIERS[t].items()} for t in TIER_ORDER},
        "totals": totals,
        "sections": sections,
        "rows": rows,
    }


# ----------------------------------------------------------------- render

def link_label(row):
    return "%s · Q%d" % (row["file"][:-5], row["q_number"])


def render_row(row):
    t = TIERS[row["tier"]]
    title = ""
    if row["evidence_count"] > 1:
        title = ' title="%d evidence records"' % row["evidence_count"]
    return (
        '<div class="q-row tier-%s" data-tier="%s">\n'
        '      <a class="q-link" href="%s">%s</a>\n'
        '      <div class="q-txt">%s</div>\n'
        '      <span class="tier-badge"%s>%s</span>\n'
        '    </div>' % (row["tier"], row["tier"], esc(row["url"]),
                        esc(link_label(row)), esc(row["display_text"]),
                        title, esc(t["badge"]))
    )


def render_section(sec, rows):
    slug, name = sec["slug"], sec["name"]
    n = sec["count"]
    size = CONFIG["batch_size"]
    batches = [rows[i:i + size] for i in range(0, n, size)]
    tabs = "".join(
        '<button class="batch-tab%s" data-ex="%s" data-batch="%d" '
        'onclick="showBatch(\'%s\',%d)">Q%d–%d</button>' % (
            " active" if i == 0 else "", slug, i, slug, i,
            i * size + 1, min((i + 1) * size, n))
        for i in range(len(batches)))
    filters = "\n".join(
        '        <label><input type="checkbox" checked data-tier-toggle="%s" '
        'onchange="filterTier(\'%s\')"> %s</label>' % (t, slug, esc(TIERS[t]["filter_label"]))
        for t in TIER_ORDER)
    stats = " &nbsp;·&nbsp; ".join(
        "%s%d %s" % (esc(TIERS[t]["badge"].split(" ")[0]), sec["by_tier"][t],
                     esc(TIERS[t]["label"].lower()))
        for t in TIER_ORDER if sec["by_tier"][t])
    note = ""
    if sec["status"] == "NEW_EXTERNAL_ONLY_EXAMINER":
        note = '\n      <div class="ex-note">%s</div>' % esc(CONFIG["external_only_note"])
    panels = []
    for i, b in enumerate(batches):
        panels.append(
            '<div class="batch-panel" id="batch-%s-%d"%s>%s</div>' % (
                slug, i, "" if i == 0 else ' style="display:none"',
                "".join(render_row(r) for r in b)))
    return (
        '  <section class="ex-section" id="ex-%s">\n'
        '    <button class="ex-head" onclick="toggleSection(\'%s\')">\n'
        '      <div class="ex-head-main">\n'
        '        <h2>%s <span class="ex-count">%d questions</span></h2>\n'
        '        <div class="ex-sub">%s</div>\n'
        '      </div>\n'
        '      <div class="ex-stats">%s</div>\n'
        '      <span class="chevron">▾</span>\n'
        '    </button>\n'
        '    <div class="ex-body" id="body-%s" style="display:none">\n'
        '      <div class="batch-tabs">%s</div>\n'
        '      <div class="tier-filter">\n'
        '        Show:\n%s\n'
        '      </div>%s\n'
        '      %s\n'
        '    </div>\n'
        '  </section>\n' % (slug, slug, esc(name), n, esc(sec["blurb"]), stats,
                            slug, tabs, filters, note, "".join(panels))
    )


def render_index(snap):
    css = (TPL / "examiner_index.css").read_text(encoding="utf-8")
    jsx = (TPL / "examiner_index.js").read_text(encoding="utf-8")
    tot = snap["totals"]
    by_slug = defaultdict(list)
    for r in snap["rows"]:
        by_slug[r["slug"]].append(r)
    summary = " ".join(
        '<span>%s <strong>%d</strong> %s</span>' % (
            esc(TIERS[t]["badge"].split(" ")[0]), tot["by_tier"][t],
            esc(TIERS[t]["label"].lower()))
        for t in TIER_ORDER if tot["by_tier"][t])
    mininav = "".join(
        '<a class="mini-pill" href="#ex-%s" onclick="openExaminer(\'%s\')">%s <span>%d</span></a>'
        % (s["slug"], s["slug"], esc(s["name"]), s["count"]) for s in snap["sections"])
    sections = "\n".join(render_section(s, by_slug[s["slug"]]) for s in snap["sections"])
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">\n'
        '<title>Examiner Index — MEO Class 1 Question Bank | Marine Intelligence Weekly</title>\n'
        '<script src="https://www.googletagmanager.com/gtag/js?id=G-0YEE2CBNP5" async></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        "gtag('js',new Date());gtag('config','G-0YEE2CBNP5');</script>\n"
        '<style>\n%s</style>\n</head>\n<body>\n\n'
        '<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>\n\n'
        '<div class="topbar">\n'
        '  <a class="topbar-logo" href="/meoclass1/">MIW</a>\n'
        '  <nav>\n'
        '    <a href="/meoclass1/">MEO Class 1</a>\n'
        '    <a href="/meoclass1/oralnotes/index.html">Notes Index</a>\n'
        '    <a href="mailto:contactus@marineintelligenceweekly.com">Contact</a>\n'
        '  </nav>\n</div>\n\n'
        '<div class="page-header">\n'
        '  <h1>Examiner Index — Kochi MMD Oral Panel</h1>\n'
        '  <p>Every QB question bundled by examiner. Click an examiner to expand. '
        'Questions tagged for more than one examiner appear in each relevant section. '
        'The badge on each row says how MIW knows: Confirmed from its own tracker, '
        'Reported from an external surveyor compilation, or declared on the QB page itself.</p>\n'
        '</div>\n\n'
        '<div class="summary-bar">\n'
        '  <span><strong>%d</strong> tagged pairs · %d examiners</span>\n'
        '  %s\n'
        '</div>\n\n'
        '<div class="mininav">\n  %s\n</div>\n\n'
        '<div class="search-bar">\n'
        '  <input type="text" id="pageSearch" placeholder="Filter questions by keyword..." '
        'oninput="filterSearch(this.value)">\n</div>\n\n'
        '<main>\n\n%s\n</main>\n\n'
        '<footer class="page-footer">\n'
        '  <div>Marine Intelligence Weekly — Examiner Index</div>\n'
        '  <div>© Marine Intelligence Weekly · <a href="mailto:contactus@marineintelligenceweekly.com">'
        'contactus@marineintelligenceweekly.com</a></div>\n'
        '</footer>\n\n'
        '<script>\n%s</script>\n\n</body>\n</html>\n'
        % (css, tot["relationships"], tot["examiners"], summary, mininav, sections, jsx)
    )


def render_sq(snap):
    css = (TPL / "sq_examiner_index.css").read_text(encoding="utf-8")
    sq = CONFIG["sq"]
    tot = snap["totals"]
    secs = {s["slug"]: s for s in snap["sections"]}
    by_slug = defaultdict(list)
    for r in snap["rows"]:
        by_slug[r["slug"]].append(r)
    free, promo = sq["free_examiner"], sq["promo_examiner"]
    for s in (free, promo):
        if s not in secs:
            fail("SQ teaser examiner %r has no section" % s)
    names = [s["name"] for s in snap["sections"]]
    names_text = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    names_list = ", ".join(names)
    free_rows = by_slug[free]
    promo_rows = by_slug[promo][:sq["promo_preview_rows"]]
    promo_total = secs[promo]["count"]
    promo_rest = promo_total - len(promo_rows)
    others = [s for s in snap["sections"] if s["slug"] not in (free, promo)]
    others_names = [s["name"] for s in others]
    others_text = (", ".join(others_names[:-1]) + ", and " + others_names[-1]
                   if len(others_names) > 1 else others_names[0])

    def qbadge(r):
        return '<span class="q-badge">%s</span>' % esc(link_label(r))

    free_html = "".join(
        '<div class="q-row-open">\n      %s\n      <div class="q-txt">%s</div>\n    </div>'
        % (qbadge(r), esc(r["display_text"])) for r in free_rows)
    promo_html = "".join(
        '<div class="q-row-preview">\n      %s\n      <div class="q-txt">%s</div>\n    </div>'
        % (qbadge(r), esc(r["display_text"])) for r in promo_rows)
    locked = "".join(
        '<div class="locked-card">\n'
        '      <div class="locked-card-top">\n'
        '        <span class="lock-icon">🔒</span>\n'
        '        <h3>%s</h3>\n'
        '      </div>\n'
        '      <div class="locked-desc">%s</div>\n'
        '      <div class="locked-count">%d questions tagged</div>\n'
        '    </div>' % (esc(s["name"]), esc(s["blurb"]), s["count"]) for s in others)
    faq = ",".join(
        json.dumps({"@type": "Question", "name": r["display_text"]}, ensure_ascii=False)
        for r in free_rows)
    free_name = secs[free]["name"]
    promo_name = secs[promo]["name"]
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>MEO Class 1 Oral Questions by Examiner — %s | Marine Intelligence Weekly</title>\n'
        '<meta name="description" content="Kochi MMD MEO Class 1 oral exam questions organized by examiner. '
        'Free sample: %s Sir\'s full question set. See exactly what %s ask.">\n'
        '<meta property="og:title" content="MEO Class 1 Questions by Examiner — Marine Intelligence Weekly">\n'
        '<meta property="og:description" content="Know your panel before you walk in. %d oral questions '
        'organized by Kochi MMD examiner.">\n'
        '<meta property="og:url" content="https://marineintelligenceweekly.com/SQ/examiner-index.html">\n'
        '<link rel="canonical" href="https://marineintelligenceweekly.com/SQ/examiner-index.html">\n'
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-0YEE2CBNP5"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        "gtag('js',new Date());gtag('config','G-0YEE2CBNP5');</script>\n"
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n'
        '</script>\n'
        '<style>\n%s</style>\n</head>\n<body>\n\n'
        '<nav>\n  <a class="brand" href="/">MIW</a>\n'
        '  <a class="home-link" href="/SQ/index.html">← QB Overview</a>\n</nav>\n\n'
        '<div class="hero">\n'
        '  <h1>Know Your <span>Examiner</span> Before You Walk In</h1>\n'
        '  <p>%d MEO Class 1 oral questions organized by Kochi MMD examiner — %s. '
        'See exactly what your panel tends to ask.</p>\n'
        '  <a class="cta-btn" href="/SQ/pay.html">Get Full Access — ₹1,499</a>\n'
        '</div>\n\n'
        '<div class="stats">\n'
        '  <div class="stat"><div class="stat-num">%d</div><div class="stat-label">Questions Tagged</div></div>\n'
        '  <div class="stat"><div class="stat-num">%d</div><div class="stat-label">Examiners Covered</div></div>\n'
        '  <div class="stat"><div class="stat-num">%d</div><div class="stat-label">%s Sir Questions</div></div>\n'
        '  <div class="stat"><div class="stat-num">%d</div><div class="stat-label">QB Files</div></div>\n'
        '</div>\n\n'
        '<main>\n\n'
        '  <div class="free-banner">\n'
        '    <div class="free-banner-top">\n'
        '      <span class="free-badge">🔓 FREE — FULL SAMPLE</span>\n'
        '      <h2>%s Sir — All %d Questions</h2>\n'
        '    </div>\n'
        '    <p>%s. This is the complete, unlocked set — no signup required.</p>\n'
        '  </div>\n\n'
        '  %s\n\n'
        '  <div class="promo-card">\n'
        '    <div class="promo-top">\n'
        '      <h2>⚙ %s Sir — %s</h2>\n'
        '      <span class="promo-badge">%s</span>\n'
        '    </div>\n'
        '    <div class="promo-desc">%s. %d questions tagged to %s Sir across the QB series. '
        "Here's a preview:</div>\n"
        '    %s\n'
        '    <div class="locked-teaser">\n'
        '      🔒 <strong>%d more %s Sir questions</strong> — diagrams, 2-stroke principles, '
        'turbocharger and fuel system deep-dives.\n'
        '      <br><a href="/SQ/pay.html">Unlock all %d %s Sir questions →</a>\n'
        '    </div>\n'
        '  </div>\n\n'
        '  <h2 class="section-title">Every Other Examiner, Covered</h2>\n'
        '  <p class="section-sub">Full breakdowns for %s are included with subscriber access.</p>\n'
        '  <div class="locked-grid">\n'
        '    %s\n'
        '  </div>\n\n'
        '  <div class="final-cta">\n'
        '    <h2>Walk in knowing your panel</h2>\n'
        '    <p>Full access includes every examiner breakdown, all %d tagged questions, and the '
        'complete Question Bank with 15-sec/60-sec model answers.</p>\n'
        '    <a class="cta-btn" href="/SQ/pay.html">Get Full Access — ₹1,499</a>\n'
        '  </div>\n\n'
        '</main>\n\n'
        '<footer>\n'
        '  <div>Marine Intelligence Weekly · MEO Class 1 Question Bank</div>\n'
        '  <div>© Marine Intelligence Weekly · <a href="mailto:contactus@marineintelligenceweekly.com">'
        'contactus@marineintelligenceweekly.com</a></div>\n'
        '</footer>\n\n</body>\n</html>\n'
        % (esc(names_list), esc(free_name), esc(names_text), tot["relationships"],
           faq, css,
           tot["relationships"], esc(names_list),
           tot["relationships"], tot["examiners"], promo_total, esc(promo_name), tot["qb_files"],
           esc(free_name), len(free_rows), esc(secs[free]["blurb"]), free_html,
           esc(promo_name), esc(sq["promo_title_suffix"]), esc(sq["promo_badge"]),
           esc(secs[promo]["blurb"]), promo_total, esc(promo_name), promo_html,
           promo_rest, esc(promo_name), promo_total, esc(promo_name),
           esc(others_text), locked, tot["relationships"])
    )


# ------------------------------------------- storefront card on SQ/index.html
# The QB overview page carries one card that describes the examiner index
# teaser. Its numbers were typed by hand ("Paul Sir's complete 10-question
# set", "Simon Sir's 212") and drifted with the page they describe. The
# generator owns exactly that card's description and examiner tags - anchored
# on the card title, and a build failure if the anchor is not found once -
# and leaves every other byte of the page alone.
CARD_RE = re.compile(
    r'(<div class="sample-card-title">Examiner Index — )([^<]*)(</div>\s*'
    r'<div class="sample-card-desc">)(.*?)(</div>\s*<div class="sample-tags">)(.*?)(</div>)',
    re.S)


def render_sq_home_card(snap):
    sq = CONFIG["sq"]
    secs = {s["slug"]: s for s in snap["sections"]}
    free, promo = secs[sq["free_examiner"]], secs[sq["promo_examiner"]]
    title = "%s Sir, Full Sample" % free["name"]
    desc = ("Every QB question bundled by Kochi MMD examiner. %s Sir's complete "
            "%d-question set is fully open here, plus a preview of %s Sir's %d "
            "machinery/2-stroke questions — see exactly what your panel tends to "
            "ask before you walk in." % (free["name"], free["count"],
                                          promo["name"], promo["count"]))
    tags = "\n" + "".join('        <span class="sample-tag">%s</span>\n' % esc(s["name"])
                          for s in snap["sections"]) + "      "
    # text-node context: keep the apostrophe in "Sir's" as typed
    return html.escape(title, quote=False), html.escape(desc, quote=False), tags


def patch_sq_home(snap):
    """Return the SQ/index.html text with the examiner-index card derived."""
    if not SQ_HOME_PATH.exists():
        fail("SQ/index.html is absent; the generator patches one card of it and "
             "cannot build without the page")
    text = SQ_HOME_PATH.read_bytes().decode("utf-8").replace("\r\n", "\n")
    hits = CARD_RE.findall(text)
    if len(hits) != 1:
        fail("SQ/index.html examiner-index card anchor found %d times, expected 1" % len(hits))
    title, desc, tags = render_sq_home_card(snap)
    return CARD_RE.sub(lambda m: m.group(1) + title + m.group(3) + desc + m.group(5)
                       + tags + m.group(7), text, count=1)


# ------------------------------------------------ the generated artefact set
# The ONE canonical list of files this generator owns. Normal mode writes
# exactly these; --check compares exactly these. Nothing else defines the set.
SNAPSHOT_PATH = OUT / SNAPSHOT_NAME
GENERATED_OUTPUTS = (SNAPSHOT_PATH, INDEX_PATH, SQ_PATH, SQ_HOME_PATH)


def rel(path):
    try:
        return path.resolve().relative_to(L.REPO.resolve()).as_posix()
    except ValueError:
        return str(path)


def lf_bytes(text):
    return text.replace("\r\n", "\n").encode("utf-8")


def build_outputs():
    """Resolve, render and self-check everything once.

    Returns (snapshot, {Path: bytes}) where the dict has exactly the
    GENERATED_OUTPUTS keys in that order and every value is the LF/UTF-8 byte
    string normal mode would write. Raises BuildFailure. Writes nothing.
    Both normal mode and --check are built from this one function, so the
    bytes that are checked can never diverge from the bytes that are written.
    """
    snap = resolve_snapshot()
    index_html = render_index(snap)
    sq_html = render_sq(snap)
    sq_home_html = patch_sq_home(snap)
    # every literal emitted must have a filter toggle in its own section
    for sec in snap["sections"]:
        blob = re.search(r'<section class="ex-section" id="ex-%s">(.*?)</section>'
                         % sec["slug"], index_html, re.S).group(1)
        toggles = set(re.findall(r'data-tier-toggle="([^"]+)"', blob))
        literals = set(re.findall(r'data-tier="([^"]+)"', blob))
        if not literals <= toggles:
            fail("tier literal without a toggle in %s: %s"
                 % (sec["slug"], sorted(literals - toggles)))
    outputs = {
        SNAPSHOT_PATH: lf_bytes(json.dumps(snap, ensure_ascii=False, indent=1) + "\n"),
        INDEX_PATH: lf_bytes(index_html),
        SQ_PATH: lf_bytes(sq_html),
        SQ_HOME_PATH: lf_bytes(sq_home_html),
    }
    if tuple(outputs) != GENERATED_OUTPUTS:
        fail("build_outputs() and GENERATED_OUTPUTS disagree on the artefact set")
    return snap, outputs


def write_atomic(path, data):
    """Stage next to the target, fsync, then os.replace(): an interrupted run
    never leaves a half-written governed artefact on disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".staging", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_outputs(outputs):
    for path, data in outputs.items():
        write_atomic(path, data)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _first_diff_line(expected, actual):
    """1-based number of the first differing line plus both lines, clipped:
    enough to locate a hand edit without dumping the file."""
    e_lines, a_lines = expected.split(b"\n"), actual.split(b"\n")
    for i, (e, a) in enumerate(zip(e_lines, a_lines), 1):
        if e != a:
            return i, e[:120], a[:120]
    i = min(len(e_lines), len(a_lines)) + 1
    e = e_lines[i - 1][:120] if i - 1 < len(e_lines) else b"<end of expected>"
    a = a_lines[i - 1][:120] if i - 1 < len(a_lines) else b"<end of actual>"
    return i, e, a


def check_outputs(outputs):
    """Compare every generated artefact's expected bytes with what is on disk.

    Returns a list of finding strings; empty means every artefact is byte-
    current. Reads only. Byte-exact on purpose: the generator promises LF,
    UTF-8, timestamp-free, hash-seed-independent bytes, so any difference is
    a hand edit, a forgotten regeneration, or a determinism defect - all of
    which must fail."""
    findings = []
    for path, expected in outputs.items():
        # the one orphan the generator can own with certainty: its own
        # staging residue beside a target (an interrupted or crashed run).
        # Anything else on disk is not this generator's to judge, so --check
        # guarantees expected-output freshness, not orphan cleanup.
        for junk in sorted(path.parent.glob(path.name + ".*.staging")):
            findings.append("EXTRA OUTPUT: %s (staging residue)" % rel(junk))
        if not path.exists():
            findings.append("MISSING OUTPUT: %s\n  expected sha256 %s (%d bytes)"
                            % (rel(path), _sha(expected), len(expected)))
            continue
        actual = path.read_bytes()
        if actual == expected:
            continue
        line, e_l, a_l = _first_diff_line(expected, actual)
        findings.append(
            "STALE OUTPUT: %s\n  expected sha256 %s (%d bytes)\n  actual   sha256 %s (%d bytes)"
            "\n  first difference at line %d\n    expected: %s\n    actual:   %s"
            % (rel(path), _sha(expected), len(expected), _sha(actual), len(actual),
               line, e_l.decode("utf-8", "replace"), a_l.decode("utf-8", "replace")))
    return findings


def run_semantic_validation():
    """validate_examiner_index.py as a subprocess (it imports this module, so an
    in-process import would be circular). It reads the on-disk artefacts and
    writes nothing. Returns (exit_code, [FAIL lines])."""
    r = subprocess.run([sys.executable, str(HERE / "validate_examiner_index.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=str(L.REPO))
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    if r.returncode != 0 and not fails:
        tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or ["no output"]
        fails = ["FAIL  validator did not run cleanly (exit %d): %s" % (r.returncode, tail[0])]
    return r.returncode, fails


def print_summary(snap):
    tot = snap["totals"]
    print("relationships %d  examiners %d  tiers %s" % (
        tot["relationships"], tot["examiners"], tot["by_tier"]))
    for s in snap["sections"]:
        print("  %-11s %4d  %s" % (s["name"], s["count"],
                                  {t: n for t, n in s["by_tier"].items() if n}))


# ------------------------------------------------------------------- main
# Exit codes: 0 current + valid; 1 semantic validation failed; 2 build
# failure; 3 stale/missing generated output. --check writes nothing, ever.

def main(argv):
    check_only = "--check" in argv
    try:
        snap, outputs = build_outputs()
    except BuildFailure as e:
        print("BUILD FAILURE: %s" % e)
        if check_only:
            print("EXAMINER INDEX CHECK: FAIL (generation failed)")
        return 2
    print_summary(snap)
    if not check_only:
        write_outputs(outputs)
        print("wrote %s" % ", ".join(rel(p) for p in outputs))
        return 0

    stale = check_outputs(outputs)
    v_rc, v_fails = run_semantic_validation()
    n = len(outputs)
    if not stale and v_rc == 0 and not v_fails:
        print("EXAMINER INDEX CHECK: PASS")
        print("%d/%d generated artefacts current" % (n, n))
        print("semantic validation PASS")
        return 0
    print("EXAMINER INDEX CHECK: FAIL")
    for f in stale:
        print(f)
    print("%d/%d generated artefacts current" % (n - len(stale), n))
    if v_rc == 0 and not v_fails:
        print("semantic validation PASS")
    else:
        print("semantic validation FAIL (%d)" % len(v_fails))
        for f in v_fails[:10]:
            print("  " + f[:160])
    return 3 if stale else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
