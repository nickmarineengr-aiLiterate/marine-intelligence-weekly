// =============================================================
// Marine Intelligence Weekly — Candidate-Lifecycle member state
// Run: node --test tools/security/*.test.mjs
//
// Offline: pure functions only. No Redis, no secrets, no network.
//
// WHAT THIS FILE IS DEFENDING
// ---------------------------
// Access sold before 15 August 2026 is Candidate-Lifecycle Access. It
// has no clock, and the Founder may close it once MIW has reliable
// confirmation that the member passed MEO Class I.
//
// Three things can go wrong, and each is worse than the last:
//
//   1. A closure that does not close. The member keeps reading a paid
//      product the Founder believes is shut off.
//   2. A closure that closes too much. A member who separately bought a
//      one-year Written term loses a product they paid for, because
//      somebody marked their legacy Oral access passed.
//   3. A closure that cannot be undone. The Founder marks the wrong
//      person, and there is no way back to what they held.
//
// (2) is the one this file works hardest at. It is also the one nobody
// would notice for months, because the affected customer is a person who
// stopped being able to open something they never asked about.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

import {
  grantState,
  grantAllowsAccess,
  grantHasLapsed,
  markPassedValue,
  reopenedGrantValue,
  extendedGrantValue,
  parsePassedValue,
  PERPETUAL,
  GRANT_NONE,
  GRANT_PERPETUAL,
  GRANT_ACTIVE,
  GRANT_EXPIRED,
  GRANT_PASSED_CLOSED,
} from "../../api/_lib/grants.js";

import {
  planMarkPassed,
  planReopen,
  describeGrant,
  summariseCounts,
} from "./entitlement_admin.mjs";

const KNOWN = ["ORAL_QB_NOTES", "SOLVED_QP"];

// A fixed clock, so nothing here depends on the day it is run.
const NOW_MS = Date.parse("2026-08-16T12:00:00Z");
const NOW = Math.floor(NOW_MS / 1000);

const inAYear = String(NOW + 365 * 86400);
const lastMonth = String(NOW - 30 * 86400);

/** What mark-passed writes for a lifecycle grant at NOW. */
const CLOSED = markPassedValue(PERPETUAL, NOW_MS);

// -------------------------------------------------------------
describe("authorization: the four states the gate must distinguish", () => {
  test("LEGACY ACTIVE — a lifecycle grant with no closure ALLOWS", () => {
    assert.equal(grantState(PERPETUAL, NOW).status, GRANT_PERPETUAL);
    assert.equal(grantAllowsAccess(PERPETUAL, NOW), true);
  });

  test("LEGACY PASSED — a closed lifecycle grant DENIES", () => {
    assert.equal(grantState(CLOSED, NOW).status, GRANT_PASSED_CLOSED);
    assert.equal(grantAllowsAccess(CLOSED, NOW), false);
  });

  test("LEGACY REOPENED — restoring puts the original grant back, and it ALLOWS", () => {
    const restored = reopenedGrantValue(CLOSED);
    assert.equal(restored, PERPETUAL);
    assert.equal(grantAllowsAccess(restored, NOW), true);
  });

  test("DATED ACTIVE — an in-term one-year grant ALLOWS", () => {
    assert.equal(grantState(inAYear, NOW).status, GRANT_ACTIVE);
    assert.equal(grantAllowsAccess(inAYear, NOW), true);
  });

  test("DATED EXPIRED — a run-out one-year grant DENIES", () => {
    assert.equal(grantState(lastMonth, NOW).status, GRANT_EXPIRED);
    assert.equal(grantAllowsAccess(lastMonth, NOW), false);
  });

  test("a closure denies no matter how far in the past it was made", () => {
    const old = markPassedValue(PERPETUAL, NOW_MS - 5 * 365 * 86400000);
    assert.equal(grantAllowsAccess(old, NOW), false);
    // ...and still denies against a clock long after it, i.e. nothing
    // about a closure decays back into access with the passage of time.
    assert.equal(grantAllowsAccess(old, NOW + 100 * 365 * 86400), false);
  });

  test("REGRESSION: a closure is not readable as a 1970 epoch", () => {
    // The whole family of bugs this codebase has already been bitten by
    // is "the value got coerced to a number". Number("passed:...") is
    // NaN, which the corrupt branch would deny — correct, but it would
    // lose the reason and the prior value, so reopen could not work.
    assert.equal(Number.isNaN(Number(CLOSED)), true);
    const s = grantState(CLOSED, NOW);
    assert.equal(s.status, GRANT_PASSED_CLOSED);
    assert.equal(s.prior, PERPETUAL);
    assert.equal(s.closedAt, NOW);
  });

  test("a closure is not a LAPSE — the pay page must not offer a renewal date", () => {
    // grantHasLapsed drives copy that prints an end date beside a renew
    // button. A closure has no end date, and a member's exam result is
    // private: it must not surface as a banner.
    assert.equal(grantHasLapsed(CLOSED, NOW), false);
    assert.equal(grantHasLapsed(lastMonth, NOW), true);
  });

  test("a malformed closure still DENIES rather than falling open", () => {
    for (const bad of ["passed:", "passed:abc:1", "passed:0:1", "passed:123", "passed:123:"]) {
      assert.equal(grantAllowsAccess(bad, NOW), false, `${bad} allowed access`);
      assert.equal(parsePassedValue(bad), null, `${bad} parsed as valid`);
    }
  });
});

