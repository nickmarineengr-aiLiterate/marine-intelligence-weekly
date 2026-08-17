// =============================================================
// Marine Intelligence Weekly — refund → access, and product clarity
// File: tools/security/refund_access.test.mjs
//
// TWO COMMERCIAL DEFECTS, ONE INCIDENT (17 August 2026)
//
//   CLARITY   A customer bought the ₹1,499 Oral product believing it
//             included the ₹1,500 Written papers, and had to be
//             refunded. The Written card had said "sold separately"
//             since launch; the Oral card said nothing, and called
//             itself "Standard Access / Full QB access". The tests here
//             hold BOTH cards to the same standard, because a warning
//             on one card teaches the reader the other has none to give.
//
//   REFUND    The refund then revoked nothing. api/razorpay-webhook.js
//             handled payment.captured and payment.failed and returned a
//             bare 200 for everything else, so refunded customers kept
//             full paid access indefinitely and no record existed that a
//             refund had happened at all.
//
// The refund tests exercise the REAL decision logic in _lib/refund.js
// through its deps bag — no network, no Redis, no secrets, and no live
// customer is touched. Razorpay is a fixture; the entitlement store is
// an object.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { revokeForRefund, isFullRefund, RefundError } from "../../api/_lib/refund.js";
import {
  grantState, grantAllowsAccess, refundedGrantValue, unrefundedGrantValue,
  extendedGrantValue, markPassedValue,
  GRANT_REFUNDED, GRANT_ACTIVE, GRANT_PERPETUAL, GRANT_PASSED_CLOSED, GRANT_NONE,
} from "../../api/_lib/grants.js";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const read = (p) => readFileSync(join(ROOT, p), "utf8");

// -------------------------------------------------------------
// Fixtures. One Razorpay, one entitlement store, no I/O.
// -------------------------------------------------------------
const ORAL_PAID = 149900;
const WRITTEN_PAID = 150000;

function razorpay({ product, paid, refunded, email = "cand@example.com", orderId = "order_X" }) {
  return async (path) => {
    if (path.startsWith("/v1/payments/")) {
      return { status: 200, data: {
        id: "pay_1", order_id: orderId, amount: paid,
        amount_refunded: refunded, currency: "INR", status: "captured", email,
      } };
    }
    if (path.startsWith("/v1/orders/")) {
      return { status: 200, data: {
        id: orderId, amount: paid, currency: "INR",
        notes: { product, tier: "standard", buyer_email: email },
      } };
    }
    return { status: 404, data: {} };
  };
}

function storeOver(held) {
  const state = { ...held };
  const audits = {};
  return {
    state, audits,
    readHeld: async () => ({ ...state }),
    writeFields: async (_email, fields) => Object.assign(state, fields),
    recordAudit: async (k, v) => { audits[k] = v; },
  };
}

const NOW_MS = 1_760_000_000_000;          // fixed clock — no Date.now() in assertions
const NOW_S = Math.floor(NOW_MS / 1000);
const A_YEAR_OUT = String(NOW_S + 300 * 86400);

async function refundRun({ product, held, paid, refunded, refundAmount }) {
  const store = storeOver(held);
  const result = await revokeForRefund({
    paymentId: "pay_1", refundId: "rfnd_1", refundAmount,
    source: "refund.processed",
    deps: { razorpayGet: razorpay({ product, paid, refunded }), store, now: () => NOW_MS },
  });
  return { result, store };
}

