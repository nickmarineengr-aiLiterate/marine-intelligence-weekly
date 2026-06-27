// =============================================================
// Marine Intelligence Weekly — Razorpay Create Order
// File: api/create-order.js
// Endpoint: POST /api/create-order
// Purpose: Create an order on Razorpay, receive order_id for checkout
// =============================================================

import https from "https";

function makeRazorpayRequest(method, path, auth, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: "api.razorpay.com",
      port: 443,
      path: path,
      method: method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Basic ${Buffer.from(auth).toString("base64")}`,
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => {
        data += chunk;
      });
      res.on("end", () => {
        try {
          resolve({
            status: res.statusCode,
            data: JSON.parse(data),
          });
        } catch (e) {
          reject(new Error(`Failed to parse Razorpay response: ${data}`));
        }
      });
    });

    req.on("error", (error) => {
      reject(error);
    });

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

export default async function handler(req, res) {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // --- Validate environment variables ---
    const KEY_ID = process.env.RAZORPAY_KEY_ID;
    const KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;

    if (!KEY_ID || !KEY_SECRET) {
      console.error("Missing Razorpay credentials in environment");
      return res.status(500).json({ error: "Server configuration error" });
    }

    // --- Parse request body ---
    const { amount, tier, buyer_email } = req.body;

    if (!amount || !tier || !buyer_email) {
      return res.status(400).json({ error: "Missing required fields: amount, tier, buyer_email" });
    }

    // --- Validate amount (minimum 100 paise = ₹1) ---
    const amountInPaise = Math.round(amount * 100);
    if (amountInPaise < 100) {
      return res.status(400).json({ error: "Amount must be at least ₹1" });
    }

    // --- Create order on Razorpay ---
    const orderPayload = {
      amount: amountInPaise,
      currency: "INR",
      receipt: `meo-${tier}-${Date.now()}`,
      notes: {
        tier: tier,
        buyer_email: buyer_email,
      },
    };

    const auth = `${KEY_ID}:${KEY_SECRET}`;
    const razorpayResponse = await makeRazorpayRequest(
      "POST",
      "/v1/orders",
      auth,
      orderPayload
    );

    if (razorpayResponse.status !== 200) {
      console.error("Razorpay API error:", razorpayResponse.data);
      return res.status(500).json({
        error: "Failed to create order",
        details: razorpayResponse.data.description,
      });
    }

    // --- Return order details to frontend ---
    return res.status(200).json({
      success: true,
      order_id: razorpayResponse.data.id,
      amount: razorpayResponse.data.amount,
      currency: razorpayResponse.data.currency,
    });

  } catch (error) {
    console.error("create-order error:", error);
    return res.status(500).json({ error: error.message });
  }
}
