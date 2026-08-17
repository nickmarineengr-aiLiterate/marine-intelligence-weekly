// =============================================================
// Marine Intelligence Weekly — Refund → entitlement revocation
// File: api/_lib/refund.js
//
// THE DEFECT THIS CLOSES
// ----------------------
// Until this file existed, api/razorpay-webhook.js handled exactly two
// events — payment.captured and payment.failed — and returned a bare
// 200 for everything else. A refund therefore did NOTHING: the money
// went back and the entitlement stayed live, indefinitely. A refunded
// customer kept full paid access, and nothing anywhere recorded that a
// refund had happened. That was true of a refund issued from the
// Razorpay dashboard, which is how the Founder actually issues them.
//
// THE TRUST RULE, UNCHANGED FROM fulfil.js
// ----------------------------------------
// The webhook signature proves the event came from Razorpay. It does
// not tell us WHAT was bought — that lives in the order notes, which
// only create-order.js ever wrote. So this module goes back to Razorpay
// and re-reads the payment and the order, exactly as fulfilment does,
// and takes the product identity from notes rather than from anything
// in the event body.
//
// WHAT IT DELIBERATELY DOES NOT DO
// --------------------------------
//   NO CREDENTIAL DELETION. Login identity and product entitlement are
//     different things. A candidate who is refunded for Oral may still
//     hold a paid Written year, and destroying their account over one
//     refund would take the product they still own with it. The
//     credential is left alone, always. tools/security/entitlement_admin
//     has --remove-credential for the rare case, and even that refuses
//     while any valid entitlement remains.
//
//   NO OTHER PRODUCT TOUCHED. Only the entitlements the REFUNDED
//     product grants are marked. miw:ent:<email> is a hash and this
//     writes named fields, so an Oral refund cannot reach SOLVED_QP.
//
//   NO PARTIAL-REFUND REVOCATION. See the note on isFullRefund below.
//
//   NO SESSION CLEARING. The edge gate re-reads the entitlement on every
//     request, so a refunded customer is denied on their next navigation
//     regardless. Dropping their sessions would sign them out of a
//     product they may still legitimately hold, to buy nothing.
// =============================================================

import { PRODUCTS } from "./products.js";
import { redisCmd } from "./redis.js";
import { entKey, getRawEntitlements } from "./entitlements.js";
import { refundedGrantValue } from "./grants.js";

export class RefundError extends Error {
  constructor(message, code) {
    super(message);
    this.name = "RefundError";
    this.code = code;
  }
}

async function defaultRazorpayGet(path) {
  const auth = `${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`;
  const r = await fetch(`https://api.razorpay.com${path}`, {
    headers: { Authorization: `Basic ${Buffer.from(auth).toString("base64")}` },
  });
  return { status: r.status, data: await r.json() };
}

const defaultStore = {
  readHeld: getRawEntitlements,
  writeFields: async (email, fields) => {
    const args = ["HSET", entKey(email)];
    for (const [k, v] of Object.entries(fields)) args.push(k, v);
    return redisCmd(args);
  },
  recordAudit: async (key, value) => redisCmd(["SET", key, value]),
};

/**
 * Is the payment now refunded IN FULL?
 *
 * WHY PARTIAL REFUNDS REVOKE NOTHING
 * ----------------------------------
 * MIW has no partial-refund policy. Razorpay can produce one from the
 * dashboard in two clicks, so the case has to be HANDLED — but handling
 * it and acting on it are different things. Revoking a whole year of
 * access because ₹100 was returned would be a worse defect than the one
 * this file fixes, and pro-rating a term against a part-refund is a
 * commercial rule nobody has written. So a partial refund is recorded
 * and reported, and access is left exactly as it is, pending a Founder
 * decision.
 *
 * The two figures are read from the re-fetched payment, with the signed
 * event's own refund amount as a floor. At refund.created the payment's
 * amount_refunded is normally already incremented, but a read that
 * raced the update would otherwise see 0 and call a genuine full refund
 * partial — which fails in the direction of leaving access live, i.e.
 * straight back into the defect.
 */
export function isFullRefund(payment, eventRefundAmount) {
  const paid = Number(payment.amount);
  const fromPayment = Number(payment.amount_refunded);
  const fromEvent = Number(eventRefundAmount);
  const refunded = Math.max(
    Number.isFinite(fromPayment) ? fromPayment : 0,
    Number.isFinite(fromEvent) ? fromEvent : 0
  );
  if (!Number.isFinite(paid) || paid <= 0) return false;
  return refunded >= paid;
}

