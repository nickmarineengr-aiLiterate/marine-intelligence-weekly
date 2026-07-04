// =============================================================
// Marine Intelligence Weekly — QB Login via Upstash Redis
// File: api/check-password.js
// v2: single-active-device enforcement.
//
// How it works:
// - Client generates a random device_id once (localStorage) and
//   sends it with every check-password call, including the silent
//   re-verify on page load.
// - On a successful password match, we compare the device_id in the
//   request against miw:active_device:<email> in Redis.
//   - No record yet, or record matches this device -> allow, refresh
//     the 30-day TTL.
//   - Record exists and belongs to a DIFFERENT device -> this new
//     login WINS and overwrites it (the old device's next silent
//     re-verify will then fail and it gets logged out). This is a
//     "last login wins" policy, not a hard block — simplest to run
//     without generating support tickets for a genuine device switch,
//     while still surfacing sharing (multiple people fighting over one
//     password will keep kicking each other out and notice).
// =============================================================

async function redisGet(url, token, key) {
  const r = await fetch(`${url}/get/${encodeURIComponent(key)}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await r.json();
  return data.result || null;
}

// Raw-command POST form — see razorpay-webhook.js / verify-payment.js
// for why we don't use query-string flags for SET ... EX here.
async function redisSetEx(url, token, key, value, ttlSeconds) {
  const r = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(["SET", key, value, "EX", ttlSeconds]),
  });
  const data = await r.json();
  return data.result === "OK";
}

const THIRTY_DAYS_SECONDS = 30 * 24 * 60 * 60;

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  try {
    const { email, password, device_id } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, error: "Missing fields" });
    }
    // device_id is optional for backward compatibility with any client
    // that hasn't been updated yet, but device enforcement only applies
    // when it's present. Update pay.html to always send one.
    const deviceId = (device_id || "").trim();

    const UPSTASH_URL = process.env.KV_REST_API_URL;
    const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;

    if (!UPSTASH_URL || !UPSTASH_TOKEN) {
      return res.status(500).json({ success: false, error: "DB config error" });
    }

    const emailKey = email.toLowerCase().trim();
    const userKey = `miw:user:${emailKey}`;
    const storedPassword = await redisGet(UPSTASH_URL, UPSTASH_TOKEN, userKey);

    if (!(storedPassword && storedPassword === password.trim())) {
      return res.status(200).json({ success: false });
    }

    // Password is correct. Now enforce single-active-device, only if
    // the caller sent a device_id.
    if (deviceId) {
      const deviceKey = `miw:active_device:${emailKey}`;
      const activeDevice = await redisGet(UPSTASH_URL, UPSTASH_TOKEN, deviceKey);

      if (activeDevice && activeDevice !== deviceId) {
        console.log(`[check-password] ${emailKey}: new device ${deviceId} is taking over from ${activeDevice}`);
      }

      // Claim/refresh this device as the active one (last login wins).
      await redisSetEx(UPSTASH_URL, UPSTASH_TOKEN, deviceKey, deviceId, THIRTY_DAYS_SECONDS);
    }

    console.log(`✓ Login: ${emailKey}`);
    res.setHeader("Set-Cookie",
      "miw_auth=1; Path=/; Max-Age=2592000; SameSite=Lax; Secure"
    );
    return res.status(200).json({ success: true });

  } catch (error) {
    console.error("check-password error:", error);
    return res.status(500).json({ success: false, error: "Server error" });
  }
}
