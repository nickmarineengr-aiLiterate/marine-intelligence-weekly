// =============================================================
// Marine Intelligence Weekly — Razorpay Verify Payment v2
// Assigns unique password per email, sends login credentials
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

function assignPassword(buyerEmail) {
  const email = buyerEmail.toLowerCase();
  const pool = JSON.parse(process.env.QB_PASSWORD_POOL || "[]");
  const used = JSON.parse(process.env.QB_USED_PASSWORDS || "{}");

  // Already has a password
  if (used[email]) return used[email];

  // Assign next available
  const usedValues = new Set(Object.values(used));
  const available = pool.find(p => !usedValues.has(p));
  if (!available) throw new Error("Password pool exhausted");

  return available;
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

    <!-- Credentials Box -->
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:12px;color:#64748b;margin:0 0 12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em">Your Login Credentials</p>
      <table style="width:100%;font-size:14px">
        <tr>
          <td style="color:#64748b;padding:4px 0;width:80px">Login page</td>
          <td><a href="${QB_LOGIN_URL}" style="color:#0d9488">${QB_LOGIN_URL}</a></td>
        </tr>
        <tr>
          <td style="color:#64748b;padding:4px 0">Email</td>
          <td style="color:#0f172a;font-weight:500">${buyerEmail}</td>
        </tr>
        <tr>
          <td style="color:#64748b;padding:4px 0">Password</td>
          <td style="color:#0f172a;font-weight:700;font-family:monospace;font-size:16px;letter-spacing:1px">${password}</td>
        </tr>
      </table>
    </div>

    <!-- CTA -->
    <div style="text-align:center;margin:1.5rem 0">
      <a href="${QB_LOGIN_URL}" style="background:#0d9488;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:600;font-size:15px;display:inline-block">
        Access Question Bank →
      </a>
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

    // Verify Razorpay signature
    const expected = crypto.createHmac("sha256", KEY_SECRET)
      .update(`${razorpay_order_id}|${razorpay_payment_id}`)
      .digest("hex");

    if (expected !== razorpay_signature)
      return res.status(400).json({ error: "Payment verification failed" });

    // Assign password
    const password = assignPassword(buyer_email);
    const validTier = ["founders","standard"].includes(tier) ? tier : "standard";

    // Send email
    await transporter.sendMail(buildEmail(validTier, buyer_name, buyer_email, password));

    console.log(`✓ QB access sent: ${buyer_email} | pwd: ${password} | tier: ${validTier} | order: ${razorpay_order_id}`);

    return res.status(200).json({ success: true, tier: validTier, order_id: razorpay_order_id });

  } catch (error) {
    console.error("verify-payment error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
