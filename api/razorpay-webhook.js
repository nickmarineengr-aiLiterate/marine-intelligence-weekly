// =============================================================
// Marine Intelligence Weekly — Razorpay Webhook Handler v2
// Fixed: atomic NX lock shared with verify-payment.js to kill
// the check-then-act race that caused double credential emails.
// Fires independently of the buyer's browser tab surviving.
// =============================================================

import crypto from "crypto";
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: "smtp-relay.brevo.com",
  port: 587,
  secure: false,
  auth: {
    user: process.env.BREVO_SMTP_LOGIN,
    pass: process.env.BREVO_SMTP_KEY,
  },
});

const QB_LOGIN_URL = "https://marineintelligenceweekly.com/SQ/pay.html";

// -------------------------------------------------------------
// Redis helpers (same pattern as verify-payment.js)
// -------------------------------------------------------------
async function redisGet(key) {
  const url = `${process.env.KV_REST_API_URL}/get/${encodeURIComponent(key)}`;
  const r = await fetch(url, {
    headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` }
  });
  const data = await r.json();
  return data.result || null;
}

async function redisSet(key, value) {
  const url = `${process.env.KV_REST_API_URL}/set/${encodeURIComponent(key)}/${encodeURIComponent(value)}`;
  const r = await fetch(url, {
    headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` }
  });
  return r.json();
}

