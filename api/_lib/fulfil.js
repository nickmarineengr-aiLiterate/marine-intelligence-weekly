// =============================================================
// Marine Intelligence Weekly — Payment fulfilment (Security V2)
// File: api/_lib/fulfil.js
//
// THE TRUST RULE
// --------------
// Nothing about WHAT was bought comes from the browser. The old
// verify-payment.js took `tier` straight off the request body and
// never looked at the amount at all, so a genuine ₹1 payment with
// `tier:"founders"` in the JSON produced full access — the Razorpay
// signature was valid, because the signature only proves that THIS
// payment belongs to THAT order. It says nothing about price.
//
// Here, after the signature is checked by the caller, we go back to
// Razorpay and read the order and payment ourselves:
//   * product + tier come from order.notes (server-authored at
//     create-order time — the browser cannot set them);
//   * the expected amount is looked up in the catalogue from that
//     product/tier and compared to what Razorpay actually recorded;
//   * currency must be INR and the payment must be captured.
// Any mismatch fails closed and grants nothing.
//
// Every external effect (Razorpay reads, Redis, SMTP) is reachable
// through the `deps` bag so tools/security/ can exercise the real
// decision logic offline with no network and no secrets.
// =============================================================

import { PRODUCTS } from "./products.js";
import { redisGet, redisSet, redisIncr, redisSetNX, redisDel } from "./redis.js";
import { grantEntitlements, userKey } from "./entitlements.js";
import { hashPassword } from "./session.js";
import { makeTransport, buildAccessEmail } from "./email.js";

async function defaultRazorpayGet(path) {
  const auth = `${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`;
  const r = await fetch(`https://api.razorpay.com${path}`, {
    headers: { Authorization: `Basic ${Buffer.from(auth).toString("base64")}` },
  });
  return { status: r.status, data: await r.json() };
}

const defaultStore = {
  get: redisGet,
  set: redisSet,
  incr: redisIncr,
  setNX: redisSetNX,
  del: redisDel,
  grant: grantEntitlements,
};

async function defaultSendMail(message) {
  const transport = await makeTransport();
  return transport.sendMail(message);
}

export class FulfilError extends Error {
  constructor(message, code) {
    super(message);
    this.name = "FulfilError";
    this.code = code;
  }
}

/**
 * Independently verify an order+payment against the catalogue and,
 * if sound, grant entitlements and send the access email exactly once.
 *
 * @param {object} o
 * @param {string} o.orderId
 * @param {string} o.paymentId
 * @param {string} o.source   "verify-payment" | "webhook" (lock value)
 * @param {object} [o.deps]   {razorpayGet, store, sendMail, passwordPool}
 */
