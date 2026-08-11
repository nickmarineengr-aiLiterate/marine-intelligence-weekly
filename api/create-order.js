// =============================================================
// Marine Intelligence Weekly — Razorpay Create Order (V2)
// File: api/create-order.js
// Endpoint: POST /api/create-order
//
// WHAT CHANGED AND WHY
// --------------------
// The previous version did:
//     const { amount, tier, buyer_email } = req.body;
//     const amountInPaise = Math.round(amount * 100);
// i.e. the browser chose what it would be charged. A trivially
// edited request bought any product for ₹1.
//
// Now: the request names a PRODUCT. The server looks the price up in
// api/_lib/products.js and ignores any amount in the body entirely.
// The product identity is written into Razorpay order notes, which
// only the server can set, so verification later has a trustworthy
// record of what was actually bought.
// =============================================================

import { resolvePurchase, PurchaseError } from "./_lib/products.js";

function razorpayRequest(method, path, auth, body = null) {
  return fetch(`https://api.razorpay.com${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${Buffer.from(auth).toString("base64")}`,
    },
    body: body ? JSON.stringify(body) : undefined,
  }).then(async (r) => ({ status: r.status, data: await r.json() }));
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const KEY_ID = process.env.RAZORPAY_KEY_ID;
    const KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;
    if (!KEY_ID || !KEY_SECRET) {
      console.error("Missing Razorpay credentials in environment");
      return res.status(500).json({ error: "Server configuration error" });
    }

    const body = req.body || {};
    const buyerEmail = String(body.buyer_email || body.email || "").trim().toLowerCase();
    const buyerName = String(body.buyer_name || body.name || "").trim();

    if (!buyerEmail || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(buyerEmail)) {
      return res.status(400).json({ error: "A valid email address is required" });
    }

    // ---- Server decides the product and the price. ----
    // Anything the client sent as `amount` is discarded here.
    let purchase;
    try {
      purchase = resolvePurchase({ product: body.product, tier: body.tier });
    } catch (e) {
      if (e instanceof PurchaseError) return res.status(e.status).json({ error: e.message });
      throw e;
    }

    if (body.amount !== undefined) {
      // Not an error — the live storefront still sends it. Log so we
      // can see when the last client stops doing so, and move on.
      console.log(
        `[create-order] ignoring client-supplied amount=${body.amount} for ` +
        `${purchase.productId}/${purchase.tier}; server amount=${purchase.amount}`
      );
    }

    const orderPayload = {
      amount: purchase.amount,       // paise, from the catalogue
      currency: purchase.currency,   // INR, from the catalogue
      receipt: `miw-${purchase.productId.toLowerCase()}-${Date.now()}`,
      notes: {
        // Server-authored. Razorpay returns these on order fetch, so
        // verification can trust them in a way it can never trust the
        // browser's claim about what was purchased.
        product: purchase.productId,
        tier: purchase.tier,
        buyer_email: buyerEmail,
        buyer_name: buyerName,
      },
    };

    const rp = await razorpayRequest(
      "POST", "/v1/orders", `${KEY_ID}:${KEY_SECRET}`, orderPayload
    );

    if (rp.status !== 200) {
      console.error("Razorpay API error:", rp.data);
      return res.status(502).json({ error: "Failed to create order" });
    }

    return res.status(200).json({
      success: true,
      order_id: rp.data.id,
      amount: rp.data.amount,       // echo of the SERVER amount
      currency: rp.data.currency,
      product: purchase.productId,
      tier: purchase.tier,
      label: purchase.label,
      key_id: KEY_ID,               // publishable, needed by checkout.js
    });

  } catch (error) {
    console.error("create-order error:", error.message);
    return res.status(500).json({ error: "Internal server error" });
  }
}
