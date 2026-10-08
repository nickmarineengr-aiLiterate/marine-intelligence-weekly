// =============================================================
// Marine Intelligence Weekly — cross-product regulatory-fact contract
// Run: node --test tools/security/*.test.mjs
//
// WHY THIS EXISTS
//   On 22 July 2026 MIW published three products on the same day that did not
//   agree with each other. Issue 30 and QB7_G said the reconvened IMO Net-Zero
//   Framework adoption session was "October 2026"; the MEO oral notes
//   (WA2-GHG1, WA2-GHG2, miw-notes-mgmt-p2) and QB10_B said 4 December 2026,
//   which is what the IMO's own MEPC 84 outcome had said since 1 May 2026.
//
//   The controlling source was public 82 days before publication AND the right
//   answer was already written down inside MIW. Nothing was stale. What was
//   missing was any mechanism that made two MIW products disagree loudly.
//   This file is that mechanism.
//
// WHAT IT IS NOT
//   It is not a fact checker. It cannot tell whether a date is true. It holds a
//   SMALL, HAND-CURATED register of high-risk regulatory facts — the ones MIW
//   repeats across the magazine, the Question Bank and the oral notes — and
//   asserts that every current-facing surface tells the same story.
//
// THE FALSE-POSITIVE PROBLEM, AND HOW SCOPE SOLVES IT
//   "October 2026" is CORRECT in ~15 past-paper files. A sitting in January 2026
//   could only know that the adjourned session was due to reconvene "about
//   twelve months later"; a solved paper that says so is right, and a site-wide
//   ban on the string would fail it. Scope is therefore drawn by PUBLICATION
//   CHRONOLOGY, not by string:
//
//     IN SCOPE   surfaces that speak in the present tense about current law —
//                the MEO Class 1 Question Bank, the oral notes, and issue pages
//                published on or after the controlling source date.
//     OUT        past papers and solvedQP (anchored to their sitting date), and
//                issues published BEFORE the controlling source, which were
//                correct when written and carry an UPDATE note instead.
//
//   Disclosed-correction and update blocks are stripped before scanning: they
//   necessarily quote the superseded wording, and a guard that fired on its own
//   audit trail would train people to delete the audit trail.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT, KEEP } from "./deploy_set.mjs";

const read = (rel) => fs.readFileSync(path.join(ROOT, rel), "utf8");

/**
 * Remove the blocks whose whole job is to quote superseded wording, so the
 * guard never fires on the correction that fixed the thing it guards.
 */
export function stripCorrectionBlocks(html) {
  // Depth-aware: these blocks nest, so a lazy match to the first closing tag
  // would leave most of the block (and its quoted wrong date) behind.
  const open = /<(section|div)\b[^>]*(?:id="(?:correction|update-note)"|class="verify-note")[^>]*>/i;
  let out = html;
  for (let guard = 0; guard < 50; guard++) {
    const m = open.exec(out);
    if (!m) break;
    const tag = m[1].toLowerCase();
    const scan = new RegExp(`<${tag}\\b[^>]*>|</${tag}\\s*>`, "gi");
    scan.lastIndex = m.index;
    let depth = 0, end = -1, t;
    while ((t = scan.exec(out))) {
      depth += t[0].startsWith("</") ? -1 : 1;
      if (depth === 0) { end = t.index + t[0].length; break; }
    }
    out = end === -1 ? out.slice(0, m.index) : out.slice(0, m.index) + out.slice(end);
  }
  return out;
}

/**
 * A study product is allowed — encouraged — to NAME a superseded date, provided
 * it marks it as superseded. That is a trap warning, not a stale claim. The
 * exemption is deliberately narrow: the refutation must sit in the same statement.
 */
const REFUTATION =
  /supersed|the original\b|originally (announced|reported|given|stated)|initially reported|briefly cited|not a fixed|with caution|stale|no longer|previously (gave|stated)|was wrong|incorrectly|factual error|as still current|overstated|\bIssue \d+ (gave|stated|said|reported)\b/i;

