// =============================================================
// Marine Intelligence Weekly — Razorpay Webhook (V2)
// File: api/razorpay-webhook.js
//
// Fires independently of the buyer's browser surviving the redirect.
// Like verify-payment.js it is now thin: prove the webhook is really
// from Razorpay, then hand the order/payment ids to fulfilPayment(),
// which re-reads both from Razorpay and applies the catalogue rules.
//
// The password/email logic that used to be duplicated here verbatim
// (with a "if you edit one, edit both" comment) now lives in one
// place, so the Written product cannot be fulfilled by one path and
// not the other.
// =============================================================

import crypto from "crypto";
import { fulfilPayment, FulfilError } from "./_lib/fulfil.js";
import { revokeForRefund, RefundError } from "./_lib/refund.js";

// Refund events that END paid access.
//
// BOTH, not just refund.processed. `created` is the moment the merchant
// decided to give the money back; `processed` can be days later once the
// bank settles. Waiting for settlement would leave a customer the Founder
// has already refunded holding full access for most of a week. Acting on
// `created` and again on `processed` is safe because the revocation is
// idempotent — the second event finds the grant already marked and writes
// nothing.
//
// refund.failed is NOT here. A failed refund means the money did not go
// back, so access arguably should return — but "arguably" is not a policy,
// and auto-restoring paid access from a payment-provider event is a far
// more dangerous default than leaving it revoked for a human to reopen.
// It is logged loudly instead. FOUNDER DECISION.
const REFUND_REVOKING_EVENTS = new Set(["refund.created", "refund.processed"]);

// Vercel parses JSON bodies by default, which would alter the exact
// bytes and break HMAC verification. Read the RAW body first.
export const config = {
  api: { bodyParser: false },
};

function readRawBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  let rawBody;
  try {
    rawBody = await readRawBody(req);
  } catch (err) {
    console.error("[webhook] Failed to read raw body:", err.message);
    return res.status(400).json({ error: "Bad request" });
  }

  // RAZORPAY_WEBHOOK_SECRET is DIFFERENT from RAZORPAY_KEY_SECRET.
  const WEBHOOK_SECRET = process.env.RAZORPAY_WEBHOOK_SECRET;
  if (!WEBHOOK_SECRET) {
    console.error("[webhook] RAZORPAY_WEBHOOK_SECRET not configured");
    return res.status(500).json({ error: "Config error" });
  }

  const received = String(req.headers["x-razorpay-signature"] || "");
  const expected = crypto.createHmac("sha256", WEBHOOK_SECRET).update(rawBody).digest("hex");
  const a = Buffer.from(expected);
  const b = Buffer.from(received);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    console.error("[webhook] Signature mismatch — rejecting");
    return res.status(400).json({ error: "Invalid signature" });
  }

  let payload;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return res.status(400).json({ error: "Invalid JSON" });
  }

  const event = payload.event;
  console.log(`[webhook] Received event: ${event}`);

  try {
    if (event === "payment.captured") {
      const entity = payload.payload.payment.entity;
      const result = await fulfilPayment({
        orderId: entity.order_id,
        paymentId: entity.id,
        source: "webhook",
      });
      if (result.status === "already_processed") {
        return res.status(200).json({ received: true, skipped: "already claimed" });
      }
    }

    if (event === "payment.failed") {
      const entity = payload.payload.payment.entity;
      console.log(
        `[webhook] payment.failed: ${entity.id} | reason: ${entity.error_description || "unknown"}`
      );
    }

    if (REFUND_REVOKING_EVENTS.has(event)) {
      const refund = payload.payload?.refund?.entity || {};
      const paymentId = refund.payment_id;
      if (!paymentId) {
        console.error(`[webhook] ${event} carried no payment_id — nothing to revoke`);
        return res.status(200).json({ received: true, refused: "no_payment_id" });
      }
      const result = await revokeForRefund({
        paymentId,
        refundId: refund.id,
        refundAmount: refund.amount,
        source: event,
      });
      console.log(
        `[webhook] ${event} → ${result.status}` +
        (result.productId ? ` | ${result.productId}` : "") +
        (result.entitlements ? ` | revoked ${result.entitlements.join("+")}` : "")
      );
      if (result.status === "partial_refund_no_change") {
        // Loud on purpose. Access is intact and a human has to decide
        // whether it should be — see isFullRefund() in _lib/refund.js.
        console.warn(
          `[webhook] PARTIAL REFUND on payment ${paymentId} ` +
          `(${result.refunded} of ${result.paid} paise). Access UNCHANGED — ` +
          "no partial-refund policy exists. FOUNDER DECISION."
        );
      }
      return res.status(200).json({ received: true, refund: result.status });
    }

    if (event === "refund.failed") {
      const refund = payload.payload?.refund?.entity || {};
      console.warn(
        `[webhook] refund.failed for payment ${refund.payment_id || "unknown"} — ` +
        "any revocation already applied STANDS. Reopen by hand if the money " +
        "genuinely stayed with MIW. FOUNDER DECISION."
      );
    }

    return res.status(200).json({ received: true });

  } catch (error) {
    if (error instanceof RefundError) {
      // Same reasoning as FulfilError: a refund we cannot resolve to a
      // product is a permanent refusal, not a transient fault. 200 stops
      // the retry storm; the log is what gets acted on. This leaves paid
      // access LIVE after a refund, so it must be impossible to miss.
      console.error(
        `[webhook] REFUND NOT APPLIED (${error.code}): ${error.message} — ` +
        "PAID ACCESS MAY STILL BE ACTIVE. Check entitlement_admin show."
      );
      return res.status(200).json({ received: true, refused: error.code });
    }
    if (error instanceof FulfilError) {
      // A payment that does not match an approved product/amount is a
      // permanent refusal, not a transient fault — return 200 so
      // Razorpay stops retrying, and surface it loudly in the logs.
      console.error(`[webhook] REFUSED (${error.code}): ${error.message}`);
      return res.status(200).json({ received: true, refused: error.code });
    }
    console.error("[webhook] Error processing event:", error.message);
    // 500 => Razorpay retries. fulfilPayment releases its lock on
    // failure, so a retry can genuinely re-attempt fulfilment.
    return res.status(500).json({ error: "Internal error" });
  }
}