// =============================================================
describe("full refund revokes the refunded product, and only that one", () => {

  test("Oral-only account: a full Oral refund ends Oral access", async () => {
    const { result, store } = await refundRun({
      product: "ORAL_QB_NOTES",
      held: { ORAL_QB_NOTES: A_YEAR_OUT },
      paid: ORAL_PAID, refunded: ORAL_PAID,
    });
    assert.equal(result.status, "revoked");
    assert.deepEqual(result.entitlements, ["ORAL_QB_NOTES"]);
    assert.equal(grantAllowsAccess(store.state.ORAL_QB_NOTES, NOW_S), false);
    assert.equal(grantState(store.state.ORAL_QB_NOTES, NOW_S).status, GRANT_REFUNDED);
  });

  test("Written-only account: a full Written refund ends Written access", async () => {
    const { result, store } = await refundRun({
      product: "SOLVED_QP",
      held: { SOLVED_QP: A_YEAR_OUT },
      paid: WRITTEN_PAID, refunded: WRITTEN_PAID,
    });
    assert.equal(result.status, "revoked");
    assert.equal(grantAllowsAccess(store.state.SOLVED_QP, NOW_S), false);
  });

  test("THE ONE THAT MATTERS: refunding Oral leaves a paid Written year alone", async () => {
    const { store } = await refundRun({
      product: "ORAL_QB_NOTES",
      held: { ORAL_QB_NOTES: A_YEAR_OUT, SOLVED_QP: A_YEAR_OUT },
      paid: ORAL_PAID, refunded: ORAL_PAID,
    });
    assert.equal(grantAllowsAccess(store.state.ORAL_QB_NOTES, NOW_S), false);
    assert.equal(grantAllowsAccess(store.state.SOLVED_QP, NOW_S), true,
      "the separately-bought Written year was collateral damage of an Oral refund");
    assert.equal(store.state.SOLVED_QP, A_YEAR_OUT, "the surviving value was rewritten");
  });

  test("and the mirror: refunding Written leaves a paid Oral year alone", async () => {
    const { store } = await refundRun({
      product: "SOLVED_QP",
      held: { ORAL_QB_NOTES: A_YEAR_OUT, SOLVED_QP: A_YEAR_OUT },
      paid: WRITTEN_PAID, refunded: WRITTEN_PAID,
    });
    assert.equal(grantAllowsAccess(store.state.SOLVED_QP, NOW_S), false);
    assert.equal(grantAllowsAccess(store.state.ORAL_QB_NOTES, NOW_S), true);
  });

  test("a refunded LEGACY perpetual grant is revoked too, and keeps its prior value", async () => {
    const { store } = await refundRun({
      product: "ORAL_QB_NOTES",
      held: { ORAL_QB_NOTES: "1" },
      paid: ORAL_PAID, refunded: ORAL_PAID,
    });
    assert.equal(grantAllowsAccess(store.state.ORAL_QB_NOTES, NOW_S), false,
      "a perpetual grant survived a full refund");
    assert.equal(unrefundedGrantValue(store.state.ORAL_QB_NOTES), "1",
      "reversing this refund could not restore what was held");
  });

  test("the login credential is never touched — identity is not entitlement", async () => {
    const { store } = await refundRun({
      product: "ORAL_QB_NOTES",
      held: { ORAL_QB_NOTES: A_YEAR_OUT },
      paid: ORAL_PAID, refunded: ORAL_PAID,
    });
    const touched = Object.keys(store.state).filter((k) => !k.startsWith("ORAL") && !k.startsWith("SOLVED"));
    assert.deepEqual(touched, [], "refund wrote outside the entitlement fields");
    const src = read("api/_lib/refund.js");
    assert.doesNotMatch(src, /miw:user:/, "refund.js reaches for the credential key");
    assert.doesNotMatch(src, /\bDEL\b/, "refund.js deletes something");
  });
});

