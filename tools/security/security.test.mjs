// =============================================================
// Marine Intelligence Weekly — Security V2 test suite
// Run: npm run security:test      (node --test tools/security/)
//
// Offline by design: no network, no Redis, no Razorpay, no SMTP,
// no secrets. Razorpay and Redis are injected as fakes so the REAL
// decision logic in api/_lib/ is what gets exercised.
//
// Each block ends with a POSITIVE CONTROL: a deliberately bad
// fixture that must be REJECTED. A guard that never fires is not a
// guard, so we prove each one can fail before trusting that it passes.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const { resolvePurchase, PRODUCTS, PurchaseError } =
  await import("../../api/_lib/products.js");
const { requiredEntitlementForPath } = await import("../../api/_lib/routes.js");
const {
  createSessionToken, verifySessionToken, newSessionId,
  hashPassword, verifyPassword, sessionCookies, SESSION_COOKIE,
} = await import("../../api/_lib/session.js");
const { fulfilPayment, FulfilError } = await import("../../api/_lib/fulfil.js");

// -------------------------------------------------------------
// 1. PRICE AUTHORITY
// -------------------------------------------------------------
describe("price authority — the server owns the amount", () => {

  test("SOLVED_QP is exactly INR 150000 paise (₹1,500)", () => {
    const p = resolvePurchase({ product: "SOLVED_QP" });
    assert.equal(p.amount, 150000);
    assert.equal(p.currency, "INR");
    assert.equal(p.productId, "SOLVED_QP");
  });

  test("existing Oral prices are preserved verbatim", () => {
    assert.equal(resolvePurchase({ product: "ORAL_QB_NOTES", tier: "standard" }).amount, 149900);
    assert.equal(resolvePurchase({ product: "ORAL_QB_NOTES", tier: "founders" }).amount, 89900);
  });

  test("a client-supplied amount cannot influence the price", () => {
    // Every one of these is what an attacker would actually send.
    for (const amount of [1, 100, 149900, 150001, 0, -5000, "150000", null, NaN]) {
      const p = resolvePurchase({ product: "SOLVED_QP", tier: "standard", amount });
      assert.equal(p.amount, 150000, `amount=${amount} must not change the charge`);
    }
  });

  test("legacy storefront tiers still map to the Oral product", () => {
    assert.equal(resolvePurchase({ tier: "standard" }).productId, "ORAL_QB_NOTES");
    assert.equal(resolvePurchase({ tier: "founders" }).productId, "ORAL_QB_NOTES");
  });

  test("unknown products and tiers are refused", () => {
    assert.throws(() => resolvePurchase({ product: "FREE_STUFF" }), PurchaseError);
    assert.throws(() => resolvePurchase({}), PurchaseError);
    assert.throws(() => resolvePurchase({ tier: "vip" }), PurchaseError);
  });

  test("BUNDLE cannot be purchased until a price is approved", () => {
    assert.throws(() => resolvePurchase({ product: "BUNDLE" }), PurchaseError);
  });

  test("POSITIVE CONTROL: a wrong expected price is detected", () => {
    const p = resolvePurchase({ product: "SOLVED_QP" });
    assert.notEqual(p.amount, 149900, "guard would be blind to a ₹1,499 substitution");
    assert.notEqual(p.amount, 1500, "₹1,500 must be expressed in paise, not rupees");
  });
});

