// =============================================================
// Marine Intelligence Weekly — Product entitlements
// File: api/_lib/entitlements.js
//
// SCHEMA
// ------
//   miw:ent:<email>          Redis HASH
//       field ORAL_QB_NOTES = "1"
//       field SOLVED_QP     = "1"
//
// A HASH (not a JSON blob) is deliberate:
//   * additive     — HSET one field never disturbs the others, so a
//                    Written purchase cannot clobber an Oral grant;
//   * idempotent   — re-running a grant is a no-op;
//   * race-free    — no read-modify-write window between the webhook
//                    and verify-payment, which can fire concurrently;
//   * extensible   — a future product is a new field, not a migration;
//   * cheap to gate— middleware reads ONE field (HGET), not the blob.
//
// ABSENCE OF A FIELD MEANS NO ACCESS. There is no default-true.
//
//   miw:active_session:<email>   string — the one live session id
//   miw:user:<email>             string — password (legacy plaintext
//                                or sha256$salt$hash after upgrade)
// =============================================================

import { redisCmd } from "./redis.js";
import { ALL_ENTITLEMENTS } from "./products.js";

export const entKey = (email) => `miw:ent:${String(email).toLowerCase().trim()}`;
export const sessionKey = (email) => `miw:active_session:${String(email).toLowerCase().trim()}`;
export const userKey = (email) => `miw:user:${String(email).toLowerCase().trim()}`;

/**
 * Grant one or more entitlements. Additive and idempotent —
 * existing grants are never touched, never removed.
 */
export async function grantEntitlements(email, entitlements) {
  const list = (Array.isArray(entitlements) ? entitlements : [entitlements])
    .filter((e) => ALL_ENTITLEMENTS.includes(e));
  if (list.length === 0) return {};

  const args = ["HSET", entKey(email)];
  for (const e of list) args.push(e, "1");
  await redisCmd(args);
  return Object.fromEntries(list.map((e) => [e, true]));
}

/** Read the full entitlement map. Always returns every known key. */
export async function getEntitlements(email) {
  const data = await redisCmd(["HGETALL", entKey(email)]);
  const raw = data.result;

  // Upstash returns HGETALL as a flat [k,v,k,v] array.
  const held = {};
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
  } else if (raw && typeof raw === "object") {
    Object.assign(held, raw);
  }

  const out = {};
  for (const e of ALL_ENTITLEMENTS) out[e] = held[e] === "1" || held[e] === 1;
  return out;
}

/** Single-field check — the hot path used when authorizing a request. */
export async function hasEntitlement(email, entitlement) {
  const data = await redisCmd(["HGET", entKey(email), entitlement]);
  return data.result === "1" || data.result === 1;
}

/**
 * Revoke one entitlement. Exposed for the admin runbook only —
 * no purchase path ever calls this.
 */
export async function revokeEntitlement(email, entitlement) {
  await redisCmd(["HDEL", entKey(email), entitlement]);
  return true;
}

// -------------------------------------------------------------
// Single active session. Second login replaces the first; the
// evicted session's next request fails the id comparison.
// -------------------------------------------------------------

export async function setActiveSession(email, sessionId, ttlSeconds) {
  await redisCmd(["SET", sessionKey(email), sessionId, "EX", ttlSeconds]);
  return true;
}

export async function getActiveSession(email) {
  const data = await redisCmd(["GET", sessionKey(email)]);
  return data.result ?? null;
}

export async function clearActiveSession(email) {
  await redisCmd(["DEL", sessionKey(email)]);
  return true;
}
