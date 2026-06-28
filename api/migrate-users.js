// =============================================================
// Marine Intelligence Weekly — One-time user migration
// File: api/migrate-users.js
// Run ONCE: GET /api/migrate-users?secret=MIW-MIGRATE-2026
// DELETE this file after migration is confirmed
// =============================================================

export default async function handler(req, res) {
  // Secret key to prevent unauthorized access
  if (req.query.secret !== "MIW-MIGRATE-2026") {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const UPSTASH_URL = process.env.KV_REST_API_URL;
  const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;

  if (!UPSTASH_URL || !UPSTASH_TOKEN) {
    return res.status(500).json({ error: "Upstash env vars missing" });
  }

  // All existing users
  const users = {
    "nickmarineengr@gmail.com": "MIW-NMjFt02S",
    "muhammedmusthafa.va@gmail.com": "MIW-OPlWwGCB",
    "sijose104@gmail.com": "MIW-04WJPSM5",
    "renjithgnair5@gmail.com": "MIW-ikDgZeUk",
    "jonbernadpaul@gmail.com": "MIW-uAMtzDyG",
    "jijozach@gmail.com": "MIW-tbPyDW5i",
    "anand.newton@gmail.com": "MIW-SldSMgtp",
    "rnair.vishnu@gmail.com": "MIW-cOwuCCK2",
    "hariprasanna.cool@gmail.com": "MIW-dkK0a1Z4",
    "sujesh_tv@yahoo.com": "MIW-vXCRO86U",
    "arunaps.mariner@gmail.com": "MIW-KdBE1RlL",
    "pradeepmech.mech@gmail.com": "MIW-fRkFM1Kp",
    "anthinthomas@gmail.com": "MIW-mXDdRsza",
    "chetan.mlore@gmail.com": "MIW-6BfQEEtA",
    "bibinbaby2201@gmail.com": "MIW-bL08Ni6b",
    "rohitmanikandan1989@gmail.com": "MIW-I4JJocwD",
    "vaisaksree17@gmail.com": "MIW-iVppV2Lp",
    "mail.thomasbibin@gmail.com": "MIW-w8Dzy4hJ",
    "tg.rathesh@gmail.com": "MIW-MGjZGJib",
    "riya3august@gmail.com": "MIW-C6erKkzf",
    "sailorsailor477@gmail.com": "MIW-Ux5SquBd",
    "svoore25@gmail.com": "MIW-IwTtJNPp",
    "aseef9@gmail.com": "MIW-wPgT9uBM",
    "vijeesh87@gmail.com": "MIW-bh8zJ93O",
    "goopi19@gmail.com": "MIW-ORsVqvqI",
    "vsteverichard@gmail.com": "MIW-0CjmZeAC"
  };

  async function redisSet(key, value) {
    const response = await fetch(`${UPSTASH_URL}/set/${encodeURIComponent(key)}/${encodeURIComponent(value)}`, {
      headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
    });
    return response.json();
  }

  const results = [];
  for (const [email, password] of Object.entries(users)) {
    const key = `miw:user:${email}`;
    const result = await redisSet(key, password);
    results.push({ email, password, result });
  }

  // Store used passwords set for fast lookup
  const usedPasswords = Object.values(users);
  await fetch(`${UPSTASH_URL}/set/miw:used_passwords`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${UPSTASH_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(["SET", "miw:used_passwords", JSON.stringify(usedPasswords)])
  });

  return res.status(200).json({
    success: true,
    migrated: results.length,
    users: results
  });
}
