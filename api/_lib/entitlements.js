// =============================================================
// Marine Intelligence Weekly — Product entitlements
// File: api/_lib/entitlements.js
//
// SCHEMA
// ------
//   miw:ent:<email>          Redis HASH
//       field ORAL_QB_NOTES = "1" | "<expiry epoch seconds>"
//       field SOLVED_QP     = "1" | "<expiry epoch seconds>"
//
//       field may also hold "passed:<closedAt>:<prior>" once the Founder
//       records that the member passed MEO Class I.
//
//   "1" means NO CLOCK-BASED EXPIRY and is what every customer who bought
//   before August 2026 holds; commercially that is Candidate-Lifecycle
//   Access. Purchases from then on carry a term and store an expiry
//   instead. api/_lib/grants.js owns the reading of that value,
//   and its trap note is required reading: Number("1") is 1970, so an
//   arithmetic-first comparison would expire the entire grandfathered
//   population in one deploy.
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
//   miw:sessions:<email>         sorted set — up to TWO live session
//                                ids, scored by login time. Defined in
//                                api/_lib/sessions.js.
//   miw:user:<email>             string — sha256$salt$digest ONLY.
//                                Plaintext records no longer verify;
//                                see api/_lib/session.js.
// =============================================================

import { redisCmd } from "./redis.js";
import { ALL_ENTITLEMENTS } from "./products.js";
import { grantAllowsAccess, grantState, extendedGrantValue } from "./grants.js";

export const entKey = (email) => `miw:ent:${String(email).toLowerCase().trim()}`;
export const userKey = (email) => `miw:user:${String(email).toLowerCase().trim()}`;

/**
 * Grant one or more entitlements. Additive — an existing grant is
 * EXTENDED, never shortened and never replaced by a shorter one.
 *
 * @param {string} email
 * @param {string|string[]} entitlements
 * @param {object} [opts]
 * @param {number|null} [opts.termDays] null ⇒ perpetual ("1")
 *
 * WHY THIS READS BEFORE IT WRITES
 * A blind HSET of a dated value would DOWNGRADE a grandfathered
 * customer the moment they bought anything — their perpetual "1"
 * overwritten by a one-year stamp, by their own payment. It would also
 * make an accidental double purchase shorten the second one to a single
 * year from today. extendedGrantValue() encodes both rules: perpetual
 * stays perpetual, and a renewal is added to whatever is already there.
 *
 * The read-modify-write window is acceptable here in a way it is not
 * for the trial: the worst interleaving of two concurrent grants for
 * the SAME product is that one term is added instead of two, which
 * under-grants rather than over-grants and is visible to support. A
 * grant for a DIFFERENT product cannot collide at all, because HSET
 * touches one field.
 */
export async function grantEntitlements(email, entitlements, opts = {}) {
  const list = (Array.isArray(entitlements) ? entitlements : [entitlements])
    .filter((e) => ALL_ENTITLEMENTS.includes(e));
  if (list.length === 0) return {};

  const termDays = opts.termDays === undefined ? null : opts.termDays;
  const now = Date.now();

  const existing = await getRawEntitlements(email);

  const args = ["HSET", entKey(email)];
  const out = {};
  for (const e of list) {
    const value = extendedGrantValue(existing[e], termDays, now);
    args.push(e, value);
    out[e] = value;
  }
  await redisCmd(args);
  return out;
}

/** The stored strings, exactly as Redis holds them. */
export async function getRawEntitlements(email) {
  const data = await redisCmd(["HGETALL", entKey(email)]);
  const raw = data.result;

  // Upstash returns HGETALL as a flat [k,v,k,v] array.
  const held = {};
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
  } else if (raw && typeof raw === "object") {
    Object.assign(held, raw);
  }
  return held;
}

/**
 * Read the full entitlement map. Always returns every known key.
 *
 * Stays BOOLEAN for every existing caller — true means "may read the
 * product right now", which is the only question /api/session and the
 * hub ever asked. Callers that need the date use getEntitlementDetail().
 */
export async function getEntitlements(email) {
  const held = await getRawEntitlements(email);
  const nowSeconds = Math.floor(Date.now() / 1000);
  const out = {};
  for (const e of ALL_ENTITLEMENTS) out[e] = grantAllowsAccess(held[e], nowSeconds);
  return out;
}

/** Per-product {status, expires, perpetual} — for the access hub. */
export async function getEntitlementDetail(email) {
  const held = await getRawEntitlements(email);
  const nowSeconds = Math.floor(Date.now() / 1000);
  const out = {};
  for (const e of ALL_ENTITLEMENTS) out[e] = grantState(held[e], nowSeconds);
  return out;
}

/** Single-field check — the hot path used when authorizing a request. */
export async function hasEntitlement(email, entitlement) {
  const data = await redisCmd(["HGET", entKey(email), entitlement]);
  return grantAllowsAccess(data.result, Math.floor(Date.now() / 1000));
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
// Active sessions now live in api/_lib/sessions.js as a bounded
// sorted set (Founder policy: TWO devices, e.g. mobile + laptop).
//
// The single-value helpers that used to live here are gone rather
// than deprecated-in-place, so there is exactly ONE definition of
// "is this session valid" in the codebase. Re-exported here only so
// existing importers keep a single obvious entry point.
// -------------------------------------------------------------

export {
  MAX_ACTIVE_SESSIONS,
  sessionsKey,
  addActiveSession,
  isActiveSession,
  listActiveSessions,
  removeActiveSession,
  clearAllSessions,
} from "./sessions.js";
