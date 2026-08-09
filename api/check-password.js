// =============================================================
// Marine Intelligence Weekly — Login (Security V2)
// File: api/check-password.js
// Endpoint: POST /api/check-password
//
// WHAT CHANGED AND WHY
// --------------------
// Before: a correct password produced `miw_auth=1` — readable,
// unsigned, and carrying no identity. The server could not tell one
// customer from another, and the browser could set the cookie itself.
//
// Now: a correct password mints a signed, HttpOnly session token
// bound to the account, registers it as THE active session, and
// returns the account's entitlements so the UI can render what is
// owned. `miw_auth=1` is still set, but purely as a UI hint that
// authorizes nothing (middleware never reads it).
//
// Password storage is also being migrated: existing accounts hold
// plaintext from QB_PASSWORD_POOL. Those still verify, and are
// transparently upgraded to a salted hash on first successful login.
// =============================================================

import { redisGet, redisSet, redisSetEx } from "./_lib/redis.js";
import {
  verifyPassword, hashPassword, createSessionToken, newSessionId,
  sessionCookies, SESSION_TTL_SECONDS,
} from "./_lib/session.js";
import {
  userKey, addActiveSession, getEntitlements, MAX_ACTIVE_SESSIONS,
} from "./_lib/entitlements.js";

const THIRTY_DAYS = 30 * 24 * 60 * 60;

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).end();

  try {
    const { email, password, device_id } = req.body || {};
    if (!email || !password) {
      return res.status(400).json({ success: false, error: "Missing fields" });
    }
    if (!process.env.MIW_SESSION_SECRET) {
      console.error("MIW_SESSION_SECRET is not set — refusing to issue sessions");
      return res.status(500).json({ success: false, error: "Server configuration error" });
    }

    const emailKey = String(email).toLowerCase().trim();
    const stored = await redisGet(userKey(emailKey));

    const { ok, legacy } = verifyPassword(stored, password);
    if (!ok) {
      // Deliberately identical response for "no such account" and
      // "wrong password" — no account enumeration.
      return res.status(200).json({ success: false });
    }

    // Opportunistic upgrade: replace the plaintext record with a
    // salted hash now that we've confirmed the password. Same
    // password keeps working; the stored form stops being readable.
    if (legacy) {
      try {
        await redisSet(userKey(emailKey), hashPassword(String(password).trim()));
        console.log(`[check-password] upgraded stored password to hash for ${emailKey}`);
      } catch (e) {
        // Non-fatal: login still succeeds on the legacy record.
        console.error("[check-password] hash upgrade failed:", e.message);
      }
    }

    // ---- Register this device's session (up to TWO per account) ----
    // Founder policy: a customer may stay signed in on a phone AND a
    // laptop. A third login does not fail — it retires the OLDEST
    // session, so the device in the customer's hand always works.
    const sessionId = newSessionId();
    const active = await addActiveSession(emailKey, sessionId, SESSION_TTL_SECONDS);
    const token = createSessionToken(emailKey, sessionId);

    // Legacy device bookkeeping retained so existing behaviour and
    // support expectations don't change; it is no longer authorization.
    const deviceId = String(device_id || "").trim();
    if (deviceId) {
      await redisSetEx(`miw:active_device:${emailKey}`, deviceId, THIRTY_DAYS);
    }

    const entitlements = await getEntitlements(emailKey);

    res.setHeader("Set-Cookie", sessionCookies(token));
    console.log(
      `✓ Login: ${emailKey} | session ${sessionId.slice(0, 8)}… | ` +
      `${active.length}/${MAX_ACTIVE_SESSIONS} devices active`
    );

    return res.status(200).json({
      success: true,
      email: emailKey,
      entitlements,
      // Lets the UI say "signed in on 2 of 2 devices" without another
      // round trip. Carries no authority — it is a count, not a token.
      activeSessions: active.length,
      maxSessions: MAX_ACTIVE_SESSIONS,
    });

  } catch (error) {
    console.error("check-password error:", error.message);
    return res.status(500).json({ success: false, error: "Server error" });
  }
}