/**
 * Revoke the entitlements a refunded payment had granted.
 *
 * Idempotent by construction rather than by lock: refundedGrantValue()
 * returns null for a field that is already marked refunded, so the
 * second delivery of refund.created — and the refund.processed that
 * follows it days later, and every Razorpay retry of both — all resolve
 * to "no fields to write" and change nothing.
 *
 * @param {object} o
 * @param {string} o.paymentId    payment the refund belongs to
 * @param {string} o.refundId     Razorpay refund id, for the audit record
 * @param {number} [o.refundAmount] amount from the signed event, in paise
 * @param {string} o.source       webhook event name, for the audit record
 * @param {object} [o.deps]       {razorpayGet, store, now}
 */
export async function revokeForRefund({
  paymentId, refundId, refundAmount, source, deps = {},
}) {
  const rpGet = deps.razorpayGet || defaultRazorpayGet;
  const store = deps.store || defaultStore;
  const nowMs = deps.now ? deps.now() : Date.now();

  // ---- 1. Re-read the payment ----
  const payRes = await rpGet(`/v1/payments/${paymentId}`);
  if (payRes.status !== 200 || !payRes.data?.id) {
    throw new RefundError("Payment not retrievable from Razorpay", "payment_unavailable");
  }
  const payment = payRes.data;

  // ---- 2. Full or partial? Partial changes nothing. ----
  if (!isFullRefund(payment, refundAmount)) {
    return {
      status: "partial_refund_no_change",
      paymentId,
      refundId,
      refunded: Number(payment.amount_refunded) || Number(refundAmount) || 0,
      paid: Number(payment.amount) || 0,
    };
  }

  // ---- 3. Product identity from the SERVER-authored order notes ----
  if (!payment.order_id) {
    throw new RefundError("Refunded payment has no order", "no_order");
  }
  const orderRes = await rpGet(`/v1/orders/${payment.order_id}`);
  if (orderRes.status !== 200 || !orderRes.data?.id) {
    throw new RefundError("Order not retrievable from Razorpay", "order_unavailable");
  }
  const notes = orderRes.data.notes || {};
  const productId = String(notes.product || "").trim();
  const product = PRODUCTS[productId];
  if (!product) {
    throw new RefundError(
      `Order ${payment.order_id} has no recognised product in notes`, "unknown_product"
    );
  }

  const buyerEmail = String(notes.buyer_email || payment.email || "").toLowerCase().trim();
  if (!buyerEmail) throw new RefundError("No buyer email on order", "no_email");

  // ---- 4. Mark ONLY this product's entitlements ----
  const held = await store.readHeld(buyerEmail);
  const fields = {};
  const skipped = [];
  for (const e of product.grants) {
    const value = refundedGrantValue(held[e], nowMs);
    if (value) fields[e] = value;
    else skipped.push(e);
  }

  if (Object.keys(fields).length === 0) {
    return {
      status: "no_change", productId, buyerEmail, refundId,
      reason: skipped.length ? "already refunded, or no grant to revoke" : "product grants nothing",
    };
  }

  await store.writeFields(buyerEmail, fields);

  // ---- 5. Audit. Enough to answer "what ended, and why". ----
  //
  // Keyed by refund id so a replayed webhook overwrites its own record
  // rather than accumulating duplicates. Deliberately holds no card,
  // no bank detail and no name — the product, the identifiers and the
  // outcome are the whole question this record exists to answer.
  await store.recordAudit(
    `miw:refund:${refundId || paymentId}`,
    JSON.stringify({
      email: buyerEmail,
      product: productId,
      entitlements: Object.keys(fields),
      orderId: payment.order_id,
      paymentId,
      refundId: refundId || null,
      amountRefunded: Number(payment.amount_refunded) || Number(refundAmount) || null,
      amountPaid: Number(payment.amount) || null,
      full: true,
      source: source || null,
      at: Math.floor(nowMs / 1000),
    })
  );

  return {
    status: "revoked",
    productId,
    buyerEmail,
    refundId,
    entitlements: Object.keys(fields),
    unchanged: skipped,
  };
}