// -------------------------------------------------------------
describe("mark-passed can only ever close a Candidate-Lifecycle grant", () => {
  test("a lifecycle grant is eligible", () => {
    assert.equal(typeof markPassedValue(PERPETUAL, NOW_MS), "string");
    assert.equal(typeof markPassedValue(1, NOW_MS), "string");
  });

  test("a dated grant, an absent grant and a closed grant are all INELIGIBLE", () => {
    // This single property is the product-separation guarantee. There is
    // no code path from mark-passed to a dated value, so no amount of
    // operator error can convert somebody's paid Written year into a
    // closure.
    assert.equal(markPassedValue(inAYear, NOW_MS), null);
    assert.equal(markPassedValue(lastMonth, NOW_MS), null);
    assert.equal(markPassedValue(undefined, NOW_MS), null);
    assert.equal(markPassedValue(null, NOW_MS), null);
    assert.equal(markPassedValue("", NOW_MS), null);
    assert.equal(markPassedValue(CLOSED, NOW_MS), null);
  });

  test("PRODUCT SEPARATION: closing legacy Oral leaves a paid Written year intact", () => {
    // The exact account shape from the Founder's brief: one email, a
    // grandfathered Oral grant and a separately-bought one-year Written
    // term. Marking them passed with no product named — the ordinary,
    // most dangerous case — must close one and not the other.
    const held = { ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: inAYear };
    const plan = planMarkPassed(held, KNOWN, NOW_MS);

    const oral = plan.find((p) => p.entitlement === "ORAL_QB_NOTES");
    const written = plan.find((p) => p.entitlement === "SOLVED_QP");

    assert.equal(oral.action, "close");
    assert.equal(written.action, "skip");
    assert.match(written.reason, /UNTOUCHED/);

    // Apply the plan and re-read: Written must still authorise.
    const after = { ...held };
    for (const p of plan) if (p.value) after[p.entitlement] = p.value;

    assert.equal(grantAllowsAccess(after.ORAL_QB_NOTES, NOW), false);
    assert.equal(grantAllowsAccess(after.SOLVED_QP, NOW), true);
    assert.equal(after.SOLVED_QP, inAYear, "the Written value was rewritten");
  });

  test("the reverse account shape is equally safe", () => {
    const held = { ORAL_QB_NOTES: inAYear, SOLVED_QP: PERPETUAL };
    const after = { ...held };
    for (const p of planMarkPassed(held, KNOWN, NOW_MS)) {
      if (p.value) after[p.entitlement] = p.value;
    }
    assert.equal(grantAllowsAccess(after.ORAL_QB_NOTES, NOW), true);
    assert.equal(after.ORAL_QB_NOTES, inAYear);
    assert.equal(grantAllowsAccess(after.SOLVED_QP, NOW), false);
  });

  test("marking one product explicitly never reaches the other field", () => {
    const held = { ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: PERPETUAL };
    const plan = planMarkPassed(held, ["ORAL_QB_NOTES"], NOW_MS);
    assert.equal(plan.length, 1);
    assert.equal(plan[0].entitlement, "ORAL_QB_NOTES");
  });

  test("a member holding BOTH as lifecycle has both closed", () => {
    const held = { ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: PERPETUAL };
    const plan = planMarkPassed(held, KNOWN, NOW_MS);
    assert.equal(plan.filter((p) => p.action === "close").length, 2);
  });

  test("IDEMPOTENT: marking an already-closed member changes nothing", () => {
    const held = { ORAL_QB_NOTES: CLOSED };
    const plan = planMarkPassed(held, ["ORAL_QB_NOTES"], NOW_MS + 86400000);
    assert.equal(plan[0].action, "skip");
    assert.match(plan[0].reason, /already closed/);
    // Crucially the original closure timestamp is not overwritten, so a
    // second run does not rewrite the audit trail.
    assert.equal(grantState(held.ORAL_QB_NOTES, NOW).closedAt, NOW);
  });

  test("an account with nothing to close reports so rather than writing", () => {
    const plan = planMarkPassed({}, KNOWN, NOW_MS);
    assert.equal(plan.every((p) => p.action === "skip" && p.value === null), true);
    assert.match(plan[0].reason, /nothing to close/);
  });

  test("every entitlement is reported, including the untouched ones", () => {
    // Silence about a skipped product is how an operator concludes it was
    // closed too.
    const plan = planMarkPassed({ ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: inAYear }, KNOWN, NOW_MS);
    assert.deepEqual(plan.map((p) => p.entitlement), KNOWN);
    assert.equal(plan.every((p) => typeof p.reason === "string" && p.reason.length > 0), true);
  });
});