async function redisIncr(key) {
  const url = `${process.env.KV_REST_API_URL}/incr/${encodeURIComponent(key)}`;
  const r = await fetch(url, {
    headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` }
  });
  const data = await r.json();
  return data.result;
}

// -------------------------------------------------------------
// Atomic claim — SET key val NX EX <ttl>. Only the first caller
// (webhook OR client verify-payment.js, whichever hits Redis
// first) gets true. This REPLACES the old alreadyProcessed()/
// markProcessed() read-then-write pair, which had a race window.
// -------------------------------------------------------------
async function redisSetNX(key, value, ttlSeconds = 86400) {
  // Same unambiguous raw-command POST form as verify-payment.js — see
  // comment there. Must stay identical in both files so the lock they
  // race against behaves the same way regardless of which path wins.
  const r = await fetch(process.env.KV_REST_API_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(["SET", key, value, "NX", "EX", ttlSeconds]),
  });
  const data = await r.json();
  return data.result === "OK";
}

// -------------------------------------------------------------
// Password assignment — identical logic to verify-payment.js
// (kept in sync intentionally; if you edit one, edit both)
// -------------------------------------------------------------
async function assignPassword(buyerEmail) {
  const email = buyerEmail.toLowerCase().trim();

  const existing = await redisGet(`miw:user:${email}`);
  if (existing) {
    console.log(`[webhook] Existing password found for ${email}`);
    return existing;
  }

  const pool = JSON.parse(process.env.QB_PASSWORD_POOL || "[]");
  if (pool.length === 0) throw new Error("QB_PASSWORD_POOL is empty");

  const counterKey = "miw:password_counter";
  let current = await redisGet(counterKey);
  if (current === null) {
    await redisSet(counterKey, "28");
    current = 28;
  }

  const nextIndex = await redisIncr(counterKey);
  const pwdIndex = nextIndex - 1;

  if (pwdIndex >= pool.length) {
    throw new Error(`Password pool exhausted (index ${pwdIndex}, pool size ${pool.length})`);
  }

  const password = pool[pwdIndex];
  console.log(`[webhook] Assigning pool[${pwdIndex}] = ${password} to ${email}`);

  await redisSet(`miw:user:${email}`, password);
  await redisSet(`miw:pwd:${password}`, email);

  return password;
}

function buildEmail(tier, buyerName, buyerEmail, password) {
  const isFounders = tier === "founders";
  const tierLabel = isFounders ? "Founders Access" : "Standard Access";
  const price = isFounders ? "₹499" : "₹899";

  const founderNote = isFounders
    ? `<p style="background:#f0fdfa;border-left:3px solid #0d9488;padding:10px 14px;margin:16px 0;font-size:14px;color:#134e4a;">
        <strong>Founders Group — one of only 20 seats.</strong> Your slot is held until you pass your MMD oral examination.
      </p>` : "";

  return {
    from: `"Marine Intelligence Weekly" <contactus@marineintelligenceweekly.com>`,
    to: buyerEmail,
    subject: `🚢 Your MEO Class 1 QB Access — ${tierLabel}`,
    html: `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',system-ui,sans-serif">
<div style="max-width:560px;margin:2rem auto;background:#fff;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden">
  <div style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:1.5rem">
    <p style="color:#0d9488;font-weight:700;font-size:1.1rem;margin:0">Marine Intelligence Weekly</p>
    <p style="color:#94a3b8;font-size:13px;margin:4px 0 0">MEO Class 1 Question Bank — ${tierLabel}</p>
  </div>
  <div style="padding:2rem">
    <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${buyerName || "there"},</p>
    <p style="color:#334155;line-height:1.6;margin:0 0 16px">Thank you for your purchase (${tierLabel} — ${price}). Your QB access is ready. ⚓</p>
    ${founderNote}
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:12px;color:#64748b;margin:0 0 12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em">Your Login Credentials</p>
      <table style="width:100%;font-size:14px;border-collapse:collapse">
        <tr><td style="color:#64748b;padding:5px 0;width:90px;vertical-align:top">Login page</td>
            <td><a href="${QB_LOGIN_URL}" style="color:#0d9488">${QB_LOGIN_URL}</a></td></tr>
        <tr><td style="color:#64748b;padding:5px 0">Email</td>
            <td style="color:#0f172a;font-weight:500">${buyerEmail}</td></tr>
        <tr><td style="color:#64748b;padding:5px 0">Password</td>
            <td style="color:#0f172a;font-weight:700;font-family:monospace;font-size:16px;letter-spacing:1px">${password}</td></tr>
      </table>
    </div>
    <div style="text-align:center;margin:1.5rem 0">
      <a href="${QB_LOGIN_URL}" style="background:#0d9488;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:600;font-size:15px;display:inline-block">Access Question Bank →</a>
    </div>
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:14px;font-weight:600;color:#14532d;margin:0 0 8px">📱 Join the MEO Class 1 WhatsApp Group</p>
      <p style="font-size:13px;color:#166534;margin:0 0 12px;line-height:1.6">Get real oral exam questions, weekly updates, and peer support from fellow candidates.</p>
      <p style="font-size:13px;color:#166534;margin:0;line-height:1.8">
        <strong>① Reply to this email</strong> with your name and WhatsApp number<br>
        <strong>② WhatsApp Nixon directly:</strong> <a href="https://wa.me/919526595999" style="color:#0d9488;font-weight:600">+91 95265 95999</a>
      </p>
    </div>
    <div style="border-top:1px solid #e2e8f0;padding-top:1rem;margin-top:1rem">
      <p style="font-size:13px;color:#334155;margin:0 0 8px;font-weight:600">✓ Important</p>
      <ul style="font-size:13px;color:#334155;padding-left:18px;margin:0;line-height:1.9">
        <li>Save this email — it contains your login credentials</li>
        <li>Password works for 30 days per device</li>
        <li>Access is personal — do not share your password</li>
        <li>All future QB updates are free for life</li>
        <li>Help: <a href="mailto:contactus@marineintelligenceweekly.com" style="color:#0d9488">contactus@marineintelligenceweekly.com</a></li>
      </ul>
    </div>
    <p style="font-size:14px;color:#334155;margin:1.5rem 0 2px">All the best for your orals.</p>
    <p style="font-size:14px;color:#0f172a;font-weight:600;margin:0">Nixon Antony</p>
    <p style="font-size:12px;color:#64748b;margin:2px 0 0">Second Engineer, Maersk A/S | Marine Intelligence Weekly</p>
  </div>
  <div style="background:#f1f5f9;padding:1rem;text-align:center;border-top:1px solid #e2e8f0">
    <p style="font-size:11px;color:#94a3b8;margin:0">© 2026 Marine Intelligence Weekly &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/terms.html" style="color:#64748b;text-decoration:none">Terms</a> &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/privacy.html" style="color:#64748b;text-decoration:none">Privacy</a>
    </p>
  </div>
</div>
</body></html>`
  };
}

// -------------------------------------------------------------
// IMPORTANT: Vercel parses JSON bodies by default, which would
// alter whitespace/formatting and break HMAC verification below.
// We must read the RAW body bytes before any parsing happens.
// -------------------------------------------------------------
export const config = {
  api: {
    bodyParser: false,
  },
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

  // -----------------------------------------------------------
  // Verify webhook signature using RAZORPAY_WEBHOOK_SECRET
  // (this is DIFFERENT from RAZORPAY_KEY_SECRET used in verify-payment.js)
  // -----------------------------------------------------------
  const WEBHOOK_SECRET = process.env.RAZORPAY_WEBHOOK_SECRET;
  if (!WEBHOOK_SECRET) {
    console.error("[webhook] RAZORPAY_WEBHOOK_SECRET not configured");
    return res.status(500).json({ error: "Config error" });
  }

  const receivedSignature = req.headers["x-razorpay-signature"];
  const expectedSignature = crypto
    .createHmac("sha256", WEBHOOK_SECRET)
    .update(rawBody)
    .digest("hex");

  if (receivedSignature !== expectedSignature) {
    console.error("[webhook] Signature mismatch — rejecting");
    return res.status(400).json({ error: "Invalid signature" });
  }

  // Signature valid — now safe to parse
  let payload;
  try {
    payload = JSON.parse(rawBody);
  } catch (err) {
    return res.status(400).json({ error: "Invalid JSON" });
  }

  const event = payload.event;
  console.log(`[webhook] Received event: ${event}`);

  try {
    if (event === "payment.captured") {
      const paymentEntity = payload.payload.payment.entity;
      const paymentId = paymentEntity.id;
      const orderId = paymentEntity.order_id;

      // notes.buyer_email / notes.tier were set in create-order.js
      const notes = paymentEntity.notes || {};
      const buyerEmail = notes.buyer_email || paymentEntity.email;
      const tierRaw = notes.tier;
      const validTier = ["founders", "standard"].includes(tierRaw) ? tierRaw : "standard";

      if (!buyerEmail) {
        console.error(`[webhook] No buyer_email found in notes for payment ${paymentId}`);
        return res.status(200).json({ received: true, warning: "no buyer_email" });
      }

      // -------------------------------------------------------
      // Atomic claim — SAME lock key format as verify-payment.js
      // (miw:send_lock:<paymentId>). Whichever path — this webhook
      // or the buyer's browser calling verify-payment.js — hits
      // Redis first wins the NX race; the other gets false and
      // returns immediately without touching password/email logic.
      // This replaces the old alreadyProcessed()/markProcessed()
      // read-then-write pair that allowed both paths through.
      // -------------------------------------------------------
      const lockKey = `miw:send_lock:${paymentId}`;
      const claimed = await redisSetNX(lockKey, "webhook");

      if (!claimed) {
        console.log(`[webhook] Payment ${paymentId} already claimed elsewhere — skipping`);
        return res.status(200).json({ received: true, skipped: "already claimed" });
      }

      const password = await assignPassword(buyerEmail);
      await transporter.sendMail(buildEmail(validTier, notes.buyer_name, buyerEmail, password));

      console.log(`✓ [webhook] QB access sent: ${buyerEmail} | pwd: ${password} | tier: ${validTier} | order: ${orderId} | payment: ${paymentId}`);
    }

    if (event === "payment.failed") {
      const paymentEntity = payload.payload.payment.entity;
      console.log(`[webhook] payment.failed logged: ${paymentEntity.id} | reason: ${paymentEntity.error_description || "unknown"}`);
      // No action needed — just visibility in Vercel logs.
    }

    return res.status(200).json({ received: true });

  } catch (error) {
    console.error("[webhook] Error processing event:", error.message);
    // Return 500 so Razorpay retries transient errors. Because the
    // NX lock above is already claimed by this attempt's key by the
    // time we might fail later in assignPassword/sendMail, a retry
    // could still be blocked — if password pool exhaustion is the
    // cause, fix the pool and manually clear miw:send_lock:<id> in
    // Redis before asking Razorpay to redeliver.
    return res.status(500).json({ error: "Internal error", detail: error.message });
  }
}
