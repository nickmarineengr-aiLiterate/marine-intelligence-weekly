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
 * exemption is deliberately narrow: the refutation must sit beside the date.
 */
const REFUTATION =
  /supersed|the original\b|originally (announced|reported|given)|initially reported|briefly cited|not a fixed|with caution|stale|no longer|previously (gave|stated)|was wrong|incorrectly|factual error|as still current/i;

export function isRefutedInPlace(body, index, label) {
  const w = body.slice(Math.max(0, index - 260), index + label.length + 260);
  return REFUTATION.test(w);
}

/** Every superseded-date occurrence that is asserted rather than refuted. */
export function liveSupersededHits(body, fact) {
  const hits = [];
  for (const s of fact.superseded) {
    const re = new RegExp(s.pattern.source, "g");
    let m;
    while ((m = re.exec(body))) {
      if (!isRefutedInPlace(body, m.index, s.label)) hits.push(s.label);
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
    // ...and must never give these, which are superseded.
    superseded: [
      { pattern: /\bOctober 2026\b/, label: "October 2026" },
      { pattern: /\bOct 2026\b/, label: "Oct 2026" },
    ],
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

  test("the superseded pattern matches the wording that was actually published", () => {
    const asPublished =
      "MEPC/ES.2 adjourned the vote (57-49) in October 2025; reconvenes October 2026.";
    assert.ok(fact.superseded.some((s) => s.pattern.test(asPublished)));
  });

  test("the superseded pattern does NOT match the corrected wording", () => {
    const corrected =
      "MEPC/ES.2 resumes 4 December 2026, immediately after MEPC 85 (30 Nov - 3 Dec 2026).";
    assert.ok(!fact.superseded.some((s) => s.pattern.test(corrected)));
    assert.ok(fact.correct.test(corrected));
  });

  test("'October 2025' is not mistaken for the superseded date", () => {
    const historyOnly = "The session adjourned in October 2025 by 57-49.";
    assert.ok(!fact.superseded.some((s) => s.pattern.test(historyOnly)));
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