// -------------------------------------------------------------
// 2. ROUTE POLICY
// -------------------------------------------------------------
describe("route policy — which URL needs which entitlement", () => {

  test("Written delivery surface requires SOLVED_QP", () => {
    assert.equal(requiredEntitlementForPath("/solvedQP/"), "SOLVED_QP");
    assert.equal(requiredEntitlementForPath("/solvedQP/QP2601.html"), "SOLVED_QP");
    assert.equal(requiredEntitlementForPath("/solvedQP"), "SOLVED_QP");
  });

  test("Written review output under meoclass1 also requires SOLVED_QP", () => {
    // Critical: this must NOT resolve to ORAL_QB_NOTES, or every Oral
    // customer silently receives the whole ₹1,500 Written library.
    assert.equal(
      requiredEntitlementForPath("/meoclass1/pastpapers/QP2601.html"), "SOLVED_QP"
    );
    assert.equal(requiredEntitlementForPath("/meoclass1/pastpapers/index.html"), "SOLVED_QP");
  });

  test("Oral surfaces require ORAL_QB_NOTES", () => {
    assert.equal(requiredEntitlementForPath("/meoclass1/QB1_A.html"), "ORAL_QB_NOTES");
    assert.equal(requiredEntitlementForPath("/meoclass1/oralnotes/index.html"), "ORAL_QB_NOTES");
    assert.equal(requiredEntitlementForPath("/meoclass1/index.html"), "ORAL_QB_NOTES");
  });

  test("public surfaces need nothing", () => {
    for (const p of ["/", "/SQ/", "/SQ/index.html", "/SQ/pay.html",
                     "/SQ/solved-qp-sample-january-2026.html", "/index.html"]) {
      assert.equal(requiredEntitlementForPath(p), null, `${p} must stay public`);
    }
  });

  test("path traversal cannot dodge a rule", () => {
    assert.equal(requiredEntitlementForPath("/SQ/../solvedQP/QP2601.html"), "SOLVED_QP");
    assert.equal(requiredEntitlementForPath("//solvedQP//QP2601.html"), "SOLVED_QP");
    assert.equal(requiredEntitlementForPath("/meoclass1/../meoclass1/QB1_A.html"), "ORAL_QB_NOTES");
  });

  test("POSITIVE CONTROL: an unprotected paid path would be caught", () => {
    assert.notEqual(
      requiredEntitlementForPath("/meoclass1/QB1_A.html"), null,
      "paid Oral content must never resolve to public"
    );
    assert.notEqual(
      requiredEntitlementForPath("/solvedQP/QP2607.html"), null,
      "paid Written content must never resolve to public"
    );
  });
});

// -------------------------------------------------------------
// 3. SESSION TOKENS
// -------------------------------------------------------------
describe("session tokens — unforgeable, identifying, expiring", () => {

  test("a minted token verifies and carries identity", () => {
    const sid = newSessionId();
    const t = createSessionToken("buyer@example.com", sid);
    const p = verifySessionToken(t);
    assert.ok(p);
    assert.equal(p.e, "buyer@example.com");
    assert.equal(p.s, sid);
  });

  test("the old miw_auth=1 cookie is not a token and proves nothing", () => {
    assert.equal(verifySessionToken("1"), null);
    assert.equal(verifySessionToken("miw_auth=1"), null);
    assert.equal(verifySessionToken(""), null);
    assert.equal(verifySessionToken(null), null);
  });

  test("a tampered payload is rejected", () => {
    const t = createSessionToken("buyer@example.com", newSessionId());
    const [v, payload, sig] = t.split(".");
    // Re-encode the payload claiming a different account.
    const evil = Buffer.from(JSON.stringify({
      e: "attacker@example.com", s: "x", x: Math.floor(Date.now() / 1000) + 999,
    })).toString("base64url");
    assert.equal(verifySessionToken(`${v}.${evil}.${sig}`), null);
    assert.equal(verifySessionToken(`${v}.${payload}.${"a".repeat(sig.length)}`), null);
  });

  test("a token signed with the wrong secret is rejected", () => {
    const t = createSessionToken("buyer@example.com", newSessionId());
    const good = process.env.MIW_SESSION_SECRET;
    process.env.MIW_SESSION_SECRET = "a-different-secret-000000000000000";
    const result = verifySessionToken(t);
    process.env.MIW_SESSION_SECRET = good;
    assert.equal(result, null);
  });

  test("an expired token is rejected", () => {
    const t = createSessionToken("buyer@example.com", newSessionId(), -1);
    assert.equal(verifySessionToken(t), null);
  });

  test("the session cookie is HttpOnly and Secure; the UI flag is not authority", () => {
    const [session, flag] = sessionCookies(createSessionToken("a@b.com", newSessionId()));
    assert.match(session, new RegExp(`^${SESSION_COOKIE}=`));
    assert.match(session, /HttpOnly/);
    assert.match(session, /Secure/);
    assert.match(session, /SameSite=Lax/);
    // miw_auth deliberately carries no token material at all.
    assert.match(flag, /^miw_auth=1;/);
    assert.doesNotMatch(flag, /HttpOnly/);
  });

  test("password hashing verifies, and legacy plaintext NO LONGER verifies at all", () => {
    const h = hashPassword("MIW-abc12345");
    assert.match(h, /^sha256\$/);
    assert.deepEqual(verifyPassword(h, "MIW-abc12345"), { ok: true });
    assert.deepEqual(verifyPassword(h, "wrong"), { ok: false });

    // This assertion is INVERTED from what it said before the incident
    // remediation. A plaintext record used to authenticate and report
    // itself as upgradeable; every credential exposed in public git
    // history was usable for exactly that reason. It now fails, and
    // the `legacy` flag it used to return no longer exists.
    assert.deepEqual(verifyPassword("MIW-abc12345", "MIW-abc12345"), { ok: false });
    assert.equal(verifyPassword("MIW-abc12345", "nope").ok, false);
  });

  test("POSITIVE CONTROL: a forged token must not verify", () => {
    const forged = "v1." +
      Buffer.from(JSON.stringify({ e: "attacker@example.com", s: "s", x: 9999999999 }))
        .toString("base64url") + ".not-a-real-signature";
    assert.equal(verifySessionToken(forged), null, "forgery guard is inert");
  });
});