export async function fulfilPayment({ orderId, paymentId, source, deps = {} }) {
  const rpGet = deps.razorpayGet || defaultRazorpayGet;
  const store = deps.store || defaultStore;
  const sendMail = deps.sendMail || defaultSendMail;

  // ---- 1. Read the order back from Razorpay ----
  const orderRes = await rpGet(`/v1/orders/${orderId}`);
  if (orderRes.status !== 200 || !orderRes.data?.id) {
    throw new FulfilError("Order not retrievable from Razorpay", "order_unavailable");
  }
  const order = orderRes.data;
  const notes = order.notes || {};

  // ---- 2. Product identity from SERVER-authored order notes ----
  const productId = String(notes.product || "").trim();
  const tier = String(notes.tier || "").trim();
  const product = PRODUCTS[productId];
  if (!product) {
    throw new FulfilError(
      `Order ${orderId} has no recognised product in notes`, "unknown_product"
    );
  }
  const tierDef = product.tiers[tier];
  if (!tierDef) {
    throw new FulfilError(
      `Order ${orderId} has no recognised tier '${tier}' for ${productId}`, "unknown_tier"
    );
  }

  // ---- 3. Amount and currency must match the catalogue exactly ----
  if (Number(order.amount) !== Number(tierDef.amount)) {
    throw new FulfilError(
      `Amount mismatch for ${productId}/${tier}: order=${order.amount} expected=${tierDef.amount}`,
      "amount_mismatch"
    );
  }
  if (String(order.currency).toUpperCase() !== product.currency) {
    throw new FulfilError(`Currency mismatch: ${order.currency}`, "currency_mismatch");
  }

  // ---- 4. The payment itself must be real, captured, same order ----
  const payRes = await rpGet(`/v1/payments/${paymentId}`);
  if (payRes.status !== 200 || !payRes.data?.id) {
    throw new FulfilError("Payment not retrievable from Razorpay", "payment_unavailable");
  }
  const payment = payRes.data;
  if (payment.order_id !== order.id) {
    throw new FulfilError("Payment does not belong to this order", "order_payment_mismatch");
  }
  if (payment.status !== "captured") {
    throw new FulfilError(`Payment not captured (status=${payment.status})`, "not_captured");
  }
  if (Number(payment.amount) !== Number(tierDef.amount)) {
    throw new FulfilError(
      `Payment amount mismatch: paid=${payment.amount} expected=${tierDef.amount}`,
      "amount_mismatch"
    );
  }

  const buyerEmail = String(notes.buyer_email || payment.email || "").toLowerCase().trim();
  if (!buyerEmail) throw new FulfilError("No buyer email on order", "no_email");
  const buyerName = String(notes.buyer_name || "").trim();

  // ---- 5. Idempotency. Exactly one caller proceeds per payment. ----
  const claimed = await store.setNX(`miw:send_lock:${paymentId}`, source);
  if (!claimed) {
    return { status: "already_processed", productId, buyerEmail };
  }

  // Steps 6–8 run under the claimed lock. If any of them throws we
  // RELEASE the lock before rethrowing. The previous code left it
  // claimed, so a Razorpay retry after (say) pool exhaustion silently
  // no-opped and the buyer never got access until someone cleared the
  // key by hand — the old comment even documented that trap.
  let password = null;          // null => existing account, no new credential
  let isUpgrade = false;
  try {
    // ---- 6. Credential: reuse the account's existing one if present ----
    const existing = await store.get(userKey(buyerEmail));
    isUpgrade = Boolean(existing);
    if (!existing) {
      password = await assignNewPassword(buyerEmail, store, deps.passwordPool);
    }

    // ---- 7. Grant. Additive — never removes an existing entitlement. ----
    await store.grant(buyerEmail, product.grants);

    // ---- 8. Email ----
    await sendMail(buildAccessEmail({
      productId,
      buyerEmail,
      buyerName,
      password,
      priceDisplay: tierDef.display,
      isUpgrade,
    }));
  } catch (e) {
    await Promise.resolve(store.del(`miw:send_lock:${paymentId}`)).catch(() => {});
    throw e;
  }

  console.log(
    `✓ Fulfilled ${productId}/${tier} for ${maskEmail(buyerEmail)} ` +
    `via ${source} | order ${orderId} | upgrade=${isUpgrade}`
  );

  return { status: "granted", productId, tier, buyerEmail, isUpgrade };
}

/**
 * New accounts draw from QB_PASSWORD_POOL exactly as before, so the
 * Founder's existing credential workflow is unchanged — but the value
 * is now STORED hashed. The plaintext exists only long enough to be
 * emailed to the buyer.
 */
async function assignNewPassword(email, store, poolOverride) {
  const pool = poolOverride || JSON.parse(process.env.QB_PASSWORD_POOL || "[]");
  if (pool.length === 0) throw new FulfilError("QB_PASSWORD_POOL is empty", "no_pool");

  const counterKey = "miw:password_counter";
  const current = await store.get(counterKey);
  if (current === null || current === undefined) await store.set(counterKey, "28");

  const nextIndex = await store.incr(counterKey);
  const pwdIndex = nextIndex - 1;
  if (pwdIndex >= pool.length) {
    throw new FulfilError(`Password pool exhausted (index ${pwdIndex})`, "pool_exhausted");
  }

  const password = pool[pwdIndex];
  await store.set(userKey(email), hashPassword(password));
  await store.set(`miw:pwd_assigned:${pwdIndex}`, email);
  return password;
}

export function maskEmail(email) {
  const [u, d] = String(email).split("@");
  if (!d) return "***";
  return `${u.slice(0, 2)}***@${d}`;
}
