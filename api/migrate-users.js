// api/migrate-users.js v2 — writes both directions
// GET /api/migrate-users?secret=MIW-MIGRATE-2026

export default async function handler(req, res) {
  if (req.query.secret !== "MIW-MIGRATE-2026") {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const UPSTASH_URL = process.env.KV_REST_API_URL;
  const UPSTASH_TOKEN = process.env.KV_REST_API_TOKEN;

  if (!UPSTASH_URL || !UPSTASH_TOKEN) {
    return res.status(500).json({ error: "Upstash env vars missing" });
  }

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
    "vsteverichard@gmail.com": "MIW-0CjmZeAC",
    "nickurfriend@yahoo.co.in": "MIW-tKaiDctB",
    "nickurfriend@gmail.com": "MIW-RA3pKZsg"
  };

  async function redisSet(key, value) {
    const r = await fetch(
      `${UPSTASH_URL}/set/${encodeURIComponent(key)}/${encodeURIComponent(value)}`,
      { headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` } }
    );
    return r.json();
  }

  const results = [];
  for (const [email, password] of Object.entries(users)) {
    // email → password
    await redisSet(`miw:user:${email}`, password);
    // password → email (reverse lookup for assignPassword)
    await redisSet(`miw:pwd:${password}`, email);
    results.push({ email, password });
  }

  return res.status(200).json({
    success: true,
    migrated: results.length,
    users: results
  });
}
