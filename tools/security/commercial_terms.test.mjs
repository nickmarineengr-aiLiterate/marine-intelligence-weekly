// =============================================================
// Marine Intelligence Weekly — commercial terms contract
// Run: node --test tools/security/*.test.mjs
//
// Offline: reads the shipped HTML off disk. No network, no secrets.
//
// THE POINT OF THIS FILE
// ----------------------
// From 15 August 2026 a new purchase buys ONE YEAR. Customers who bought
// before that hold Candidate-Lifecycle Access: no expiry date, running
// for their MEO Class I preparation, closable by the Founder once MIW
// has reliable confirmation that they passed.
//
// Both statements are true at once, and that is what makes the copy
// hard: "lifetime" is a lie on a page inviting a purchase today, AND an
// over-promise even to the earlier cohort, whose access was never sold
// as until-death. For a week after the term shipped, the trial page, the
// pay page and the homepage all still said "lifetime access" beside a
// ₹1,500 buy button.
//
// SO THIS IS NOT A BANNED-WORD TEST.
//
// A blanket ban on "lifetime" would fire on the engineering corpus,
// where "the catalyst's lifetime" is ordinary technical prose, and on
// the Terms clause that has to NAME the old wording in order to define
// it. Instead every occurrence on a commercial surface must be
// JUSTIFIED by something near it. An unjustified occurrence is a defect
// and fails.
//
// It also guards the ₹899/month plan that was cancelled on 16 August
// 2026 before going live. Removing an announcement is easy; keeping it
// removed is what a test is for, because a disabled card, a hidden div
// and a "coming soon" comment all still ship the promise.
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

describe("the cancelled ₹899/month plan is gone from every current surface", () => {
  // Not just absent from the rendered page — absent from the FILE. A
  // display:none card, a disabled button and an HTML comment reading
  // "₹899/month planned" are all still shipped to anyone who reads the
  // source, and all three were plausible ways to "remove" this card.
  const KILLED = [
    "₹899 <span>/ month</span>",
    "899 / month",
    "899/month",
    "Moving to a bigger platform",
    "From 1 September",
    "Details coming 1 September",
    "monthly subscription",
    "new signups from September",
  ];
  const CURRENT_SURFACES = [
    "SQ/index.html", "SQ/pay.html", "SQ/trial.html", "index.html", "terms.html",
  ];

  for (const path of CURRENT_SURFACES) {
    test(`${path} carries no trace of the abandoned monthly plan`, () => {
      const html = read(path);
      const found = KILLED.filter((k) => occurrences(html, k).length > 0);
      assert.deepEqual(found, [], `${path} still ships: ${found.join(", ")}`);
    });
  }

  test("the storefront advertises no recurring charge at all", () => {
    const html = read("SQ/index.html");
    assert.doesNotMatch(html, /\/\s*month/i);
    assert.doesNotMatch(html, /per month/i);
  });

  test("POSITIVE CONTROL: the monthly-plan detector can be seen to fire", () => {
    const fake = '<div class="tier-price">₹899 <span>/ month</span></div>';
    assert.equal(KILLED.some((k) => occurrences(fake, k).length > 0), true);
  });
});

describe("legacy members hold Candidate-Lifecycle Access, not until-death access", () => {
  test("the pay page's legacy wording is gated on server-reported perpetual", () => {
    const html = read("SQ/pay.html");
    const hits = occurrences(html, "Candidate-Lifecycle Access — your original access remains active.");
    assert.equal(hits.length, 1, "the legacy line should exist exactly once");

    // Prove the gate, not just the proximity: the branch condition must
    // be the perpetual flag, and it must sit between the `if` and the text.
    const before = html.slice(Math.max(0, hits[0] - 600), hits[0]);
    assert.match(before, /if\s*\(a\.perpetual\)/);
  });

  test("the internal word PERPETUAL never reaches a customer's eyes", () => {
    // It is the stored SHAPE, not the commercial term. Rendering it would
    // both confuse and over-promise. Comments are stripped before the
    // check because the file must be free to explain itself.
    const rendered = read("SQ/pay.html")
      .replace(/\/\*[\s\S]*?\*\//g, "")
      .replace(/^\s*\/\/.*$/gm, "");
    for (const word of ["Perpetual access", "PERPETUAL access", "Lifetime access"]) {
      assert.equal(occurrences(rendered, word).length, 0, `pay.html renders "${word}"`);
    }
  });

  test("a dated customer is shown a date, never an unbounded promise", () => {
    const html = read("SQ/pay.html");
    assert.match(html, /a\.expires[\s\S]{0,200}Access until/);
  });

  test("Terms define Candidate-Lifecycle Access and name the old wording once", () => {
    const terms = read("terms.html");
    assert.match(terms, /Candidate-Lifecycle Access/);
    // The old phrase must appear, in quotes, to connect the definition to
    // what these members were actually told — but only where it is being
    // defined, never as a live claim.
    assert.match(terms, /previously described as "lifetime access", is\s+Candidate-Lifecycle Access/);
    assert.match(terms, /until you pass the MEO Class I examination/);
    assert.match(terms, /does not mean access for the\s+natural lifetime of the purchaser/);
  });

  test("Terms state that closure needs reliable confirmation, not detection", () => {
    const terms = read("terms.html");
    assert.match(terms, /We do not monitor examination results/);
    assert.match(terms, /reliable confirmation that a member has passed/);
    // No claim of continuous monitoring — the system genuinely has none.
    assert.doesNotMatch(terms, /automatically detect|monitor your progress|track your result/i);
  });

  test("Terms keep inactivity and credential reset out of the entitlement question", () => {
    const terms = read("terms.html");
    assert.match(terms, /Not logging in is not passing/);
    assert.match(terms, /We do not close, suspend or expire accounts\s+for inactivity/);
    assert.match(terms, /A password reset is a security step,\s+not a decision about your access/);
  });

  test("Terms no longer promise the earlier cohort an unending grant", () => {
    const terms = read("terms.html");
    // "carry no end date" was true of the STORED VALUE and false of the
    // commercial term. It read as until-death and had to go.
    assert.doesNotMatch(terms, /carry no end date/i);
    assert.doesNotMatch(terms, /access does not stop when you pass/i);
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
    assert.match(terms, /Purchases made on or after 15 August 2026 — one year/);
    assert.match(terms, /These provide one year of access<\/strong>, running\s+from the date of purchase/);
  });

  test("no dormancy mechanism was built to match the removed clause", () => {
    // A guard against 'fixing' the contradiction in the other direction.
    // Removing published policy is the reversible choice; building
    // inactivity expiry would be a new product decision.
    const grants = read("api/_lib/grants.js");
    assert.doesNotMatch(grants, /lastLogin|last_login|dormant|inactiv/i);
  });
});
