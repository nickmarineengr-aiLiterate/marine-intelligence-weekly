// =============================================================
// Marine Intelligence Weekly — entitlement admin tool test suite
// Run: node --test tools/security/*.test.mjs
//
// Offline: no network, no Redis, no secrets. The module is imported,
// not executed, so nothing here reaches for KV credentials.
//
// THE POINT OF THIS FILE
// ----------------------
// The support tool is the only place a human looks at a customer's
// entitlement, and for a week after the one-year term shipped it was
// wrong in both directions at once:
//
//   READING  it printed "YES" only for the literal "1", so a customer
//            with a perfectly good dated grant read as "no". The obvious
//            operator response to "no" is to grant access to someone who
//            already has it, or to tell a paying customer they have none.
//
//   WRITING  every grant wrote "1". A one-year buyer with a failed
//            checkout was silently handed a perpetual grant by the repair,
//            and nothing anywhere would ever surface it.
//
// Neither defect could be seen from the output: both produced a
// confident, plausible line of text. So the tests below assert on the
// two things an operator cannot check by eye — what a value MEANS, and
// what value is about to be WRITTEN.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

import {
  describeGrant,
  resolveTerm,
  grantValueToWrite,
} from "./entitlement_admin.mjs";
import { PERPETUAL, grantAllowsAccess } from "../../api/_lib/grants.js";
import { DEFAULT_TERM_DAYS } from "../../api/_lib/products.js";

// A fixed clock. Every expectation below is arithmetic from these two,
// so nothing in this file depends on the day it is run.
const NOW_MS = Date.parse("2026-08-16T12:00:00Z");
const NOW = Math.floor(NOW_MS / 1000);
const DAY = 86400;

describe("show: what an operator is told", () => {
  test("an account with no grant reads as none", () => {
    assert.equal(describeGrant(undefined, NOW), "none");
    assert.equal(describeGrant(null, NOW), "none");
    assert.equal(describeGrant("", NOW), "none");
  });

  test("a grandfathered lifetime customer reads as PERPETUAL", () => {
    const out = describeGrant(PERPETUAL, NOW);
    assert.match(out, /PERPETUAL/);
    assert.match(out, /never expires/);
  });

  test("THE DEFECT: an active dated customer must NEVER read as 'no'", () => {
    // This is the exact case that made the old tool dangerous. A customer
    // who paid ₹1,500 four months ago, with eight months still to run,
    // was printed as "no".
    const eightMonthsOut = String(NOW + 243 * DAY);
    const out = describeGrant(eightMonthsOut, NOW);

    assert.doesNotMatch(out, /^no$/);
    assert.doesNotMatch(out, /\bnone\b/);
    assert.match(out, /ACTIVE/);
    // And the operator is told WHEN, because "active" alone does not
    // answer the question a customer actually asks.
    assert.match(out, /until 2027-04-16/);
    assert.match(out, /243 days left/);
  });

  test("an expired dated customer reads as EXPIRED, with the date", () => {
    const lastWeek = String(NOW - 7 * DAY);
    const out = describeGrant(lastWeek, NOW);
    assert.match(out, /EXPIRED/);
    assert.match(out, /2026-08-09/);
    assert.doesNotMatch(out, /ACTIVE/);
  });

  test("one second past expiry is EXPIRED, one second short of it is ACTIVE", () => {
    assert.match(describeGrant(String(NOW + 1), NOW), /ACTIVE/);
    assert.match(describeGrant(String(NOW - 1), NOW), /EXPIRED/);
  });

  test("a corrupt value is reported as corrupt, not quietly as access", () => {
    const out = describeGrant("banana", NOW);
    assert.match(out, /EXPIRED/);
    assert.match(out, /corrupt/);
  });

  test("the four states are all distinguishable from one another", () => {
    // A positive control on the display itself: if two states ever
    // collapsed to the same sentence the tool would be useless for the
    // one job it has.
    const seen = new Set([
      describeGrant(undefined, NOW),
      describeGrant(PERPETUAL, NOW),
      describeGrant(String(NOW + 30 * DAY), NOW),
      describeGrant(String(NOW - 30 * DAY), NOW),
    ]);
    assert.equal(seen.size, 4);
  });

  test("the display never echoes the raw stored value", () => {
    // Operator output is pasted into support threads. The stored value is
    // not a secret, but there is no reason for it to travel.
    const raw = String(NOW + 30 * DAY);
    assert.ok(!describeGrant(raw, NOW).includes(raw));
  });
});