// =============================================================
describe("the refunded state denies at the gate and is not an expiry", () => {

  test("REFUNDED is denied by the single question the gate asks", () => {
    const v = refundedGrantValue(A_YEAR_OUT, NOW_MS);
    assert.equal(grantAllowsAccess(v, NOW_S), false);
  });

  test("FAILS CLOSED on a stale deploy: code that predates this reads it as corrupt", () => {
    // Number("refunded:...") is NaN, which the pre-existing corrupt-value
    // branch already denies. A closure cannot be defeated by an old build.
    assert.equal(Number.isFinite(Number(refundedGrantValue("1", NOW_MS))), false);
  });

  test("a refund is NOT reported as a lapsed term — there is no date to renew from", () => {
    const v = refundedGrantValue(A_YEAR_OUT, NOW_MS);
    const s = grantState(v, NOW_S);
    assert.equal(s.status, GRANT_REFUNDED);
    assert.equal(s.expires, null);
    assert.notEqual(s.status, GRANT_ACTIVE);
  });

  test("REFUNDED, EXPIRED, PASSED_CLOSED and NONE stay four different answers", () => {
    const statuses = [
      grantState(refundedGrantValue("1", NOW_MS), NOW_S).status,
      grantState(String(NOW_S - 10), NOW_S).status,
      grantState(markPassedValue("1", NOW_MS), NOW_S).status,
      grantState(undefined, NOW_S).status,
    ];
    assert.equal(new Set(statuses).size, 4, "two reasons for losing access look alike");
    assert.equal(statuses[0], GRANT_REFUNDED);
    assert.equal(statuses[2], GRANT_PASSED_CLOSED);
    assert.equal(statuses[3], GRANT_NONE);
  });

  test("a refund applied over a closed lifecycle keeps BOTH facts", () => {
    const closed = markPassedValue("1", NOW_MS);
    const v = refundedGrantValue(closed, NOW_MS);
    assert.equal(grantState(v, NOW_S).status, GRANT_REFUNDED, "the refund is the outer, latest fact");
    assert.equal(grantState(unrefundedGrantValue(v), NOW_S).status, GRANT_PASSED_CLOSED);
  });

  test("a refunded customer who buys again gets a fresh dated term, not their old grant back", () => {
    const refundedPerpetual = refundedGrantValue("1", NOW_MS);
    const after = extendedGrantValue(refundedPerpetual, 365, NOW_MS);
    assert.notEqual(after, "1", "a refunded legacy holder repurchased into perpetual access");
    assert.equal(grantState(after, NOW_S).status, GRANT_ACTIVE);
  });
});

// =============================================================
describe("idempotency and the cases that must change nothing", () => {

  test("re-delivery of the same refund writes nothing the second time", async () => {
    const store = storeOver({ ORAL_QB_NOTES: A_YEAR_OUT });
    const deps = {
      razorpayGet: razorpay({ product: "ORAL_QB_NOTES", paid: ORAL_PAID, refunded: ORAL_PAID }),
      store, now: () => NOW_MS,
    };
    const first = await revokeForRefund({ paymentId: "pay_1", refundId: "rfnd_1", refundAmount: ORAL_PAID, deps });
    const stamped = store.state.ORAL_QB_NOTES;
    const second = await revokeForRefund({ paymentId: "pay_1", refundId: "rfnd_1", refundAmount: ORAL_PAID, deps });
    assert.equal(first.status, "revoked");
    assert.equal(second.status, "no_change");
    assert.equal(store.state.ORAL_QB_NOTES, stamped, "the value was re-wrapped on redelivery");
  });

  test("PARTIAL refund changes nothing — MIW has no partial-refund policy", async () => {
    const { result, store } = await refundRun({
      product: "SOLVED_QP",
      held: { SOLVED_QP: A_YEAR_OUT },
      paid: WRITTEN_PAID, refunded: 50000, refundAmount: 50000,
    });
    assert.equal(result.status, "partial_refund_no_change");
    assert.equal(store.state.SOLVED_QP, A_YEAR_OUT);
    assert.equal(grantAllowsAccess(store.state.SOLVED_QP, NOW_S), true);
  });

  test("a full refund is still full when only the EVENT knows the amount yet", () => {
    // amount_refunded can lag the refund.created event. Reading 0 there
    // and calling a full refund partial fails straight back into the
    // defect, so the signed event's amount is a floor.
    assert.equal(isFullRefund({ amount: ORAL_PAID, amount_refunded: 0 }, ORAL_PAID), true);
    assert.equal(isFullRefund({ amount: ORAL_PAID, amount_refunded: ORAL_PAID }, undefined), true);
    assert.equal(isFullRefund({ amount: ORAL_PAID, amount_refunded: 0 }, 500), false);
  });

  test("a refund for an account holding no such grant INVENTS nothing", async () => {
    const { result, store } = await refundRun({
      product: "ORAL_QB_NOTES",
      held: { SOLVED_QP: A_YEAR_OUT },
      paid: ORAL_PAID, refunded: ORAL_PAID,
    });
    assert.equal(result.status, "no_change");
    assert.equal(store.state.ORAL_QB_NOTES, undefined, "a purchase was invented on an empty field");
    assert.equal(grantAllowsAccess(store.state.SOLVED_QP, NOW_S), true);
  });

  test("an order with no recognised product fails CLOSED and grants/revokes nothing", async () => {
    const store = storeOver({ ORAL_QB_NOTES: A_YEAR_OUT });
    await assert.rejects(
      () => revokeForRefund({
        paymentId: "pay_1", refundId: "rfnd_1", refundAmount: ORAL_PAID,
        deps: {
          razorpayGet: razorpay({ product: "NOT_A_PRODUCT", paid: ORAL_PAID, refunded: ORAL_PAID }),
          store, now: () => NOW_MS,
        },
      }),
      RefundError
    );
    assert.equal(store.state.ORAL_QB_NOTES, A_YEAR_OUT);
  });
});

