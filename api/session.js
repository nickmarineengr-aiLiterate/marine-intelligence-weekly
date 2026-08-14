// =============================================================
// Marine Intelligence Weekly — Session introspection / logout
// File: api/session.js
// Endpoints:
//   GET  /api/session   -> who am I, and what do I own?
//   POST /api/session   -> {action:"logout"} clears the session
//
// This is what SQ/pay.html uses to render the product hub. The page
// asks the SERVER what is owned; it never decides from localStorage.
// =============================================================

import { parseCookies, verifySessionToken, clearCookies, SESSION_COOKIE } from "./_lib/session.js";
import {
  isActiveSession, removeActiveSession, clearAllSessions,
  getEntitlements, getEntitlementDetail, MAX_ACTIVE_SESSIONS,
} from "./_lib/entitlements.js";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Cache-Control", "no-store, private");
  if (req.method === "OPTIONS") return res.status(200).end();

  const cookies = parseCookies(req.headers.cookie);
  const payload = verifySessionToken(cookies[SESSION_COOKIE]);

  if (req.method === "POST") {
    const body = req.body || {};
    const action = String(body.action || "");
    if (action !== "logout") return res.status(400).json({ error: "Unknown action" });

    if (payload) {
      // Default logout signs out THIS device only — the customer's
      // other device stays signed in, which is the point of allowing
      // two. {scope:"all"} is the deliberate "sign out everywhere"
      // escape hatch, and is what credential rotation must use.
      if (String(body.scope || "") === "all") {
        await clearAllSessions(payload.e).catch(() => {});
      } else {
        await removeActiveSession(payload.e, payload.s).catch(() => {});
      }
    }
    res.setHeader("Set-Cookie", clearCookies());
    return res.status(200).json({ success: true, authenticated: false });
  }

  if (req.method !== "GET") return res.status(405).end();

  if (!payload) {
    return res.status(200).json({ authenticated: false, entitlements: {} });
  }

  // A valid signature is not enough — the session must still be one
  // of the account's live sessions. Logging in on a THIRD device
  // retires the oldest, and that retired token lands here.
  if (!(await isActiveSession(payload.e, payload.s))) {
    res.setHeader("Set-Cookie", clearCookies());
    return res.status(200).json({
      authenticated: false, reason: "evicted", entitlements: {},
    });
  }

  // `entitlements` stays BOOLEAN — "may they read it right now" — because
  // that is the only question every existing caller asks, and changing
  // its shape would silently alter what those callers decide.
  // `access` carries the term alongside it, for surfaces that want to
  // say "until 14 August 2027" or "lifetime".
  const [entitlements, access] = await Promise.all([
    getEntitlements(payload.e), getEntitlementDetail(payload.e),
  ]);
  return res.status(200).json({
    authenticated: true,
    email: payload.e,
    expires: payload.x,
    entitlements,
    access,
    maxSessions: MAX_ACTIVE_SESSIONS,
  });
}
