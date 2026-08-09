// =============================================================
// Marine Intelligence Weekly — Signed session tokens
// File: api/_lib/session.js
//
// WHY THIS EXISTS
// ---------------
// The previous model set `miw_auth=1` — a readable, unsigned,
// identity-free cookie — and every paid page did:
//     if(!/miw_auth=1/.test(document.cookie)) location.replace(...)
// Anyone could type `document.cookie="miw_auth=1"` and walk in, and
// the server had no idea WHO the visitor was, so it could not have
// checked entitlements even if it wanted to.
//
// A session token now carries identity (email + session id + expiry)
// and is HMAC-signed with MIW_SESSION_SECRET. It is unforgeable
// without the secret, and it tells the server who is asking.
//
// Format:  v1.<base64url(payload)>.<base64url(hmac)>
// Payload: {"e": email, "s": sessionId, "x": expiryEpochSeconds}
//
// This module is used by Node serverless functions. middleware.js
// re-implements VERIFY ONLY against the same format using Web Crypto,
// because Edge has no node:crypto. Keep the two in sync.
// =============================================================

import crypto from "crypto";

export const SESSION_COOKIE = "miw_session";
// Non-secret convenience flag so existing client UI can cheaply know
// "probably logged in" without a round trip. It authorizes NOTHING.
export const UI_FLAG_COOKIE = "miw_auth";

export const SESSION_TTL_SECONDS = 30 * 24 * 60 * 60; // 30 days

function b64url(buf) {
  return Buffer.from(buf).toString("base64")
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function b64urlDecode(str) {
  const pad = str.length % 4 === 0 ? "" : "=".repeat(4 - (str.length % 4));
  return Buffer.from(str.replace(/-/g, "+").replace(/_/g, "/") + pad, "base64");
}

function secret() {
  const s = process.env.MIW_SESSION_SECRET;
  if (!s || s.length < 16) {
    const e = new Error("MIW_SESSION_SECRET missing or too short");
    e.status = 500;
    throw e;
  }
  return s;
}

function sign(payloadB64) {
  return b64url(crypto.createHmac("sha256", secret()).update(payloadB64).digest());
}

export function newSessionId() {
  return crypto.randomBytes(16).toString("hex");
}

/** Mint a signed token. Does NOT touch Redis. */
export function createSessionToken(email, sessionId, ttlSeconds = SESSION_TTL_SECONDS) {
  const payload = {
    e: String(email).toLowerCase().trim(),
    s: sessionId,
    x: Math.floor(Date.now() / 1000) + ttlSeconds,
  };
  const payloadB64 = b64url(JSON.stringify(payload));
  return `v1.${payloadB64}.${sign(payloadB64)}`;
}

/**
 * Verify signature + expiry. Returns the payload or null.
 * Does NOT check Redis active-session — callers must do that
 * separately so a revoked session can be evicted.
 */
export function verifySessionToken(token) {
  if (!token || typeof token !== "string") return null;
  const parts = token.split(".");
  if (parts.length !== 3 || parts[0] !== "v1") return null;

  const [, payloadB64, sig] = parts;
  let expected;
  try {
    expected = sign(payloadB64);
  } catch {
    return null;
  }

  // Constant-time compare — lengths must match first or timingSafeEqual throws.
  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;

  let payload;
  try {
    payload = JSON.parse(b64urlDecode(payloadB64).toString("utf8"));
  } catch {
    return null;
  }

  if (!payload || !payload.e || !payload.s || !payload.x) return null;
  if (Math.floor(Date.now() / 1000) >= payload.x) return null;

  return payload;
}

/**
 * Cookie headers for a fresh login.
 * miw_session  — HttpOnly, the actual authority.
 * miw_auth     — readable UI hint only; middleware ignores it entirely.
 */
export function sessionCookies(token, { secure = true } = {}) {
  const base = `Path=/; Max-Age=${SESSION_TTL_SECONDS}; SameSite=Lax${secure ? "; Secure" : ""}`;
  return [
    `${SESSION_COOKIE}=${token}; HttpOnly; ${base}`,
    `${UI_FLAG_COOKIE}=1; ${base}`,
  ];
}

export function clearCookies({ secure = true } = {}) {
  const base = `Path=/; Max-Age=0; SameSite=Lax${secure ? "; Secure" : ""}`;
  return [
    `${SESSION_COOKIE}=; HttpOnly; ${base}`,
    `${UI_FLAG_COOKIE}=; ${base}`,
  ];
}

/** Parse a Cookie header into a plain object. */
export function parseCookies(header) {
  const out = {};
  if (!header) return out;
  for (const part of String(header).split(";")) {
    const i = part.indexOf("=");
    if (i < 0) continue;
    out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  return out;
}

// -------------------------------------------------------------
// Password storage. Existing accounts hold PLAINTEXT passwords in
// miw:user:<email> (assigned from QB_PASSWORD_POOL). We must keep
// verifying those, but we stop creating new ones: verifyPassword
// reports whether the stored form was legacy so the caller can
// transparently upgrade it to a salted hash on next successful login.
// -------------------------------------------------------------

export function hashPassword(password, salt = crypto.randomBytes(16).toString("hex")) {
  const h = crypto.createHash("sha256").update(`${salt}:${password}`).digest("hex");
  return `sha256$${salt}$${h}`;
}

export function verifyPassword(stored, supplied) {
  if (!stored) return { ok: false, legacy: false };
  const given = String(supplied || "").trim();

  if (stored.startsWith("sha256$")) {
    const [, salt] = stored.split("$");
    const candidate = hashPassword(given, salt);
    const a = Buffer.from(candidate);
    const b = Buffer.from(stored);
    const ok = a.length === b.length && crypto.timingSafeEqual(a, b);
    return { ok, legacy: false };
  }

  // Legacy plaintext record.
  const a = Buffer.from(stored);
  const b = Buffer.from(given);
  const ok = a.length === b.length && crypto.timingSafeEqual(a, b);
  return { ok, legacy: true };
}
