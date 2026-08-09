// =============================================================
// Marine Intelligence Weekly — Active session set (Security V2)
// File: api/_lib/sessions.js
//
// FOUNDER POLICY: a customer may stay logged in on TWO devices.
//
// The first Security V2 draft allowed exactly ONE active session
// (`miw:active_session:<email>` held a single id, and a second login
// silently evicted the first). That broke a standing promise to
// customers that a phone AND a laptop may both remain signed in.
// This module replaces that with a bounded set of TWO.
//
// SCHEMA
// ------
//   miw:sessions:<email>   Redis SORTED SET
//       member = session id
//       score  = login time, epoch seconds
//
// WHY A SORTED SET
//   * ordered      — "retire the OLDEST" is ZREMRANGEBYRANK, not a
//                    read-modify-write of a JSON blob;
//   * bounded      — trimming to the newest N is one command, so the
//                    cap cannot drift no matter how logins interleave;
//   * cheap to gate— authorising a request is ONE ZSCORE, the same
//                    single-command cost as the old GET;
//   * self-pruning — expired sessions are removed by score range, so
//                    the set does not accumulate dead ids;
//   * race-safe    — two concurrent logins both add then both trim;
//                    every interleaving leaves the newest N. There is
//                    no window where a third session survives.
//
// A set with MAX_ACTIVE_SESSIONS = 1 would reproduce the old
// behaviour exactly, so this is a generalisation of the previous
// mechanism, not a second one running beside it. The legacy
// single-value key is deleted on next login (see loginCommands).
//
// ENTITLEMENTS ARE NOT PER-DEVICE. Both sessions of an account see
// exactly the same entitlement set — this module never touches
// miw:ent:<email>.
// =============================================================

import { redisCmd, redisPipeline } from "./redis.js";

/** Founder-approved cap: mobile + laptop. */
export const MAX_ACTIVE_SESSIONS = 2;

const norm = (email) => String(email).toLowerCase().trim();

export const sessionsKey = (email) => `miw:sessions:${norm(email)}`;

/**
 * The pre-Security-V2 single-session key. Retained ONLY so it can be
 * deleted; nothing reads it any more.
 */
export const legacySessionKey = (email) => `miw:active_session:${norm(email)}`;

/**
 * Build the exact command sequence for a login. Pure — no I/O — so
 * the ordering guarantees can be asserted directly in tests.
 *
 * Order matters:
 *   1. drop sessions older than the TTL   (expiry cleanup)
 *   2. add the new session
 *   3. trim to the newest MAX            (evicts the oldest)
 *   4. refresh the key TTL
 *   5. delete the legacy single-session key
 *
 * Trimming AFTER adding is what makes the cap hold: the new session
 * is ranked against the survivors, so login #3 removes login #1.
 */
export function loginCommands(email, sessionId, nowSeconds, ttlSeconds) {
  const key = sessionsKey(email);
  const cutoff = nowSeconds - ttlSeconds;
  return [
    ["ZREMRANGEBYSCORE", key, "-inf", `(${cutoff}`],
    ["ZADD", key, String(nowSeconds), sessionId],
    ["ZREMRANGEBYRANK", key, "0", String(-(MAX_ACTIVE_SESSIONS + 1))],
    ["EXPIRE", key, String(ttlSeconds)],
    ["DEL", legacySessionKey(email)],
  ];
}

/** Default I/O bindings; tests inject an in-memory double instead. */
const defaultDeps = { cmd: redisCmd, pipeline: redisPipeline };

/**
 * Register a new session, evicting the oldest if the account is
 * already at the cap. Returns the session ids still valid, newest first.
 */
export async function addActiveSession(email, sessionId, ttlSeconds, deps = defaultDeps) {
  const now = Math.floor(Date.now() / 1000);
  await deps.pipeline(loginCommands(email, sessionId, now, ttlSeconds));
  return listActiveSessions(email, deps);
}

/**
 * Is this session id one of the account's currently valid sessions?
 * This is the hot authorisation path — exactly one command.
 */
export async function isActiveSession(email, sessionId, deps = defaultDeps) {
  if (!sessionId) return false;
  const data = await deps.cmd(["ZSCORE", sessionsKey(email), sessionId]);
  return data?.result !== null && data?.result !== undefined;
}

/** Active session ids, newest first. Used by the admin runbook and tests. */
export async function listActiveSessions(email, deps = defaultDeps) {
  const data = await deps.cmd(["ZREVRANGE", sessionsKey(email), "0", "-1"]);
  const raw = data?.result;
  return Array.isArray(raw) ? raw : [];
}

/**
 * Sign out ONE session — the device that pressed logout. The
 * customer's other device stays signed in, which is the whole point
 * of the two-session policy.
 */
export async function removeActiveSession(email, sessionId, deps = defaultDeps) {
  if (!sessionId) return false;
  const data = await deps.cmd(["ZREM", sessionsKey(email), sessionId]);
  return Number(data?.result || 0) > 0;
}

/**
 * Sign out EVERY device. Used by credential rotation — a rotated
 * password must not leave an attacker's session alive.
 */
export async function clearAllSessions(email, deps = defaultDeps) {
  await deps.pipeline([
    ["DEL", sessionsKey(email)],
    ["DEL", legacySessionKey(email)],
  ]);
  return true;
}
