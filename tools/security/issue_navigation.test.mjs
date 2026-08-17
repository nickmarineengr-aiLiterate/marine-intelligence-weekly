// =============================================================
// Marine Intelligence Weekly — issue-navigation contract (R5)
// Run: node --test tools/security/*.test.mjs
//
// R1 published the archive and, while verifying it, MEASURED the
// previous-issue chain instead of assuming it. Two pages were broken:
// index24 carried no previous-issue link at all, and index25 was reported
// as pointing at Issue 22 rather than Issue 24.
//
// The second report was half right. index25's only reference to Issue 22
// lives inside an "archive pointer" paragraph — editorial body copy that
// correctly says the MSC 111 items it does not repeat were covered in
// Issue 22. It was never a navigation control. So index25's real defect
// was the SAME as index24's: no previous-issue navigation existed.
// Rewriting that paragraph's href would have corrupted a true sentence.
//
// That distinction is the whole reason this guard classifies by
// AFFORDANCE rather than by "does the page mention another issue":
//
//   A previous-issue navigation link is an anchor that (a) resolves to
//   another issue's page and (b) whose visible text carries a back
//   affordance — a left arrow or the word "Previous".
//
// Editorial prose that cites an earlier issue has neither, and is
// correctly ignored. A nav control cannot lack both and still be a nav
// control, so the classifier cannot be dodged by restyling.
//
// WHY NOT ASSERT MARKUP
//   There is no shared navigation component. Every issue is a bespoke
//   one-page design and the prev link lives somewhere different in each:
//   .mast-prev (17-22 era), .prev-issue-bar (23-25), .btn-nav.btn-prev
//   (26), .topnav + .footernav (27-29), .nav-toplinks + footer (30).
//   A guard written against any one of those shapes would be a guard
//   against one issue. Asserting the RELATIONSHIP survives redesigns.
//
// WHY THE FIXTURES ARE SYNTHETIC
//   The controls below are hand-written strings, never pages sampled from
//   the corpus. A self-test whose fixture is harvested from live content
//   stops discriminating the moment the content changes, and does so
//   silently — this repository has already paid for that lesson once.
//
// Absent-next is deliberate house convention, not an oversight: no issue
// page has ever had a next link, so Issue 30 carries no pointer at an
// unstarted Issue 31. That absence is asserted, so it cannot be
// "helpfully" filled in later without a decision.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT } from "./deploy_set.mjs";

/** Every issue with a root page, oldest to newest. */
const ISSUES = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];

/**
 * Issues whose page carries NO previous-issue navigation.
 *
 * This is recorded evidence of how those pages were actually published,
 * not a rule anyone chose. They predate the convention settling down and
 * are deliberately left as history. Issue 20 is NOT among them — it does
 * carry a masthead "← Issue 19", which an earlier reading of the chain
 * missed because it only looked for absolute issue URLs in a footer.
 */
const NO_PREV_LINK = new Set([17, 18, 19, 21, 22]);

/** First issue required to point at its predecessor. */
const CHAIN_STARTS_AT = 23;

const rootPage = (n) => `index${n}.html`;
const archivePage = (n) => `archive/issue${n}.html`;
const read = (rel) => fs.readFileSync(path.join(ROOT, rel), "utf8");

const ANCHOR = /<a\b[^>]*\bhref\s*=\s*"([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi;

/** Same-site host forms used across the issue pages. */
const HOSTS = [
  "https://marineintelligenceweekly.com",
  "https://www.marineintelligenceweekly.com",
  "http://marineintelligenceweekly.com",
];

/**
 * The issue number an href targets, or null if it does not target an
 * issue page. Handles absolute, root-relative and archive-relative forms
 * so root pages and their archive twins are read identically.
 */
