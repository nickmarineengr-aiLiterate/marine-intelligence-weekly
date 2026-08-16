// =============================================================
// Marine Intelligence Weekly — commercial terms contract
// Run: node --test tools/security/*.test.mjs
//
// Offline: reads the shipped HTML off disk. No network, no secrets.
//
// THE POINT OF THIS FILE
// ----------------------
// From 15 August 2026 a new purchase buys ONE YEAR. Customers who bought
// before that hold a genuinely perpetual grant and are being honoured.
//
// Both statements are true at once, and that is exactly what makes the
// copy hard: the word "lifetime" is a lie on a page inviting a purchase
// today, and the plain truth on a page describing what an existing
// customer already holds. For a week after the term shipped, the trial
// page, the pay page and the homepage all still said "lifetime access"
// beside a ₹1,500 buy button.
//
// SO THIS IS NOT A BANNED-WORD TEST.
//
// A blanket ban on "lifetime" would delete the one honest use of it and
// would fire on the engineering corpus, where "the catalyst's lifetime"
// is ordinary technical prose. Instead every occurrence on a commercial
// surface must be JUSTIFIED by something near it — a perpetual gate, or
// an explicit statement of who it applies to. An unjustified occurrence
// is a defect and fails.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const read = (p) => readFileSync(join(ROOT, p), "utf8");

/** Every index at which `needle` occurs, case-insensitively. */
function occurrences(haystack, needle) {
  const hits = [];
  const h = haystack.toLowerCase();
  const n = needle.toLowerCase();
  let i = h.indexOf(n);
  while (i !== -1) {
    hits.push(i);
    i = h.indexOf(n, i + 1);
  }
  return hits;
}

/** The text around an occurrence, which is where its justification must live. */
function context(text, at, before = 500, after = 200) {
  return text.slice(Math.max(0, at - before), at + after);
}

// -------------------------------------------------------------
// The surfaces on which a candidate is invited to BUY. Nothing here may
// promise access that a purchase made today does not actually deliver.
// -------------------------------------------------------------
const NEW_SALE_SURFACES = ["SQ/trial.html", "SQ/pay.html", "SQ/index.html", "index.html"];

// Phrases that describe an unbounded grant. Each needs justification.
const UNBOUNDED_CLAIMS = [
  "lifetime access",
  "get lifetime access",
  "lifetime — ₹",
  "all future solved papers",
  "all future papers",
  "unlimited access",
  "access forever",
  "forever access",
];

// A nearby marker proving the claim is scoped to the grandfathered
// cohort rather than offered to today's buyer.
const LEGACY_MARKERS = [
  "a.perpetual",            // the pay-page branch, gated on server truth
  "perpetual",
  "bought before",
  "purchased before",
  "original purchase",
];

describe("new-sale surfaces promise only what a purchase delivers", () => {
  for (const path of NEW_SALE_SURFACES) {
    test(`${path} makes no unjustified unbounded-access claim`, () => {
      const html = read(path);
      const unjustified = [];

      for (const claim of UNBOUNDED_CLAIMS) {
        for (const at of occurrences(html, claim)) {
          const near = context(html, at).toLowerCase();
          const justified = LEGACY_MARKERS.some((m) => near.includes(m.toLowerCase()));
          if (!justified) {
            unjustified.push(`"${claim}" at offset ${at}: ${context(html, at, 90, 90).trim()}`);
          }
        }
      }

      assert.deepEqual(
        unjustified,
        [],
        `${path} offers unbounded access to a new buyer:\n  ` + unjustified.join("\n  ")
      );
    });
  }

  test("POSITIVE CONTROL: the check can be seen to fire", () => {
    // If this ever stops failing, the detector has been broken and every
    // test above is passing vacuously.
    const fake = '<a class="btn" href="/SQ/#pricing">Get lifetime access ₹1,500 →</a>';
    const found = occurrences(fake, "lifetime access");
    assert.equal(found.length, 1);
    const near = context(fake, found[0]).toLowerCase();
    assert.equal(LEGACY_MARKERS.some((m) => near.includes(m)), false);
  });
});

