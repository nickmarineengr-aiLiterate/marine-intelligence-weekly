// =============================================================
// Marine Intelligence Weekly — Entitlement term test suite
// Run: node --test tools/security/
//
// Offline: no network, no Redis, no secrets.
//
// THE POINT OF THIS FILE
// ----------------------
// Purchases carry a one-year term from August 2026. Roughly a hundred
// customers bought before that under an explicit, published promise of
// lifetime access, and their records hold the literal "1".
//
// Number("1") is 1, which is 1 January 1970. An arithmetic-first
// reading of the stored value therefore expires every one of those
// customers at once, silently, on the first request after deploy.
// There is no error and nothing in a log — the gate simply starts
// denying people who paid.
//
// Most of what follows exists to make that specific mistake impossible
// to ship.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const {
  grantState, grantAllowsAccess, grantHasLapsed, grantValueFor,
  extendedGrantValue, PERPETUAL,
  GRANT_NONE, GRANT_PERPETUAL, GRANT_ACTIVE, GRANT_EXPIRED,
} = await import("../../api/_lib/grants.js");

const { authorizeRequest } = await import("../../api/_lib/routes.js");
const { resolvePurchase, DEFAULT_TERM_DAYS, PRODUCTS } =
  await import("../../api/_lib/products.js");

const DAY = 86400;
const NOW = 1_786_700_000;          // a plausible 2026 second

// -------------------------------------------------------------
// 1. GRANDFATHERING — the population that must not break
// -------------------------------------------------------------
describe("grandfathered lifetime customers", () => {

  test('"1" is perpetual and never expires', () => {
    const s = grantState("1", NOW);
    assert.equal(s.status, GRANT_PERPETUAL);
    assert.equal(s.perpetual, true);
    assert.equal(s.expires, null);
  });

  test('"1" still grants access a century from now', () => {
    const century = NOW + 100 * 365 * DAY;
    assert.equal(grantAllowsAccess("1", century), true,
      'a lifetime customer must not expire because time passed');
  });

  test("THE 1970 TRAP: a numeric reading of \"1\" must never be used", () => {
    // This is the failure being guarded. If grantState ever parses
    // before it compares, "1" becomes epoch second 1 — long past — and
    // every grandfathered customer is locked out in one deploy.
    assert.ok(Number("1") < NOW, "fixture sanity: 1 really is in the past");
    assert.equal(grantAllowsAccess("1", NOW), true,
      'arithmetic-first parsing has been reintroduced in grants.js');
    assert.notEqual(grantState("1", NOW).status, GRANT_EXPIRED);
  });

  test("the redis numeric form of 1 is treated the same as the string", () => {
    // Upstash can hand back a number rather than a string.
    assert.equal(grantAllowsAccess(1, NOW), true);
    assert.equal(grantState(1, NOW).status, GRANT_PERPETUAL);
  });

  test("a perpetual holder is never reported as lapsed", () => {
    assert.equal(grantHasLapsed("1", NOW), false);
    assert.equal(grantHasLapsed("1", NOW + 100 * 365 * DAY), false);
  });

  test("POSITIVE CONTROL: the perpetual branch is distinguishable", () => {
    // If everything returned perpetual, every test above passes for the
    // wrong reason. A stale stamp must still expire.
    assert.equal(grantState(String(NOW - 1), NOW).status, GRANT_EXPIRED);
    assert.notEqual(grantState("1", NOW).status,
                    grantState(String(NOW - 1), NOW).status);
  });
});

// -------------------------------------------------------------
// 2. DATED GRANTS
// -------------------------------------------------------------
describe("one-year purchases", () => {

  test("a term of 365 days lands exactly 365 days out", () => {
    const nowMs = NOW * 1000;
    assert.equal(grantValueFor(365, nowMs), String(NOW + 365 * DAY));
  });

  test("the catalogue term is one year, and it is server-owned", () => {
    assert.equal(DEFAULT_TERM_DAYS, 365);
    assert.equal(resolvePurchase({ product: "SOLVED_QP" }).termDays, 365);
    assert.equal(resolvePurchase({ product: "ORAL_QB_NOTES" }).termDays, 365);
  });

  test("a buyer cannot choose their own term any more than their price", () => {
    for (const termDays of [99999, 0, -1, null, "3650"]) {
      const p = resolvePurchase({ product: "SOLVED_QP", termDays });
      assert.equal(p.termDays, 365, `termDays=${termDays} must be ignored`);
      assert.equal(p.amount, 150000);
    }
  });

  test("an in-term grant allows access; one second past does not", () => {
    assert.equal(grantAllowsAccess(String(NOW + 1), NOW), true);
    assert.equal(grantAllowsAccess(String(NOW), NOW), false);
    assert.equal(grantAllowsAccess(String(NOW - 1), NOW), false);
  });

  test("null term still means perpetual, so a comped account is possible", () => {
    assert.equal(grantValueFor(null, NOW * 1000), PERPETUAL);
  });

  test("absent means never had it, which is not the same as expired", () => {
    for (const raw of [null, undefined, ""]) {
      assert.equal(grantState(raw, NOW).status, GRANT_NONE);
      assert.equal(grantHasLapsed(raw, NOW), false);
    }
  });

  test("a corrupt value fails CLOSED", () => {
    for (const raw of ["banana", "-5", "0", "NaN"]) {
      assert.equal(grantAllowsAccess(raw, NOW), false, `${raw} must not open the gate`);
    }
  });
});

