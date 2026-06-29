// =============================================================
// Marine Intelligence Weekly — QB Login via Upstash Redis
// File: api/check-password.js
// =============================================================

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, error: "Missing fields" });
    }

    const UPSTASH_URL = process.env.KV_REST_API_URL;
    const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;

    if (!UPSTASH_URL || !UPSTASH_TOKEN) {
      return res.status(500).json({ success: false, error: "DB config error" });
    }

    const key = `miw:user:${email.toLowerCase().trim()}`;
    const response = await fetch(`${UPSTASH_URL}/get/${encodeURIComponent(key)}`, {
      headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
    });

    const data = await response.json();
    const storedPassword = data.result;

    if (storedPassword && storedPassword === password.trim()) {
      console.log(`✓ Login: ${email}`);
      // Set auth cookie: 30 days, Secure, SameSite=Lax
      res.setHeader("Set-Cookie",
        "miw_auth=1; Path=/; Max-Age=2592000; SameSite=Lax; Secure; HttpOnly"
      );
      return res.status(200).json({ success: true });
    } else {
      return res.status(200).json({ success: false });
    }

  } catch (error) {
    console.error("check-password error:", error);
    return res.status(500).json({ success: false, error: "Server error" });
  }
}
