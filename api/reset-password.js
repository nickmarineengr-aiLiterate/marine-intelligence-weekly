// =============================================================
// Marine Intelligence Weekly — Password reset
// File: api/reset-password.js
// Endpoint: POST /api/reset-password   { email }
//
// Issues a NEW password and emails it. It cannot resend the existing
// one — credentials are stored as salted hashes and the plaintext
// exists nowhere. See api/_lib/reset.js for the reasoning and for the
// three properties that make an unauthenticated reset form safe:
// no enumeration, throttled, sessions revoked.
//
// This endpoint is deliberately thin. All of the decision logic lives
// in _lib/reset.js so tools/security/reset.test.mjs can exercise the
// real sequence offline with no network and no secrets.
// =============================================================

import { redisGet, redisSet, redisDel, redisCmd, redisSetNX } from "./_lib/redis.js";
import { requestReset, GENERIC_RESPONSE } from "./_lib/reset.js";
import { buildResetEmail, makeTransport } from "./_lib/email.js";
import { sessionsKey } from "./_lib/sessions.js";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  const { email } = req.body || {};

  const store = {
    get: redisGet,
    set: redisSet,
    del: redisDel,
    countSessions: async (e) => Number((await redisCmd(["ZCARD", sessionsKey(e)])).result || 0),
    claim: (key, ttl) => redisSetNX(key, "1", ttl),
  };

  try {
    const { outcome } = await requestReset({
      email,
      store,
      buildEmail: buildResetEmail,
      sendMail: async (message) => {
        const transport = await makeTransport();
        return transport.sendMail(message);
      },
    });

    // Logged for the operator, never returned. The masking matters:
    // this line would otherwise become a record of which addresses are
    // customers, sitting in a log with a longer retention than anyone
    // intends.
    const masked = String(email || "").replace(/^(.{0,2})[^@]*/, "$1***");
    console.log(`[reset-password] ${masked} -> ${outcome}`);
  } catch (e) {
    // Even an internal failure must not change the response shape, or
    // the error itself becomes the enumeration oracle.
    console.error("[reset-password] error:", e.message);
  }

  // ONE response for every path: sent, throttled, no such account,
  // malformed address, or an exception above.
  return res.status(200).json({ success: true, message: GENERIC_RESPONSE });
}