// -------------------------------------------------------------
// 3. RENEWAL AND UPGRADE — the downgrade hazards
// -------------------------------------------------------------
describe("extending a grant", () => {

  test("a perpetual customer who buys again STAYS perpetual", () => {
    // The hazard: a grandfathered customer buys the other product, a
    // blind write stamps a one-year expiry over their "1", and their
    // own payment silently downgrades them.
    assert.equal(extendedGrantValue("1", 365, NOW * 1000), PERPETUAL);
    assert.equal(extendedGrantValue(1, 365, NOW * 1000), PERPETUAL);
  });

  test("renewing early ADDS to the time already paid for", () => {
    const remaining = NOW + 100 * DAY;
    const renewed = Number(extendedGrantValue(String(remaining), 365, NOW * 1000));
    assert.equal(renewed, remaining + 365 * DAY,
      "renewing with 100 days left must not throw those 100 days away");
  });

  test("renewing after expiry runs from today, not from the old date", () => {
    const lapsed = NOW - 200 * DAY;
    const renewed = Number(extendedGrantValue(String(lapsed), 365, NOW * 1000));
    assert.equal(renewed, NOW + 365 * DAY,
      "a lapsed customer must get a full term, not one backdated into the past");
  });

  test("a first purchase runs a full term from today", () => {
    assert.equal(Number(extendedGrantValue(undefined, 365, NOW * 1000)), NOW + 365 * DAY);
  });

  test("POSITIVE CONTROL: extension can never shorten a grant", () => {
    // Any stored state, extended, must allow access for at least as
    // long as it did before.
    for (const existing of ["1", String(NOW + 500 * DAY), String(NOW + 1), undefined]) {
      const after = extendedGrantValue(existing, 365, NOW * 1000);
      const beforeOk = grantAllowsAccess(existing, NOW);
      const afterOk = grantAllowsAccess(after, NOW);
      if (beforeOk) {
        assert.equal(afterOk, true, `extending ${existing} revoked access`);
      }
      if (existing === "1") continue;
      if (existing && Number.isFinite(Number(existing))) {
        assert.ok(Number(after) >= Number(existing),
          `extending ${existing} moved the expiry BACKWARDS to ${after}`);
      }
    }
  });
});

// -------------------------------------------------------------
// 4. THE GATE
// -------------------------------------------------------------
describe("authorizeRequest with dated entitlements", () => {
  const base = {
    pathname: "/solvedQP/index.html",
    configured: true,
    payload: { e: "c@example.com", s: "s1", x: NOW + 9999 },
    sessionScore: "1",
    now: NOW,
  };

  test("a grandfathered customer is allowed, decades on", () => {
    const far = NOW + 30 * 365 * DAY;
    const d = authorizeRequest({
      ...base, now: far, payload: { ...base.payload, x: far + 9999 }, entitled: "1",
    });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "ok");
  });

  test("an in-term customer is allowed", () => {
    const d = authorizeRequest({ ...base, entitled: String(NOW + 10 * DAY) });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "ok");
  });

  test("a lapsed customer is denied as EXPIRED, not as a stranger", () => {
    const d = authorizeRequest({ ...base, entitled: String(NOW - 1) });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "expired",
      "a lapsed customer should be offered a renewal, not a first-time pitch");
  });

  test("a lapsed customer is NOT told to go and start a free trial", () => {
    // Their trial may well have been spent a year ago. "expired" must
    // win over both trial branches.
    const d = authorizeRequest({
      ...base, entitled: String(NOW - 1), trialExpiry: null,
    });
    assert.equal(d.reason, "expired");
    const d2 = authorizeRequest({
      ...base, entitled: String(NOW - 1), trialExpiry: String(NOW - 500 * DAY),
    });
    assert.equal(d2.reason, "expired");
  });

  test("a lapsed customer with a RUNNING trial still gets in", () => {
    // Unlikely, but the trial is a live grant and must be honoured.
    const d = authorizeRequest({
      ...base, entitled: String(NOW - 1), trialExpiry: String(NOW + 3600),
    });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "trial");
  });

  test("never bought is still noentitlement, distinct from expired", () => {
    const d = authorizeRequest({ ...base, entitled: null, trialExpiry: null });
    assert.equal(d.reason, "noentitlement");
  });

  test("POSITIVE CONTROL: a dated grant really can deny", () => {
    assert.equal(authorizeRequest({ ...base, entitled: String(NOW - 1) }).allow, false,
      "if this passes, the term is not being enforced at all");
  });

  test("POSITIVE CONTROL: every grandfathered path allows, on every route", () => {
    // The blast radius test. If this fails, ~100 paying customers are
    // locked out of everything.
    for (const p of ["/solvedQP/", "/solvedQP/QP2403.html",
                     "/meoclass1/", "/meoclass1/pastpapers/QP2601.html"]) {
      const d = authorizeRequest({ ...base, pathname: p, entitled: "1" });
      assert.equal(d.allow, true, `grandfathered customer denied on ${p}`);
    }
  });
});

// -------------------------------------------------------------
// 5. PRICE LADDER — declared, never computed
// -------------------------------------------------------------
describe("price ladder", () => {

  test("the ladder is declared on the product", () => {
    const l = PRODUCTS.SOLVED_QP.priceLadder;
    assert.equal(l.perExamYear, 50000, "₹500 per exam year, in paise");
    assert.equal(l.nextAmount, 200000, "₹2,000 once 2026 completes");
    assert.equal(l.stepsWhenYearCompletes, 2026);
  });

  test("the CURRENT price is still ₹1,500 — the ladder changes nothing by itself", () => {
    assert.equal(resolvePurchase({ product: "SOLVED_QP" }).amount, 150000,
      "no script may change what a candidate is charged");
  });
});
