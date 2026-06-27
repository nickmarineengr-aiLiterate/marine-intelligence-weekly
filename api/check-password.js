// api/check-password.js
// Verifies QB access password

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  const { password } = req.body;
  const QB_PASSWORD = process.env.QB_ACCESS_PASSWORD;

  if (!QB_PASSWORD) {
    return res.status(500).json({ error: "Server config error" });
  }

  if (password === QB_PASSWORD) {
    return res.status(200).json({ success: true });
  } else {
    return res.status(200).json({ success: false });
  }
}
