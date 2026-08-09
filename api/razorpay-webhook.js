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

    return res.status(200).json({ received: true });

  } catch (error) {
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