export function issueTargetOf(href) {
  let h = (href || "").trim();
  if (!h || h.startsWith("#")) return null;
  for (const host of HOSTS) {
    if (h.toLowerCase().startsWith(host)) { h = h.slice(host.length); break; }
  }
  h = h.split("#")[0].split("?")[0];
  h = h.replace(/^\.\.\//, "/").replace(/^\.\//, "/");
  if (!h.startsWith("/")) h = "/" + h;
  const m = /^\/index(\d+)\.html$/i.exec(h);
  return m ? Number(m[1]) : null;
}

/** Visible text of an anchor, entities and tags flattened. */
function visibleText(inner) {
  return inner
    .replace(/<[^>]*>/g, " ")
    .replace(/&#8592;|&larr;/gi, "←")
    .replace(/&#8594;|&rarr;/gi, "→")
    .replace(/&nbsp;/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const hasBackAffordance = (t) => t.includes("←") || /\bprevious\b/i.test(t);
const hasForwardAffordance = (t) => t.includes("→") || /\bnext\s+issue\b/i.test(t);

/**
 * Issue numbers reached from `html` by links that read as previous-issue
 * (and separately, next-issue) navigation.
 */
export function navTargets(html) {
  const prev = new Set();
  const next = new Set();
  for (const m of html.matchAll(ANCHOR)) {
    const target = issueTargetOf(m[1]);
    if (target === null) continue;
    const text = visibleText(m[2]);
    if (hasBackAffordance(text)) prev.add(target);
    if (hasForwardAffordance(text)) next.add(target);
  }
  return { prev: [...prev].sort((a, b) => a - b), next: [...next].sort((a, b) => a - b) };
}

// -------------------------------------------------------------
// 0. CONTROLS — the classifier actually discriminates
//
// Mutation coverage: each control is the guard's own failure mode. If
// any of these stops holding, every assertion below can pass vacuously.
// -------------------------------------------------------------
describe("navigation classifier controls", () => {
  test("recognises every href form used across the corpus", () => {
    assert.equal(issueTargetOf("https://marineintelligenceweekly.com/index22.html"), 22);
    assert.equal(issueTargetOf("https://www.marineintelligenceweekly.com/index19.html"), 19);
    assert.equal(issueTargetOf("/index26.html"), 26);
    assert.equal(issueTargetOf("index29.html"), 29);
    assert.equal(issueTargetOf("../index29.html"), 29);
    assert.equal(issueTargetOf("/index27.html#feature"), 27);
  });

  test("does not mistake non-issue links for issue links", () => {
    assert.equal(issueTargetOf("/index.html"), null);
    assert.equal(issueTargetOf("#takeaway"), null);
    assert.equal(issueTargetOf("/archive/index.html"), null);
    assert.equal(issueTargetOf("https://api.whatsapp.com/send?text=index25.html"), null);
    assert.equal(issueTargetOf(""), null);
  });

  test("a back affordance is required — editorial prose is not navigation", () => {
    // Shaped after index25's real archive-pointer sentence. Classifying
    // this as navigation is exactly the mistake that would have had us
    // rewrite a correct sentence about MSC 111.
    const prose = '<div class="archive-pointer">Also from MSC 111 — covered in Issue 22: '
      + '<a href="https://marineintelligenceweekly.com/index22.html">'
      + 'marineintelligenceweekly.com/index22.html</a></div>';
    assert.deepEqual(navTargets(prose).prev, []);

    const nav = '<a href="https://marineintelligenceweekly.com/index22.html">&#8592; Issue 22</a>';
    assert.deepEqual(navTargets(nav).prev, [22]);

    const worded = '<a href="/index29.html">Previous Issue &mdash; 29</a>';
    assert.deepEqual(navTargets(worded).prev, [29]);
  });

  test("catches a WRONG predecessor, not merely a missing one", () => {
    // The defect class R5 exists to prevent: a link that resolves fine and
    // looks like navigation, but points at the wrong issue.
    const wrong = '<a href="/index22.html">&#8592; Issue 22</a>';
    assert.deepEqual(navTargets(wrong).prev, [22]);
    assert.notDeepEqual(navTargets(wrong).prev, [24]);

    const missing = '<a href="/index.html">Home</a>';
    assert.deepEqual(navTargets(missing).prev, []);
  });

  test("a next-issue link would be detected if one were ever added", () => {
    const fwd = '<a href="/index31.html">Next Issue &#8594;</a>';
    assert.deepEqual(navTargets(fwd).next, [31]);
    // A same-page teaser anchor is not a next-issue link.
    assert.deepEqual(navTargets('<a href="#teaser">Next Issue</a>').next, []);
  });
});

// -------------------------------------------------------------
// 1. THE CHAIN — Issues 23..30 each point at their predecessor
// -------------------------------------------------------------
describe("previous-issue chain (root pages)", () => {
  for (const n of ISSUES.filter((n) => n >= CHAIN_STARTS_AT)) {
    test(`index${n} points back to Issue ${n - 1}`, () => {
      const { prev } = navTargets(read(rootPage(n)));
      assert.deepEqual(
        prev, [n - 1],
        `index${n} previous-issue navigation should reach exactly Issue ${n - 1}, got [${prev}]`,
      );
    });
  }
});

describe("previous-issue chain (archive copies)", () => {
  for (const n of ISSUES.filter((n) => n >= CHAIN_STARTS_AT)) {
    test(`archive/issue${n} points back to Issue ${n - 1}`, () => {
      const { prev } = navTargets(read(archivePage(n)));
      assert.deepEqual(prev, [n - 1]);
    });
  }
});

// -------------------------------------------------------------
// 2. RECORDED HISTORY — pages that legitimately have no prev link
// -------------------------------------------------------------
describe("pre-convention issues are left as published", () => {
  for (const n of ISSUES.filter((n) => NO_PREV_LINK.has(n))) {
    test(`index${n} has no previous-issue navigation (as published)`, () => {
      assert.deepEqual(navTargets(read(rootPage(n))).prev, []);
    });
  }

  test("index20 does carry its masthead link to Issue 19", () => {
    // Explicitly pinned: this page was once recorded as having no
    // previous link. It has one, and losing it would be a regression.
    assert.deepEqual(navTargets(read(rootPage(20))).prev, [19]);
  });
});

// -------------------------------------------------------------
// 3. NO NEXT LINKS — house convention, and no pointer at Issue 31
// -------------------------------------------------------------
describe("absent-next convention", () => {
  for (const n of ISSUES) {
    test(`index${n} has no next-issue link`, () => {
      assert.deepEqual(navTargets(read(rootPage(n))).next, []);
    });
  }

  test("no page anywhere references an unpublished issue", () => {
    const offenders = [];
    for (const n of ISSUES) {
      for (const rel of [rootPage(n), archivePage(n)]) {
        if (!fs.existsSync(path.join(ROOT, rel))) continue;
        const html = read(rel);
        for (const m of html.matchAll(ANCHOR)) {
          const t = issueTargetOf(m[1]);
          if (t !== null && t > 30) offenders.push(`${rel} -> Issue ${t}`);
        }
      }
    }
    assert.deepEqual(offenders, []);
  });
});

// -------------------------------------------------------------
// 4. ROOT AND ARCHIVE AGREE
//
// The archive twin is a verbatim copy, so its navigation must read
// identically. A divergence here means one of the pair was edited alone —
// the exact silent drift the R1 contract exists to prevent.
// -------------------------------------------------------------
describe("root and archive navigation agree", () => {
  for (const n of ISSUES) {
    const arc = archivePage(n);
    test(`Issue ${n}: archive copy navigates like its root twin`, () => {
      if (!fs.existsSync(path.join(ROOT, arc))) {
        assert.fail(`${arc} is missing — archive continuity is broken`);
      }
      assert.deepEqual(navTargets(read(arc)), navTargets(read(rootPage(n))));
    });
  }
});
