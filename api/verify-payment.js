// =============================================================
// Marine Intelligence Weekly — Razorpay Verify Payment
// File: api/verify-payment.js
// Endpoint: POST /api/verify-payment
// Purpose: Verify payment signature, send QB access email via Brevo
// =============================================================

import crypto from "crypto";
import nodemailer from "nodemailer";

// Brevo SMTP transporter
const transporter = nodemailer.createTransport({
  host: "smtp-relay.brevo.com",
  port: 587,
  secure: false,
  auth: {
    user: process.env.BREVO_SMTP_LOGIN,
    pass: process.env.BREVO_SMTP_KEY,
  },
});

const QB_LINK = "https://marineintelligenceweekly.com/meoclass1";

function buildWelcomeEmail(tier, buyerName, buyerEmail) {
  const isFounders = tier === "founders";
  const price = isFounders ? "₹499" : "₹899";
  const tierLabel = isFounders ? "Founders Access" : "Standard Access";

  const founderExtra = isFounders
    ? `<p style="background:#f0fdfa;border-left:3px solid #0d9488;padding:10px 14px;margin:16px 0;font-size:14px;color:#134e4a;">
        <strong>You are part of the Founders Group — one of only 20 seats.</strong> Your slot is held until you pass your MMD oral examination.
      </p>`
    : "";

  return {
    from: `"Marine Intelligence Weekly" <${process.env.BREVO_SMTP_LOGIN}>`,
    to: buyerEmail,
    subject: `🚢 Your MEO Class 1 QB is ready — ${tierLabel}`,
    html: `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',system-ui,sans-serif">
  <div style="max-width:560px;margin:2rem auto;background:#ffffff;border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.05)">
    
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:1.5rem">
      <p style="color:#0d9488;font-weight:700;font-size:1.15rem;margin:0;letter-spacing:.02em">Marine Intelligence Weekly</p>
      <p style="color:#94a3b8;font-size:13px;margin:4px 0 0">MEO Class 1 Question Bank</p>
    </div>

    <!-- Body -->
    <div style="padding:2rem">
      <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${buyerName || "there"},</p>
      <p style="color:#334155;margin:0 0 16px;line-height:1.6">
        Thank you for subscribing to the <strong>MIW MEO Class 1 Question Bank</strong> (${tierLabel} — ${price}).
        Your access is ready. Let's get you through those orals. ⚓
      </p>

      ${founderExtra}

      <!-- CTA Button -->
      <div style="text-align:center;margin:28px 0">
        <a href="${QB_LINK}"
           style="background:#0d9488;color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:8px;font-weight:600;font-size:15px;display:inline-block;box-shadow:0 2px 8px rgba(13,148,136,.2)">
          Access Your Question Bank →
        </a>
      </div>

      <p style="font-size:13px;color:#64748b;margin:0 0 8px;text-align:center">
        Or copy to your browser: <br>
        <a href="${QB_LINK}" style="color:#0d9488;word-break:break-all;font-size:12px">${QB_LINK}</a>
      </p>

      <!-- Instructions -->
      <div style="border-top:1px solid #e2e8f0;margin:24px 0;padding-top:16px">
        <p style="font-size:14px;font-weight:600;color:#0f172a;margin:0 0 10px">✓ Important — please read</p>
        <ul style="font-size:13px;color:#334155;padding-left:18px;margin:0;line-height:1.8">
          <li style="margin-bottom:6px"><strong>Bookmark this page</strong> — save it for anytime access</li>
          <li style="margin-bottom:6px">Your access is <strong>personal and non-transferable</strong> — do not share this link</li>
          <li style="margin-bottom:6px">New questions added regularly — all updates are <strong>free for life</strong></li>
          <li style="margin-bottom:6px">Questions? Email <a href="mailto:contactus@marineintelligenceweekly.com" style="color:#0d9488">contactus@marineintelligenceweekly.com</a></li>
        </ul>
      </div>

      <p style="font-size:14px;color:#334155;margin:16px 0 2px">All the best for your orals.</p>
      <p style="font-size:14px;color:#0f172a;font-weight:600;margin:0">Nixon Antony</p>
      <p style="font-size:12px;color:#64748b;margin:2px 0 0">Second Engineer, Maersk A/S &nbsp;|&nbsp; Marine Intelligence Weekly</p>
    </div>

    <!-- Footer -->
    <div style="background:#f1f5f9;padding:1rem 1.5rem;text-align:center;border-top:1px solid #e2e8f0">
      <p style="font-size:11px;color:#94a3b8;margin:0">
        &copy; 2026 Marine Intelligence Weekly &nbsp;|&nbsp;
        <a href="https://marineintelligenceweekly.com/terms.html" style="color:#64748b;text-decoration:none">Terms</a> &nbsp;|&nbsp;
        <a href="https://marineintelligenceweekly.com/privacy.html" style="color:#64748b;text-decoration:none">Privacy</a>
      </p>
    </div>

  </div>
</body>
</html>`,
  };
}

export default async function handler(req, res) {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // --- Validate Razorpay credentials ---
    const KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;
    if (!KEY_SECRET) {
      console.error("Missing RAZORPAY_KEY_SECRET in environment");
      return res.status(500).json({ error: "Server configuration error" });
    }

    // --- Parse request ---
    const {
      razorpay_order_id,
      razorpay_payment_id,
      razorpay_signature,
      buyer_email,
      buyer_name,
      tier,
    } = req.body;

    // --- Validate required fields ---
    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
      return res.status(400).json({
        error: "Missing payment details",
        code: "MISSING_FIELDS",
      });
    }

    if (!buyer_email || !tier) {
      return res.status(400).json({
        error: "Missing buyer details",
        code: "MISSING_BUYER",
      });
    }

    // --- CRITICAL: Verify Razorpay signature ---
    // This is the security check — prevents spoofed payments
    const expectedSignature = crypto
      .createHmac("sha256", KEY_SECRET)
      .update(`${razorpay_order_id}|${razorpay_payment_id}`)
      .digest("hex");

    if (expectedSignature !== razorpay_signature) {
      console.error(
        `Signature mismatch: expected ${expectedSignature}, got ${razorpay_signature}`
      );
      return res.status(400).json({
        error: "Payment verification failed — signature mismatch",
        code: "SIGNATURE_MISMATCH",
      });
    }

    // --- Signature valid — send QB access email ---
    const validTier = ["founders", "standard"].includes(tier) ? tier : "standard";
    const emailOptions = buildWelcomeEmail(validTier, buyer_name, buyer_email);

    await transporter.sendMail(emailOptions);

    console.log(`✓ QB access sent: ${buyer_email} | tier: ${validTier} | order: ${razorpay_order_id}`);

    // --- Success response ---
    return res.status(200).json({
      success: true,
      message: "Payment verified and access email sent",
      tier: validTier,
      order_id: razorpay_order_id,
    });

  } catch (error) {
    console.error("verify-payment error:", error);
    return res.status(500).json({
      error: "Internal server error",
      code: "INTERNAL_ERROR",
    });
  }
}
