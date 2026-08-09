// =============================================================
// Marine Intelligence Weekly — Razorpay Verify Payment (V2)
// File: api/verify-payment.js
//
// This endpoint is now THIN. It proves the callback is authentic
// (HMAC over order_id|payment_id) and then hands off to
// api/_lib/fulfil.js, which independently re-reads the order and
// payment from Razorpay and decides what — if anything — was bought.
//
// What it deliberately no longer does:
//   * trust `tier` from the request body (it used to; that is how a
//     ₹1 payment could claim the ₹1,499 product);
//   * decide the product or the price at all;
//   * carry its own copy of the password/email logic.
// =============================================================

import crypto from "crypto";
import { fulfilPayment, FulfilError, maskEmail } from "./_lib/fulfil.js";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  try {
    const KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;
    if (!KEY_SECRET) return res.status(500).json({ error: "Config error" });

    const {
      razorpay_order_id, razorpay_payment_id, razorpay_signature,
    } = req.body || {};

    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
      return res.status(400).json({ error: "Missing payment details" });
    }

    // ---- Authenticity: this payment really belongs to this order ----
    // NOTE: a valid signature proves association, NOT price and NOT
    // product. Those are established in fulfilPayment().
    const expected = crypto.createHmac("sha256", KEY_SECRET)
      .update(`${razorpay_order_id}|${razorpay_payment_id}`)
      .digest("hex");

    const a = Buffer.from(expected);
    const b = Buffer.from(String(razorpay_signature));
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
      console.error("[verify-payment] signature mismatch — rejecting");
      return res.status(400).json({ error: "Payment verification failed" });
    }

    const result = await fulfilPayment({
      orderId: razorpay_order_id,
      paymentId: razorpay_payment_id,
      source: "verify-payment",
    });

    if (result.status === "already_processed") {
      return res.status(200).json({ success: true, skipped: "already processed" });
    }

    return res.status(200).json({
      success: true,
      product: result.productId,
      order_id: razorpay_order_id,
    });

  } catch (error) {
    if (error instanceof FulfilError) {
      // These are refusals, not crashes: the payment was authentic but
      // did not match an approved product/amount. Log loudly, tell the
      // buyer nothing exploitable.
      console.error(`[verify-payment] REFUSED (${error.code}): ${error.message}`);
      return res.status(400).json({ error: "Payment could not be validated" });
    }
    console.error("[verify-payment] error:", error.message);
    return res.status(500).json({ error: "Internal server error" });
  }
}