describe("the current offer is stated, not merely implied", () => {
  test("the trial page invites a one-year purchase for both products", () => {
    const html = read("SQ/trial.html");
    assert.match(html, /Get one-year access/);
    assert.match(html, /One year of access: ₹1,500/);
    // The CTA is shared by both products, so Oral cannot drift alone.
    assert.equal(occurrences(html, "Get one-year access").length >= 2, true);
  });

  test("the pay page invites a one-year purchase", () => {
    assert.match(read("SQ/pay.html"), /Get one-year access/);
  });

  test("the Written storefront card bounds its 'future papers' promise", () => {
    const html = read("SQ/index.html");
    assert.match(html, /Every paper published during your access year included/);
    assert.doesNotMatch(html, /All future solved papers included/);
    assert.match(html, /One year of access: ₹1,500/);
  });

  test("the Oral storefront card and homepage state a one-year term", () => {
    assert.match(read("SQ/index.html"), /One year of access, one payment/);
    assert.match(read("index.html"), /₹1,499 for one year of access/);
  });
});

describe("legacy customers keep what they bought", () => {
  test("the pay page's lifetime wording is gated on server-reported perpetual", () => {
    const html = read("SQ/pay.html");
    const hits = occurrences(html, "Lifetime access — yours from the original purchase");
    assert.equal(hits.length, 1, "the legacy line should exist exactly once");

    // Prove the gate, not just the proximity: the branch condition must
    // be the perpetual flag, and it must sit between the `if` and the text.
    const before = html.slice(Math.max(0, hits[0] - 400), hits[0]);
    assert.match(before, /if\s*\(a\.perpetual\)/);
  });

  test("a dated customer is shown a date, never a lifetime promise", () => {
    const html = read("SQ/pay.html");
    assert.match(html, /a\.expires[\s\S]{0,200}Access until/);
  });

  test("the storefront's grandfathering line names who it applies to", () => {
    const html = read("SQ/index.html");
    // The promise itself must survive — it is real and must not be
    // deleted for the sake of removing a word.
    assert.match(html, /keep their original lifetime access — unaffected/);
    assert.match(html, /bought before 15 August 2026 keep their original lifetime access/);
  });

  test("Terms honour the earlier lifetime offer without redefining it", () => {
    const terms = read("terms.html");
    assert.match(terms, /hold "lifetime access", and we are\s+honouring it/);
    assert.match(terms, /Those earlier purchases carry no end date/);

    // The retroactive reinterpretation is gone. It was published after
    // those customers bought, contradicted the code (which grants true
    // perpetuity), and rested on a pass-status mechanism that has never
    // existed.
    assert.doesNotMatch(terms, /until you pass the examination/i);
    assert.doesNotMatch(terms, /not access in perpetuity/i);
  });
});

describe("Terms describe only mechanisms that exist", () => {
  test("the unimplemented 18-month dormancy policy is gone", () => {
    const terms = read("terms.html");
    // There is no last-login field, no inactivity tracker, no cron and no
    // credential TTL anywhere in the system. Publishing the policy while
    // nothing can execute it is a promise to no one and a threat to
    // everyone.
    assert.doesNotMatch(terms, /dormant/i);
    assert.doesNotMatch(terms, /eighteen months/i);
    assert.doesNotMatch(terms, /18 months/i);
  });

  test("the replacement says only what the system actually does", () => {
    const terms = read("terms.html");
    assert.match(terms, /We do not close, suspend or expire accounts\s+for inactivity/);
  });

  test("the one-year term and its start date are stated", () => {
    const terms = read("terms.html");
    assert.match(terms, /on or after 15 August 2026 provide one year of access/);
  });

  test("no dormancy mechanism was built to match the removed clause", () => {
    // A guard against 'fixing' the contradiction in the other direction.
    // Removing published policy is the reversible choice; building
    // inactivity expiry would be a new product decision.
    const grants = read("api/_lib/grants.js");
    assert.doesNotMatch(grants, /lastLogin|last_login|dormant|inactiv/i);
  });
});