/**
 * The page as a list of statements — the unit a claim is made in. Block-level
 * markup (paragraph, list item, table cell, heading, line break, div, pre line)
 * ends a statement; inline markup (strong, em, span, a) does not, so a claim
 * that is split by formatting is still read as one sentence. Within a block,
 * sentences end at . ! ? followed by a space ("MEPC/ES.2" does not split).
 * Line breaks in the HTML source are only wrapping and never end a statement,
 * except inside <pre>, where each line of an ASCII diagram is its own line.
 */
const BLOCK_TAG =
  /<\/?(?:p|li|ul|ol|td|th|tr|thead|tbody|table|caption|h[1-6]|div|section|article|aside|header|footer|nav|main|blockquote|pre|dt|dd|dl|figure|figcaption|br|hr)\b[^>]*>/gi;
const ENTITIES = { "&nbsp;": " ", "&#160;": " ", "&amp;": "&", "&mdash;": "\u2014", "&ndash;": "\u2013",
                   "&middot;": "\u00b7", "&quot;": '"', "&#39;": "'", "&rsquo;": "\u2019", "&lsquo;": "\u2018",
                   "&ldquo;": "\u201c", "&rdquo;": "\u201d", "&lt;": "<", "&gt;": ">" };

const BREAK = "\u0001";

