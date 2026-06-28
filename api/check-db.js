// api/check-db.js — temporary debug endpoint, delete after use
// GET /api/check-db?email=test@test.com

export default async function handler(req, res) {
  const email = req.query.email;
  if (!email) return res.status(400).json({ error: "email param required" });

  const UPSTASH_URL = process.env.KV_REST_API_URL;
  const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;

  if (!UPSTASH_URL || !UPSTASH_TOKEN) {
    return res.status(500).json({ 
      error: "Upstash env vars missing",
      url_set: !!UPSTASH_URL,
      token_set: !!UPSTASH_TOKEN
    });
  }

  const key = `miw:user:${email.toLowerCase().trim()}`;
  const response = await fetch(
    `${UPSTASH_URL}/get/${encodeURIComponent(key)}`,
    { headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` } }
  );
  const data = await response.json();

  return res.status(200).json({
    email,
    key,
    found: !!data.result,
    password: data.result || "NOT FOUND",
    raw: data
  });
}