// -------------------------------------------------------------
// 4. PAYMENT FULFILMENT
// -------------------------------------------------------------

/** Minimal in-memory Redis + Razorpay doubles. */
function harness({ order, payment, existingUser = null }) {
  const kv = new Map();
  // Production seeds this counter at 28 (28 pool passwords already
  // issued before the counter existed). The fake pool here has 2, so
  // start it at 0 — this is fixture setup, not a behaviour change.
  kv.set("miw:password_counter", "0");
  if (existingUser) kv.set(`miw:user:${order.notes.buyer_email}`, existingUser);
  const granted = [];
  const mails = [];
  const store = {
    get: async (k) => (kv.has(k) ? kv.get(k) : null),
    set: async (k, v) => { kv.set(k, v); return true; },
    incr: async (k) => { const n = Number(kv.get(k) || 0) + 1; kv.set(k, String(n)); return n; },
    setNX: async (k, v) => { if (kv.has(k)) return false; kv.set(k, v); return true; },
    del: async (k) => { kv.delete(k); return 1; },
    grant: async (email, ents) => { granted.push({ email, ents }); return true; },
  };
  return {
    kv, granted, mails, store,
    deps: {
      store,
      passwordPool: ["MIW-testpw01", "MIW-testpw02"],
      sendMail: async (m) => { mails.push(m); return { messageId: "test" }; },
      razorpayGet: async (path) => {
        if (path.startsWith("/v1/orders/")) return { status: 200, data: order };
        if (path.startsWith("/v1/payments/")) return { status: 200, data: payment };
        return { status: 404, data: {} };
      },
    },
  };
}

const goodOrder = (over = {}) => ({
  id: "order_TEST1", amount: 150000, currency: "INR",
  notes: { product: "SOLVED_QP", tier: "standard", buyer_email: "buyer@example.com", buyer_name: "Test" },
  ...over,
});
const goodPayment = (over = {}) => ({
  id: "pay_TEST1", order_id: "order_TEST1", amount: 150000,
  currency: "INR", status: "captured", ...over,
});