export function statements(html) {
  const text = html
    .replace(/<pre\b[^>]*>[\s\S]*?<\/pre\s*>/gi, (pre) => pre.replace(/\r?\n/g, BREAK))
    .replace(/\s+/g, " ")
    .replace(/<(script|style)\b[\s\S]*?<\/\1\s*>/gi, BREAK)
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(BLOCK_TAG, BREAK)
    .replace(/<[^>]+>/g, "")
    .replace(/&[#a-z0-9]+;/gi, (e) => ENTITIES[e.toLowerCase()] ?? e);
  return text
    .split(new RegExp(`${BREAK}|(?<=[.!?])\\s+`))
    .map((x) => x.replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

/**
 * Context that turns a month into a claim about the resumed session. Kept
 * small on purpose: "Net-Zero Framework ... not adopted" is a correct status
 * statement, so bare "Net-Zero"/"adopt" is NOT context; adoption TIMING is.
 */
const ES2_CONTEXT = new RegExp([
  String.raw`\bMEPC\s*[\/.]?\s*ES\s*[.\/]?\s*2\b`,
  String.raw`\bES\.2\b`,
  String.raw`\bextraordinary (?:MEPC )?session\b`,
  String.raw`\breconven\w*`,
  String.raw`\bresum(?:e|es|ed|ing|ption)\b`,
  String.raw`\badoption (?:is |was |now )?(?:expected|scheduled|due|vote|date|decision|timing)\b`,
  String.raw`\b(?:expected|scheduled|due) (?:to be )?adopt`,
  String.raw`\bdecision point\b`,
  String.raw`\b(?:Net-Zero|NZF)\b(?:(?![.!?]).){0,40}?\bvote\b`,
].join("|"), "i");

/** Clause boundaries, for tokens that are only stale in their own clause. */
const CLAUSE = /[,;]|\s[\u2014\u2013]\s/;

/** Every superseded-date occurrence that is asserted (in context) rather than refuted. */
export function liveSupersededHits(body, fact) {
  const hits = [];
  for (const st of statements(body)) {
    if (REFUTATION.test(st)) continue;
    for (const s of fact.superseded) {
      const units = s.scope === "clause" ? st.split(CLAUSE) : [st];
      for (const u of units) {
        if (s.exclude && s.exclude.test(u)) continue;
        if (!fact.context.test(u)) continue;
        const re = new RegExp(s.pattern.source, "g");
        let m;
        while ((m = re.exec(u))) hits.push(s.label);
      }
    }
  }
  return hits;
}

// -------------------------------------------------------------
// THE REGISTER — high-risk facts MIW repeats across products.
// Keep this SHORT. A fact earns a row by being (a) a date or status, (b) said
// in more than one product, and (c) already wrong once.
// -------------------------------------------------------------
export const REGULATORY_FACTS = [
  {
    id: "mepc-es2-resumption",
    what: "resumed IMO MEPC extraordinary session (MEPC/ES.2) on the Net-Zero Framework",
    // IMO press briefing, 01 May 2026 — MEPC 84 outcome.
    source: "IMO MEPC 84 outcome, 1 May 2026",
    controllingSourceDate: "2026-05-01",
    // A surface that discusses the resumption must give this date. The year is
    // optional: WA2-GHG1 writes "a resumed one-day MEPC/ES.2 on 4 Dec" inside a
    // sentence that already carries 2026.
    correct: /\b4 De(c|cember)\b/,
    // ...and must never give these, which are superseded — but a month is only
    // a claim about the session when the statement it sits in is ABOUT the
    // session (ES2_CONTEXT). The original rule banned the bare month everywhere;
    // from 1 October 2026 that flagged every as-at dateline, membership count
    // and delivery date written this month (Notes P24, P25, P28, P29).
    // A day number before the month ("7 October 2026") is a calendar date, not
    // the superseded month. (Flags are dropped when a pattern is re-compiled
    // with "g", so none are relied on.)
    superseded: [
      { pattern: /(?<!\b\d{1,2} )\bOctober 2026\b/, label: "October 2026", scope: "statement" },
      { pattern: /(?<!\b\d{1,2} )\bOct 2026\b/, label: "Oct 2026", scope: "statement" },
      // "November 2026" was also announced (and superseded) as the adoption
      // point, but ISWG-GHG 23 genuinely meets in November 2026 — so it counts
      // only inside its own clause, and never in a clause about the
      // intersessional working groups.
      { pattern: /(?<!\b\d{1,2} )\bNov(?:ember)? 2026\b/, label: "November 2026", scope: "clause",
        exclude: /intersessional|working group|ISWG/i },
    ],
    context: ES2_CONTEXT,
    // Only pages that actually talk about the session are asked for the date.
    topic: /Net-Zero Framework|MEPC\/ES\.2|extraordinary session/i,
  },
];

// -------------------------------------------------------------
// SCOPE
// -------------------------------------------------------------

/** Issue pages, with the publication date the page itself declares. */
function issuePages() {
  const out = [];
  for (const rel of KEEP) {
    const p = rel.replace(/\\/g, "/");
    if (!/^(index\d+\.html|archive\/issue\d+\.html)$/.test(p)) continue;
    const html = read(p);
    const m = html.match(/"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"/);
    out.push({ rel: p, published: m ? m[1] : null, html });
  }
  return out;
}

/** Candidate-facing study product: the Question Bank and the oral notes. */
function studyPages() {
  return KEEP
    .map((r) => r.replace(/\\/g, "/"))
    .filter((p) => /^meoclass1\/(QB[^/]+\.html|oralnotes\/[^/]+\.html)$/.test(p))
    .map((rel) => ({ rel, html: read(rel) }));
}

/**
 * Historical, sitting-anchored corpora — deliberately never in scope. A solved
 * or sample paper answers as of ITS sitting date, so "around October 2026" is
 * the correct answer there and must never be rewritten to today's law.
 */
const HISTORICAL =
  /^(meoclass1\/pastpapers\/|solvedQP\/|SQ\/)|\/(solved-qp|written-sample)[\w-]*\.html$/;

/** Every surface that speaks in the present tense about current law. */
export function currentFacingPages(fact) {
  const pages = [
    ...studyPages(),
    ...issuePages().filter(
      (p) => p.published && p.published >= fact.controllingSourceDate,
    ),
  ];
  return pages.filter((p) => !HISTORICAL.test(p.rel));
}

// -------------------------------------------------------------
// 0. CONTROLS — prove the detector discriminates before trusting it
// -------------------------------------------------------------
describe("controls", () => {
  const fact = REGULATORY_FACTS[0];

  const hits = (text) => liveSupersededHits(text, fact);

  test("the detector catches the wording that was actually published", () => {
    const asPublished =
      "MEPC/ES.2 adjourned the vote (57-49) in October 2025; reconvenes October 2026.";
    assert.ok(hits(asPublished).length >= 1);
  });

  test("the detector does NOT flag the corrected wording", () => {
    const corrected =
      "MEPC/ES.2 resumes 4 December 2026, immediately after MEPC 85 (30 Nov - 3 Dec 2026).";
    assert.deepEqual(hits(corrected), []);
    assert.ok(fact.correct.test(corrected));
  });

  test("'October 2025' is not mistaken for the superseded date", () => {
    assert.deepEqual(hits("The session adjourned in October 2025 by 57-49."), []);
    assert.deepEqual(hits("MEPC/ES.2 (14\u201317 Oct 2025) adjourned for one year without adopting."), []);
  });

  // NEGATIVE CONTROLS — an October 2026 (or November 2026) date that is not a
  // claim about the resumed session. From 1 October 2026 the bare month is also
  // the month a page was checked, a statistic was counted or a product ships.
  test("benign October/November 2026 dates are never offenders", () => {
    const benign = [
      "Key Instruments and Their Status (October 2026)",                                   // P25 reg box
      "<th>Fuel</th><th>Instrument</th><th>Status (Oct 2026)</th>",                          // P25 table
      "describes a measure that, at the time of writing (October 2026), exists only as draft amendments to MARPOL Annex VI, the IMO Net-Zero Framework.", // P24
      "ESG = framework of factors \u00b7 MACN = 225+ COMPANIES in 45+ countries (Oct 2026), est. 2011.", // P28 memory box
      "MACN states it has over 225 member companies across more than 45 countries (October 2026; the figure changes).", // P28
      "first deliveries from October 2026, not yet confirmed in commercial service",           // P29
      "Issue 31 \u2014 7 October 2026. MEPC/ES.2 resumes 4 December 2026.",                    // publication date
      '<div class="issue-number-badge">Issue 31 &nbsp;\u00b7&nbsp; 7 October 2026</div>',
      "As at October 2026 the Net-Zero Framework is approved but not adopted, and not in force.",
      "The EU ETS surrender guidance for shipping companies was updated in October 2026.",     // unrelated #1
      "The Administration issued the 2025 CII rating statements in October 2026.",            // unrelated #2
      "Two further intersessional working groups meet in September and November 2026, reporting to MEPC 85.",
      "The GISIS public site listed about thirty modules when checked in October 2026.",       // P23 style
      // a disclosed prior MIW error, reported as such (Issue 31 correction note)
      "Published on 22 July 2026, Issue 30 gave the reconvened MEPC extraordinary session as October 2026, and derived an earliest entry into force of about March 2028 from it.",
      // a source-wrapped refutation stays one statement (WA2-GHG1 v1.4 changelog)
      "<p>the reconvened session is <strong>MEPC 85 in November 2026</strong>, not the\n  October 2026 date some outlets initially reported in October 2025</p>",
      // a later changelog entry correcting the one above (WA2-GHG1 v1.7)
      "Also revised the Chapter 5 reconvened-session date: the v1.4 note's \"confirmed MEPC 85 in November 2026\" overstated certainty.",
    ];
    for (const s of benign) assert.deepEqual(hits(s), [], `benign date flagged: ${s}`);
  });

  // POSITIVE CONTROLS — genuine obsolete MEPC/ES.2 timing must still fail.
  test("genuine obsolete MEPC/ES.2 timing is detected", () => {
    const stale = [
      "MEPC/ES.2 reconvenes October 2026.",
      "The extraordinary session resumes in October 2026.",
      "The Net-Zero Framework adoption is expected in October 2026.",
      "For the Net-Zero Framework, the decision point is November 2026.",
      "the GFI standard, with adoption expected at MEPC 85 (Nov 2026) and entry into force 12 months later",
      "the Net-Zero vote falls in October 2026",
      "reconvenes Oct 2026",
      // beside an otherwise-valid dateline, in the same block and in the next block
      "Key Instruments and Their Status (October 2026) \u2014 MEPC/ES.2 reconvenes October 2026.",
      '<div class="reg-box-title">Key Instruments and Their Status (October 2026)</div><p>MEPC/ES.2 reconvenes October 2026.</p>',
      // embedded in inline markup
      '<p>The resumed <strong>MEPC/ES.2</strong> is <em>scheduled</em> for <span class="d">Oct 2026</span>.</p>',
      '<li><a href="#x">Extraordinary session</a> reconvening: <b>October 2026</b></li>',
    ];
    for (const s of stale) assert.ok(hits(s).length >= 1, `stale claim missed: ${s}`);
  });

  test("statements end at block markup, not at inline markup", () => {
    assert.deepEqual(statements("<p>a <strong>b</strong> c.</p><p>d</p>"), ["a b c.", "d"]);
    assert.deepEqual(statements("<td>x</td><td>y</td>"), ["x", "y"]);
    // source line-wrapping is not a statement boundary; <pre> lines are
    assert.deepEqual(statements("<p>MEPC/ES.2\n   reconvenes\n October 2026.</p>"),
      ["MEPC/ES.2 reconvenes October 2026."]);
    assert.ok(hits("<p>MEPC/ES.2\n   reconvenes\n October 2026.</p>").length >= 1);
    assert.deepEqual(statements("<pre>  line one\n  line two</pre>"), ["line one", "line two"]);
    // a refutation in a neighbouring block does not excuse a stale claim
    assert.ok(hits("<p>The original date was superseded.</p><p>MEPC/ES.2 reconvenes October 2026.</p>").length >= 1);
  });

  test("mutation: a stale ES.2 claim injected into a real Notes page is caught", () => {
    const rel = "meoclass1/oralnotes/miw-notes-mgmt-p24.html";
    const clean = stripCorrectionBlocks(read(rel));
    assert.deepEqual(hits(clean), [], `${rel} must be clean before mutation`);
    const mutated = clean.replace('<p class="notes-body">',
      '<p class="notes-body">The resumed MEPC/ES.2 reconvenes October 2026. ');
    assert.notEqual(mutated, clean, "mutation anchor must exist");
    assert.ok(hits(mutated).length >= 1, "injected stale claim must be detected");
  });

  test("correction blocks are stripped, and only correction blocks", () => {
    const html =
      '<p>body text</p>' +
      '<section id="correction"><p>originally stated October 2026</p></section>' +
      '<div class="verify-note">previously gave October 2026</div>' +
      '<p>keep me</p>';
    const stripped = stripCorrectionBlocks(html);
    assert.ok(!/October 2026/.test(stripped), "correction blocks must be stripped");
    assert.ok(stripped.includes("body text") && stripped.includes("keep me"),
      "stripping must not eat ordinary body copy");
  });

  test("stripping does not hide a real defect in body copy", () => {
    const html = '<p>reconvenes October 2026</p><section id="correction">x</section>';
    assert.ok(/October 2026/.test(stripCorrectionBlocks(html)));
  });

  test("scope is non-empty and excludes the historical corpora", () => {
    const pages = currentFacingPages(fact);
    assert.ok(pages.length > 0, "the guard must actually be looking at something");
    for (const p of pages) {
      assert.ok(!HISTORICAL.test(p.rel), `${p.rel} is historical and must be out of scope`);
    }
  });

  test("past papers really do carry the superseded wording, and are still excluded", () => {
    // If this ever stops being true the scope rule has become untestable and
    // the exclusion above is no longer carrying weight.
    const historicalHits = KEEP
      .map((r) => r.replace(/\\/g, "/"))
      .filter((p) => HISTORICAL.test(p) && p.endsWith(".html"))
      .filter((p) => /October 2026|Oct 2026/.test(read(p)));
    assert.ok(historicalHits.length > 0,
      "expected the historical corpora to contain legitimate 'October 2026' references");
  });
});

// -------------------------------------------------------------
// 1. NO CURRENT-FACING SURFACE MAY CARRY A SUPERSEDED FACT
// -------------------------------------------------------------
describe("superseded regulatory facts are not live", () => {
  for (const fact of REGULATORY_FACTS) {
    test(`no current-facing page states a superseded ${fact.id}`, () => {
      const offenders = [];
      for (const page of currentFacingPages(fact)) {
        const body = stripCorrectionBlocks(page.html);
        for (const label of new Set(liveSupersededHits(body, fact))) {
          offenders.push(`${page.rel} -> "${label}"`);
        }
      }
      assert.deepEqual(offenders, [],
        `superseded ${fact.what} still live (correct value: ${fact.source}):\n  ` +
        offenders.join("\n  "));
    });
  }
});

// -------------------------------------------------------------
// 2. PRODUCTS MUST AGREE WITH EACH OTHER
// -------------------------------------------------------------
describe("cross-product consistency", () => {
  for (const fact of REGULATORY_FACTS) {
    test(`every page that discusses ${fact.id} gives the same date`, () => {
      const missing = [];
      for (const page of currentFacingPages(fact)) {
        const body = stripCorrectionBlocks(page.html);
        if (!fact.topic.test(body)) continue;          // page does not raise it
        if (!/resum|reconven/i.test(body)) continue;   // ...or does not date it
        if (!fact.correct.test(body)) missing.push(page.rel);
      }
      assert.deepEqual(missing, [],
        `these pages date the ${fact.what} without giving the correct value ` +
        `(${fact.source}):\n  ` + missing.join("\n  "));
    });
  }
});

// -------------------------------------------------------------
// 3. THE CORRECTION IS DISCLOSED, NOT SILENT
// -------------------------------------------------------------
describe("disclosure", () => {
  const corrected = ["index30.html", "archive/issue30.html",
                     "index23.html", "archive/issue23.html"];

  for (const rel of corrected) {
    test(`${rel} carries a dated disclosed correction`, () => {
      const html = read(rel);
      assert.match(html, /id="correction"/,
        "a corrected issue page must carry a visible correction block");
      assert.match(html, /CORRECTION\s+\u2014\s+\d{1,2}\s+\w+\s+20\d\d:/,
        "the correction must be dated, per governance/CORRECTION_WORKFLOW.md");
      assert.match(html, /4 December 2026/,
        "the correction must state the corrected value");
    });
  }

  for (const rel of ["index17.html", "archive/issue17.html"]) {
    test(`${rel} carries an update note, not a correction`, () => {
      const html = read(rel);
      assert.match(html, /id="update-note"/,
        "Issue 17 predates the controlling source: it is an update, not a correction");
      assert.match(html, /UPDATE\s+\u2014\s+\d{1,2}\s+\w+\s+20\d\d:/);
      assert.doesNotMatch(html, /id="correction"/,
        "Issue 17 was correct when published and must not be labelled a correction");
    });
  }

  test("the archive twins stay byte-identical to their root pages", () => {
    const norm = (s) => s.replace(/\r\n/g, "\n");
    for (const n of [17, 23, 30]) {
      assert.equal(norm(read(`archive/issue${n}.html`)), norm(read(`index${n}.html`)),
        `archive/issue${n}.html has drifted from index${n}.html`);
    }
  });
});
