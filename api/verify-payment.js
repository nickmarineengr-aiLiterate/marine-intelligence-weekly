// =============================================================
// Marine Intelligence Weekly — Razorpay Verify Payment v4
// Writes email→password to Upstash Redis on payment
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

async function redisGet(key) {
  const UPSTASH_URL = process.env.KV_REST_API_URL;
  const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;
  const response = await fetch(`${UPSTASH_URL}/get/${encodeURIComponent(key)}`, {
    headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
  });
  const data = await response.json();
  return data.result;
}

async function redisSet(key, value) {
  const UPSTASH_URL = process.env.KV_REST_API_URL;
  const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;
  const response = await fetch(`${UPSTASH_URL}/set/${encodeURIComponent(key)}/${encodeURIComponent(value)}`, {
    headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
  });
  return response.json();
}

async function assignPassword(buyerEmail) {
  const email = buyerEmail.toLowerCase().trim();

  // Check if already has password
  const existing = await redisGet(`miw:user:${email}`);
  if (existing) return existing;

  // Get pool and find next available
  const pool = JSON.parse(process.env.QB_PASSWORD_POOL || "[]");

  // Find used passwords by checking pool sequentially
  for (const pwd of pool) {
    const check = await redisGet(`miw:pwd:${pwd}`);
    if (!check) {
      // Mark password as used
      await redisSet(`miw:pwd:${pwd}`, email);
      // Store user→password mapping
      await redisSet(`miw:user:${email}`, pwd);
      return pwd;
    }
  }
  throw new Error("Password pool exhausted");
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
    <p style="color:#334155;line-height:1.6;margin:0 0 16px">
      Thank you for your purchase (${tierLabel} — ${price}). Your QB access is ready. ⚓
    </p>

    ${founderNote}

    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:12px;color:#64748b;margin:0 0 12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em">Your Login Credentials</p>
      <table style="width:100%;font-size:14px;border-collapse:collapse">
        <tr>
          <td style="color:#64748b;padding:5px 0;width:90px;vertical-align:top">Login page</td>
          <td><a href="${QB_LOGIN_URL}" style="color:#0d9488">${QB_LOGIN_URL}</a></td>
        </tr>
        <tr>
          <td style="color:#64748b;padding:5px 0">Email</td>
          <td style="color:#0f172a;font-weight:500">${buyerEmail}</td>
        </tr>
        <tr>
          <td style="color:#64748b;padding:5px 0">Password</td>
          <td style="color:#0f172a;font-weight:700;font-family:monospace;font-size:16px;letter-spacing:1px">${password}</td>
        </tr>
      </table>
    </div>

    <div style="text-align:center;margin:1.5rem 0">
      <a href="${QB_LOGIN_URL}" style="background:#0d9488;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:600;font-size:15px;display:inline-block">
        Access Question Bank →
      </a>
    </div>

    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:14px;font-weight:600;color:#14532d;margin:0 0 8px">📱 Join the MEO Class 1 WhatsApp Group</p>
      <p style="font-size:13px;color:#166534;margin:0 0 12px;line-height:1.6">
        Get real oral exam questions, weekly updates, and peer support from fellow candidates.
      </p>
      <p style="font-size:13px;color:#166534;margin:0;line-height:1.8">
        <strong>① Reply to this email</strong> with your name and WhatsApp number<br>
        <strong>② WhatsApp Nixon directly:</strong>
        <a href="https://wa.me/919526595999" style="color:#0d9488;font-weight:600">+91 95265 95999</a>
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
    <p style="font-size:11px;color:#94a3b8;margin:0">
      © 2026 Marine Intelligence Weekly &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/terms.html" style="color:#64748b;text-decoration:none">Terms</a> &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/privacy.html" style="color:#64748b;text-decoration:none">Privacy</a>
    </p>
  </div>
</div>
</body></html>`
  };
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  try {
    const KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;
    if (!KEY_SECRET) return res.status(500).json({ error: "Config error" });

    const { razorpay_order_id, razorpay_payment_id, razorpay_signature,
            buyer_email, buyer_name, tier } = req.body;

    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature)
      return res.status(400).json({ error: "Missing payment details" });
    if (!buyer_email || !tier)
      return res.status(400).json({ error: "Missing buyer details" });

    const expected = crypto.createHmac("sha256", KEY_SECRET)
      .update(`${razorpay_order_id}|${razorpay_payment_id}`)
      .digest("hex");

    if (expected !== razorpay_signature)
      return res.status(400).json({ error: "Payment verification failed" });

    // Assign password — now persisted in Redis
    const password = await assignPassword(buyer_email);
    const validTier = ["founders","standard"].includes(tier) ? tier : "standard";

    await transporter.sendMail(buildEmail(validTier, buyer_name, buyer_email, password));

    console.log(`✓ QB access sent: ${buyer_email} | pwd: ${password} | tier: ${validTier} | order: ${razorpay_order_id}`);

    return res.status(200).json({ success: true, tier: validTier, order_id: razorpay_order_id });

  } catch (error) {
    console.error("verify-payment error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
