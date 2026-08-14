// =============================================================
// Marine Intelligence Weekly — Account creation for trial candidates
// File: api/request-access.js
// Endpoint: POST /api/request-access   { email }
//
// Creates an MIW account for an address that does not already have
// one, and emails the password. It grants NOTHING — no entitlement, no
// trial, no clock. The candidate signs in with the emailed password and
// then explicitly starts a trial via POST /api/trial.
//
// Splitting it that way is deliberate. If this endpoint started the
// trial, a stranger could burn someone else's one free trial by typing
// their address into a form.
//
// This endpoint is deliberately thin, exactly like reset-password.js
// beside it. All of the decision logic — neutrality, throttling, and
// the absolute rule that an existing account is never touched — lives
// in _lib/reset.js so tools/security/ can exercise the real sequence
// offline with no network and no secrets.
// =============================================================

import { redisGet, redisDel, redisSetNX, redisCreateNX } from "./_lib/redis.js";
import { requestTrialAccount, SIGNUP_RESPONSE } from "./_lib/reset.js";
import { buildTrialAccountEmail, makeTransport } from "./_lib/email.js";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Cache-Control", "no-store, private");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  const { email } = req.body || {};

  const store = {
    get: redisGet,
    del: redisDel,
    claim: (key, ttl) => redisSetNX(key, "1", ttl),
    // Durable create, no TTL. redisSetNX would have expired the
    // credential in 24 hours — see the note on redisCreateNX.
    createNX: redisCreateNX,
  };

  try {
    const { outcome } = await requestTrialAccount({
      email,
      store,
      buildEmail: buildTrialAccountEmail,
      sendMail: async (message) => {
        const transport = await makeTransport();
        return transport.sendMail(message);
      },
    });

    // Masked, for the same reason reset-password masks it: an unmasked
    // line here would become a durable record of who asked for access.
    const masked = String(email || "").replace(/^(.{0,2})[^@]*/, "$1***");
    console.log(`[request-access] ${masked} -> ${outcome}`);
  } catch (e) {
    // An internal failure must not change the response shape, or the
    // error itself becomes the enumeration oracle.
    console.error("[request-access] error:", e.message);
  }

  // ONE response for every path: created, throttled, address already
  // has an account, malformed address, or an exception above.
  return res.status(200).json({ success: true, message: SIGNUP_RESPONSE });
}