// -------------------------------------------------------------
describe("reopen-candidate restores exactly what was held", () => {
  test("a closed lifecycle grant is restored to its original value", () => {
    const plan = planReopen({ ORAL_QB_NOTES: CLOSED }, ["ORAL_QB_NOTES"]);
    assert.equal(plan[0].action, "reopen");
    assert.equal(plan[0].value, PERPETUAL);
    assert.equal(grantAllowsAccess(plan[0].value, NOW), true);
  });

  test("the round trip is lossless", () => {
    const closed = markPassedValue(PERPETUAL, NOW_MS);
    assert.equal(reopenedGrantValue(closed), PERPETUAL);
  });

  test("reopen cannot MINT access for somebody who was never closed", () => {
    // The restored value is recovered from the record, never
    // reconstructed. Reopening an account with no closure must be a
    // no-op, or the command becomes "grant perpetual access to anyone
    // you can name" with a friendlier word on it.
    for (const raw of [undefined, null, "", inAYear, lastMonth, PERPETUAL, "garbage"]) {
      assert.equal(reopenedGrantValue(raw), null);
    }
    const plan = planReopen({ SOLVED_QP: inAYear }, ["SOLVED_QP"]);
    assert.equal(plan[0].action, "skip");
    assert.equal(plan[0].value, null);
  });

  test("reopen does not touch a dated grant sitting beside the closed one", () => {
    const held = { ORAL_QB_NOTES: CLOSED, SOLVED_QP: inAYear };
    const after = { ...held };
    for (const p of planReopen(held, KNOWN)) if (p.value) after[p.entitlement] = p.value;
    assert.equal(after.ORAL_QB_NOTES, PERPETUAL);
    assert.equal(after.SOLVED_QP, inAYear);
  });

  test("close → reopen → close returns to a denying state", () => {
    let v = PERPETUAL;
    v = markPassedValue(v, NOW_MS);
    assert.equal(grantAllowsAccess(v, NOW), false);
    v = reopenedGrantValue(v);
    assert.equal(grantAllowsAccess(v, NOW), true);
    v = markPassedValue(v, NOW_MS);
    assert.equal(grantAllowsAccess(v, NOW), false);
  });
});