describe("grant: which term is chosen", () => {
  const argv = (...flags) => ["node", "tool", "grant", "a@b.com", "SOLVED_QP", ...flags];

  test("the default term is the catalogue term, not a number typed here", () => {
    const term = resolveTerm(argv(), NOW_MS);
    assert.equal(term.perpetual, false);
    assert.equal(term.termDays, DEFAULT_TERM_DAYS);
  });

  test("THE DEFECT: the default support grant is NOT perpetual", () => {
    // The whole incident in one assertion. A support correction for a
    // current customer must not mint lifetime rights.
    assert.equal(resolveTerm(argv(), NOW_MS).perpetual, false);
    assert.notEqual(grantValueToWrite(undefined, resolveTerm(argv(), NOW_MS), NOW_MS), PERPETUAL);
  });

  test("--days takes an explicit number of days", () => {
    assert.equal(resolveTerm(argv("--days", "30"), NOW_MS).termDays, 30);
  });

  test("--until targets the END of the named day, so that day is included", () => {
    const term = resolveTerm(argv("--until", "2027-08-14"), NOW_MS);
    const value = grantValueToWrite(undefined, term, NOW_MS);
    const expiry = new Date(Number(value) * 1000).toISOString();
    assert.match(expiry, /^2027-08-14T23:59:59/);
  });

  test("--perpetual is available, because legacy restoration must stay possible", () => {
    assert.equal(resolveTerm(argv("--perpetual"), NOW_MS).perpetual, true);
  });

  test("two term flags at once is an error, not a silent winner", () => {
    assert.throws(() => resolveTerm(argv("--days", "30", "--perpetual"), NOW_MS), /ONE of/);
    assert.throws(() => resolveTerm(argv("--days", "30", "--until", "2027-01-01"), NOW_MS), /ONE of/);
  });

  test("a malformed or backwards term is refused rather than guessed at", () => {
    assert.throws(() => resolveTerm(argv("--days", "0"), NOW_MS), /positive/);
    assert.throws(() => resolveTerm(argv("--days", "later"), NOW_MS), /positive/);
    assert.throws(() => resolveTerm(argv("--until", "14-08-2027"), NOW_MS), /YYYY-MM-DD/);
    assert.throws(() => resolveTerm(argv("--until", "2020-01-01"), NOW_MS), /in the past/);
  });
});

describe("grant: which value is written", () => {
  const oneYear = { perpetual: false, termDays: DEFAULT_TERM_DAYS };

  test("a first-time repair writes a dated grant one year out", () => {
    const value = grantValueToWrite(undefined, oneYear, NOW_MS);
    assert.equal(value, String(NOW + 365 * DAY));
    assert.equal(grantAllowsAccess(value, NOW), true);
    assert.equal(grantAllowsAccess(value, NOW + 366 * DAY), false);
  });

  test("LEGACY RIGHTS ARE FROZEN: a dated repair can never downgrade a perpetual holder", () => {
    // The operator types the ordinary repair command against a
    // grandfathered account. The account must come out the other side
    // still perpetual — not converted to a dated year by the fix.
    const value = grantValueToWrite(PERPETUAL, oneYear, NOW_MS);
    assert.equal(value, PERPETUAL);
    assert.equal(grantAllowsAccess(value, NOW + 50 * 365 * DAY), true);
  });

  test("a running term is EXTENDED from its own expiry, never restarted from today", () => {
    // Restarting from today would silently confiscate the months a
    // customer had already paid for.
    const existing = String(NOW + 200 * DAY);
    const value = grantValueToWrite(existing, oneYear, NOW_MS);
    assert.equal(value, String(NOW + 200 * DAY + 365 * DAY));
    assert.ok(Number(value) > Number(existing));
  });

  test("a lapsed term restarts from today rather than from the old expiry", () => {
    const value = grantValueToWrite(String(NOW - 100 * DAY), oneYear, NOW_MS);
    assert.equal(value, String(NOW + 365 * DAY));
  });

  test("explicit legacy restoration writes the canonical perpetual literal", () => {
    const value = grantValueToWrite(undefined, { perpetual: true }, NOW_MS);
    assert.equal(value, PERPETUAL);
    assert.equal(value, "1");
    assert.match(describeGrant(value, NOW), /PERPETUAL/);
    assert.equal(grantAllowsAccess(value, NOW + 100 * 365 * DAY), true);
  });

  test("POSITIVE CONTROL: a grant can be seen to shorten nothing, ever", () => {
    // Sweep every shape a stored value takes against every term shape.
    const existings = [undefined, PERPETUAL, String(NOW + 10 * DAY), String(NOW - 10 * DAY)];
    const terms = [oneYear, { perpetual: false, termDays: 1 }, { perpetual: true }];
    for (const existing of existings) {
      for (const term of terms) {
        const value = grantValueToWrite(existing, term, NOW_MS);
        if (existing === PERPETUAL) {
          assert.equal(value, PERPETUAL, "a perpetual holder stayed perpetual");
        }
        // Whatever was granted, the account holds access immediately after.
        assert.equal(grantAllowsAccess(value, NOW), true);
      }
    }
  });
});