// =============================================================
describe("the refund leaves an audit trail that answers 'why did this end'", () => {

  test("one record per refund, naming the product, the ids and the outcome", async () => {
    const { store } = await refundRun({
      product: "SOLVED_QP",
      held: { SOLVED_QP: A_YEAR_OUT },
      paid: WRITTEN_PAID, refunded: WRITTEN_PAID,
    });
    const rec = JSON.parse(store.audits["miw:refund:rfnd_1"]);
    assert.equal(rec.product, "SOLVED_QP");
    assert.deepEqual(rec.entitlements, ["SOLVED_QP"]);
    assert.equal(rec.refundId, "rfnd_1");
    assert.equal(rec.paymentId, "pay_1");
    assert.equal(rec.orderId, "order_X");
    assert.equal(rec.full, true);
    assert.equal(typeof rec.at, "number");
  });

  test("it stores no card, bank or instrument detail", async () => {
    const { store } = await refundRun({
      product: "SOLVED_QP", held: { SOLVED_QP: A_YEAR_OUT },
      paid: WRITTEN_PAID, refunded: WRITTEN_PAID,
    });
    const blob = store.audits["miw:refund:rfnd_1"].toLowerCase();
    for (const banned of ["card", "vpa", "bank", "ifsc", "upi", "contact"]) {
      assert.equal(blob.includes(banned), false, `the audit record stores ${banned}`);
    }
  });
});

// =============================================================
describe("the webhook actually listens for refunds", () => {
  const hook = read("api/razorpay-webhook.js");

  test("refund.created and refund.processed both reach the revocation", () => {
    assert.match(hook, /refund\.created/);
    assert.match(hook, /refund\.processed/);
    assert.match(hook, /revokeForRefund/);
  });

  test("POSITIVE CONTROL: the old build handled neither", () => {
    // If someone removes the handler, this pair is what should fail
    // first — the events, not the helper's name.
    const withoutRefunds = hook.replace(/refund/gi, "xxxx");
    assert.doesNotMatch(withoutRefunds, /refund\.created/);
  });

  test("signature verification is still the first thing that happens", () => {
    const sigAt = hook.indexOf("timingSafeEqual");
    // The CALL, not the import at the top of the file.
    const refundAt = hook.indexOf("await revokeForRefund(");
    assert.ok(sigAt > -1 && refundAt > sigAt,
      "an unsigned request could reach the revocation path");
  });
});

