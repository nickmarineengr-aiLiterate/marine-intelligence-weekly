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
// Password storage accepts HASHED RECORDS ONLY. Accounts once held
// plaintext from QB_PASSWORD_POOL, and for a time a plaintext record
// still verified and was upgraded on login. After the git-history
// credential exposure all 100 production credentials were rotated to
// fresh random values stored as hashes, and that legacy branch was
// deleted from _lib/session.js. A non-hash record now fails to
// authenticate rather than being repaired.
// =============================================================

import { redisGet, redisSetEx } from "./_lib/redis.js";
import {
  verifyPassword, createSessionToken, newSessionId,
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

    const { ok } = verifyPassword(stored, password);
    if (!ok) {
      // Deliberately identical response for "no such account",
      // "wrong password" and "stored record is not a hash" — no
      // account enumeration, and no signal that a record exists but
      // is in an unusable form.
      return res.status(200).json({ success: false });
    }

    // There is no opportunistic plaintext->hash upgrade here any more.
    // It was removed with the legacy verify branch in _lib/session.js
    // after all 100 production credentials were rotated to hashes; see
    // the note there. A login can no longer write to the credential
    // record at all, which is the property that makes this endpoint
    // read-only with respect to stored secrets.

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
