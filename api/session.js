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
import { getActiveSession, clearActiveSession, getEntitlements } from "./_lib/entitlements.js";

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
    const action = String((req.body || {}).action || "");
    if (action !== "logout") return res.status(400).json({ error: "Unknown action" });
    if (payload) await clearActiveSession(payload.e).catch(() => {});
    res.setHeader("Set-Cookie", clearCookies());
    return res.status(200).json({ success: true, authenticated: false });
  }

  if (req.method !== "GET") return res.status(405).end();

  if (!payload) {
    return res.status(200).json({ authenticated: false, entitlements: {} });
  }

  // A valid signature is not enough — the session must still be THE
  // active one. A second login elsewhere evicts this token.
  const active = await getActiveSession(payload.e);
  if (!active || active !== payload.s) {
    res.setHeader("Set-Cookie", clearCookies());
    return res.status(200).json({
      authenticated: false, reason: "evicted", entitlements: {},
    });
  }

  const entitlements = await getEntitlements(payload.e);
  return res.status(200).json({
    authenticated: true,
    email: payload.e,
    expires: payload.x,
    entitlements,
  });
}