describe("payment fulfilment — the signature is not the authority", () => {

  test("a correct ₹1,500 SOLVED_QP payment grants exactly SOLVED_QP", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment() });
    const r = await fulfilPayment({
      orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps,
    });
    assert.equal(r.status, "granted");
    assert.equal(r.productId, "SOLVED_QP");
    assert.deepEqual(h.granted[0].ents, ["SOLVED_QP"]);
    assert.equal(h.mails.length, 1);
    assert.match(h.mails[0].subject, /Solved Question Papers/);
  });

  test("a ₹1 payment MUST NOT grant Solved QP", async () => {
    const h = harness({
      order: goodOrder({ amount: 100 }), payment: goodPayment({ amount: 100 }),
    });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e instanceof FulfilError && e.code === "amount_mismatch"
    );
    assert.equal(h.granted.length, 0, "nothing may be granted");
    assert.equal(h.mails.length, 0, "no access email may be sent");
  });

  test("₹1,499 must not buy the ₹1,500 product", async () => {
    const h = harness({
      order: goodOrder({ amount: 149900 }), payment: goodPayment({ amount: 149900 }),
    });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "amount_mismatch"
    );
    assert.equal(h.granted.length, 0);
  });

  test("an order amount that matches but a payment that does not is refused", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment({ amount: 100 }) });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "amount_mismatch"
    );
    assert.equal(h.granted.length, 0);
  });

  test("non-INR is refused", async () => {
    const h = harness({
      order: goodOrder({ currency: "USD" }), payment: goodPayment({ currency: "USD" }),
    });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "currency_mismatch"
    );
  });

  test("an uncaptured payment is refused", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment({ status: "authorized" }) });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "not_captured"
    );
  });

  test("a payment belonging to a different order is refused", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment({ order_id: "order_OTHER" }) });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "order_payment_mismatch"
    );
  });

  test("an order with no server-authored product is refused", async () => {
    const h = harness({
      order: goodOrder({ notes: { buyer_email: "buyer@example.com" } }), payment: goodPayment(),
    });
    await assert.rejects(
      () => fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps }),
      (e) => e.code === "unknown_product"
    );
  });

  test("replay is idempotent — one grant, one email", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment() });
    const a = { orderId: "order_TEST1", paymentId: "pay_TEST1", source: "verify-payment", deps: h.deps };
    const first = await fulfilPayment(a);
    const second = await fulfilPayment({ ...a, source: "webhook" });
    assert.equal(first.status, "granted");
    assert.equal(second.status, "already_processed");
    assert.equal(h.granted.length, 1, "must not grant twice");
    assert.equal(h.mails.length, 1, "must not send a duplicate credential email");
  });

  test("an existing Oral customer buying Written keeps their login and gains SOLVED_QP", async () => {
    const h = harness({
      order: goodOrder(), payment: goodPayment(),
      existingUser: hashPassword("MIW-existing1"),
    });
    const r = await fulfilPayment({
      orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps,
    });
    assert.equal(r.isUpgrade, true);
    assert.deepEqual(h.granted[0].ents, ["SOLVED_QP"], "adds Written only — never revokes Oral");
    // No new password is issued, and none is emailed.
    assert.doesNotMatch(h.mails[0].html, /Your Login Credentials/);
    assert.match(h.mails[0].html, /added to that same account/);
  });

  test("a new buyer's password is stored hashed, never in plaintext", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment() });
    await fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps });
    const stored = h.kv.get("miw:user:buyer@example.com");
    assert.match(stored, /^sha256\$/);
    assert.ok(!stored.includes("MIW-testpw01"), "plaintext must not be stored");
    // But the buyer is still told their password in the email.
    assert.match(h.mails[0].html, /MIW-testpw01/);
  });

  test("a failure inside the lock releases it so a retry can succeed", async () => {
    const h = harness({ order: goodOrder(), payment: goodPayment() });
    let attempt = 0;
    const flaky = { ...h.deps, sendMail: async (m) => {
      if (++attempt === 1) throw new Error("SMTP down");
      h.mails.push(m); return {};
    }};
    await assert.rejects(() => fulfilPayment({
      orderId: "order_TEST1", paymentId: "pay_TEST1", source: "webhook", deps: flaky,
    }));
    assert.equal(h.kv.has("miw:send_lock:pay_TEST1"), false, "lock must be released");
    const retry = await fulfilPayment({
      orderId: "order_TEST1", paymentId: "pay_TEST1", source: "webhook", deps: flaky,
    });
    assert.equal(retry.status, "granted");
  });

  test("POSITIVE CONTROL: the amount guard fires on a tampered fixture", async () => {
    // Deliberately corrupt the catalogue expectation by shipping an
    // order that claims SOLVED_QP at the Oral price. If this passes,
    // every other amount assertion above is meaningless.
    const h = harness({
      order: goodOrder({ amount: 89900 }), payment: goodPayment({ amount: 89900 }),
    });
    let fired = false;
    try {
      await fulfilPayment({ orderId: "order_TEST1", paymentId: "pay_TEST1", source: "test", deps: h.deps });
    } catch (e) { fired = e.code === "amount_mismatch"; }
    assert.equal(fired, true, "amount guard did not fire — it is inert");
  });
});