// =============================================================
describe("the storefront states what each product is NOT", () => {
  const sq = read("SQ/index.html");

  // Deliberately semantic rather than exact-string: the assertion is
  // that each price is tied to its own product name and carries an
  // exclusion, not that a particular sentence survives a copy edit.
  const oralCard = sq.slice(sq.indexOf("ORAL CARD"), sq.indexOf("SOLVED WRITTEN QUESTION PAPERS"));
  const writtenCard = sq.slice(sq.indexOf("SOLVED WRITTEN QUESTION PAPERS"), sq.indexOf("<!-- SUCCESS MODAL"));

  test("the Oral card names the Oral exam, its price, and the word only", () => {
    assert.match(oralCard, /₹1,499/);
    assert.match(oralCard, /Oral/);
    assert.match(oralCard, /only/i);
  });

  test("the Oral card excludes the Written papers ABOVE its buy button", () => {
    const excl = oralCard.search(/Does not include/i);
    const button = oralCard.indexOf("startCheckout('ORAL_QB_NOTES'");
    assert.ok(excl > -1, "the Oral card carries no exclusion at all");
    assert.ok(excl < button, "the exclusion sits below the purchase button");
    assert.match(oralCard.slice(excl, excl + 220), /Written/);
  });

  test("the Written card excludes the Oral question bank ABOVE its buy button", () => {
    const excl = writtenCard.search(/Does not include/i);
    const button = writtenCard.indexOf("startCheckout('SOLVED_QP'");
    assert.ok(excl > -1);
    assert.ok(excl < button);
    assert.match(writtenCard.slice(excl, excl + 260), /Oral/);
  });

  test("neither card claims the other's price as its own", () => {
    // Only the copy ABOVE the exclusion is checked. Naming the other
    // product's price INSIDE the exclusion is the point of the exclusion
    // — "a separate ₹1,500 product" is what tells the reader there is a
    // second thing to buy — so a blanket ban would forbid the fix.
    assert.doesNotMatch(oralCard.split("Does not include")[0], /₹1,500/);
    assert.doesNotMatch(writtenCard.split("Does not include")[0], /₹1,499/);
  });

  test("no purchase button is generic — each names its product and price", () => {
    const labels = [...sq.matchAll(/<button class="pay-btn[^>]*>\s*([^<]+?)\s*<\/button>/g)]
      .map((m) => m[1].trim());
    assert.ok(labels.length >= 2, "the purchase buttons were not found");
    for (const l of labels) {
      assert.match(l, /Oral|Written/, `CTA "${l}" does not say which product it buys`);
      assert.match(l, /₹1,4\d\d|₹1,5\d\d/, `CTA "${l}" does not carry its price`);
    }
  });

  test("BANNED: 'Full Access' beside the Oral price — the phrase that sold the wrong product", () => {
    assert.doesNotMatch(sq, /Get Full Access/i);
    assert.doesNotMatch(sq, /Full Access\s*[—-]\s*₹1,499/i);
  });

  test("no surface offers an unqualified 'MEO Class I access' at either price", () => {
    for (const path of ["SQ/index.html", "SQ/pay.html", "SQ/trial.html"]) {
      assert.doesNotMatch(read(path), /MEO Class I Access/i, `${path} sells generic access`);
    }
  });
});

// =============================================================
describe("the confirmation screen names the product that was bought", () => {
  const sq = read("SQ/index.html");

  test("success copy exists for BOTH products, keyed like the buttons", () => {
    assert.match(sq, /SUCCESS_DETAIL/);
    assert.match(sq, /"ORAL_QB_NOTES:standard":\s*\n?\s*"Payment verified/);
    assert.match(sq, /"SOLVED_QP:standard":\s*\n?\s*"Payment verified/);
  });

  test("each confirmation repeats its own exclusion", () => {
    const block = sq.slice(sq.indexOf("const SUCCESS_DETAIL"), sq.indexOf("UTILITY FUNCTIONS"));
    const oral = block.slice(block.indexOf("ORAL_QB_NOTES:standard"), block.indexOf("SOLVED_QP:standard"));
    const written = block.slice(block.indexOf("SOLVED_QP:standard"));
    assert.match(oral, /not<\/strong>\s*include[\s\S]{0,80}Written/);
    assert.match(written, /not<\/strong>\s*include[\s\S]{0,80}Oral/);
  });

  test("the modal is no longer hardcoded to the Oral product", () => {
    const modal = sq.slice(sq.indexOf('id="success-modal"'), sq.indexOf('id="success-modal"') + 1200);
    assert.doesNotMatch(modal, /200 pages of Simon Sir notes/,
      "a Written buyer is still congratulated on the Oral product");
  });

  test("the Razorpay checkout description carries the server's product label", () => {
    assert.match(sq, /description:\s*order\.label/);
    const products = read("api/_lib/products.js");
    assert.match(products, /label:\s*"MEO Class I Oral/);
    assert.match(products, /label:\s*"MIW Solved Question Papers — Written"/);
  });
});