// -------------------------------------------------------------
describe("commercial history survives a closure", () => {
  test("a closed member is distinguishable from one who never purchased", () => {
    assert.equal(grantState(undefined, NOW).status, GRANT_NONE);
    assert.equal(grantState(CLOSED, NOW).status, GRANT_PASSED_CLOSED);
    assert.notEqual(grantState(CLOSED, NOW).status, GRANT_NONE);
  });

  test("the closure records WHEN and WHAT was closed", () => {
    const s = grantState(CLOSED, NOW);
    assert.equal(s.closedAt, NOW);
    assert.equal(s.prior, PERPETUAL);
  });

  test("a member who buys again after closing becomes a dated customer", () => {
    // Not a restoration. Extending a closure into a fresh perpetual grant
    // would silently undo the Founder's decision by way of a purchase.
    const next = extendedGrantValue(CLOSED, 365, NOW_MS);
    assert.equal(next, String(NOW + 365 * 86400));
    assert.equal(grantState(next, NOW).status, GRANT_ACTIVE);
    assert.equal(grantState(next, NOW).perpetual, false);
  });

  test("a live lifecycle grant is still never downgraded by a purchase", () => {
    // The pre-existing guarantee, re-asserted because isLifecycleValue()
    // now stands where a literal comparison used to.
    assert.equal(extendedGrantValue(PERPETUAL, 365, NOW_MS), PERPETUAL);
    assert.equal(extendedGrantValue(1, 365, NOW_MS), PERPETUAL);
  });
});

// -------------------------------------------------------------
describe("what the operator is shown", () => {
  test("show names the lifecycle state in operator language", () => {
    assert.match(describeGrant(PERPETUAL, NOW), /Candidate-Lifecycle \/ ACTIVE/);
    assert.match(describeGrant(CLOSED, NOW), /Candidate-Lifecycle \/ PASSED_CLOSED/);
    assert.match(describeGrant(CLOSED, NOW), /2026-08-16/);
    assert.match(describeGrant(inAYear, NOW), /ACTIVE until/);
    assert.match(describeGrant(lastMonth, NOW), /EXPIRED on/);
    assert.equal(describeGrant(undefined, NOW), "none");
  });

  test("no stored value is ever echoed back to the terminal", () => {
    // describeGrant is the only thing `show` prints per product. A raw
    // value in operator output is a value in a screenshot, a support
    // thread and a scrollback buffer.
    for (const raw of [PERPETUAL, CLOSED, inAYear, lastMonth]) {
      assert.equal(describeGrant(raw, NOW).includes(String(raw)), false,
        `describeGrant echoed the stored value for ${raw}`);
    }
  });

  test("the four Founder-facing counts add up from stored data alone", () => {
    const records = [
      { email: "a", held: { ORAL_QB_NOTES: PERPETUAL } },
      { email: "b", held: { ORAL_QB_NOTES: CLOSED } },
      { email: "c", held: { ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: inAYear } },
      { email: "d", held: { SOLVED_QP: lastMonth } },
      { email: "e", held: {} },
    ];
    const c = summariseCounts(records, NOW, KNOWN);
    assert.equal(c.accounts, 5);
    assert.equal(c.lifecycleActive, 2);        // a, c
    assert.equal(c.lifecyclePassedClosed, 1);  // b
    assert.equal(c.fixedTermActive, 1);        // c
    assert.equal(c.fixedTermExpired, 1);       // d
    assert.equal(c.corrupt, 0);
  });

  test("an unreadable stored value is counted separately, not as an expiry", () => {
    const c = summariseCounts([{ email: "x", held: { SOLVED_QP: "??" } }], NOW, KNOWN);
    assert.equal(c.corrupt, 1);
    assert.equal(c.fixedTermExpired, 0);
  });
});

// -------------------------------------------------------------
describe("no automatic pass detection exists anywhere", () => {
  test("nothing in the grant logic reads a clock to infer a pass", () => {
    // Founder policy is explicit: no cron, no inactivity rule, no
    // results scraping, no bulk closure. A closure is a value somebody
    // wrote on purpose, and the only way to produce one is
    // markPassedValue(), which takes an existing grant and a timestamp
    // and nothing else. This asserts the shape of that API rather than
    // grepping for words.
    assert.equal(markPassedValue.length, 2);
    // No amount of elapsed time turns a live lifecycle grant into a
    // closed one.
    const farFuture = NOW + 50 * 365 * 86400;
    assert.equal(grantState(PERPETUAL, farFuture).status, GRANT_PERPETUAL);
    assert.equal(grantAllowsAccess(PERPETUAL, farFuture), true);
  });
});
