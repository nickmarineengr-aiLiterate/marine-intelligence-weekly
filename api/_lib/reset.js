// =============================================================
// Marine Intelligence Weekly — Self-service password reset
// File: api/_lib/reset.js
//
// WHY THIS CANNOT "RESEND THE SAME PASSWORD"
// ------------------------------------------
// The obvious feature request is "email me my password again". It is
// not implementable and never will be: miw:user:<email> holds
// sha256$salt$digest, and the plaintext exists nowhere — not in Redis,
// not in a log, not in this repository. That is the whole point of the
// remediation that produced these records. A reset therefore ISSUES A
// NEW CREDENTIAL; it cannot recover the old one.
//
// THE THREE THINGS THAT MAKE THIS SAFE
// ------------------------------------
// 1. NO ACCOUNT ENUMERATION. The response is byte-identical whether the
//    address has an account, has none, or is throttled. A reset form is
//    otherwise a free oracle for "is this person a customer", which is
//    exactly the question the leaked blob answered and which we are not
//    going to answer again through a different door.
//
// 2. THROTTLED. Anyone may request a reset for any address without
//    proving anything — that is inherent to the feature. Unthrottled,
//    it is a denial-of-service tool: repeatedly resetting a real
//    customer's password locks them out of a product they paid for,
//    from a form, anonymously. One reset per address per window closes
//    that. The throttle is an atomic SET NX EX, so two simultaneous
//    requests cannot both win.
//
// 3. SESSIONS REVOKED. If the reset happened because somebody else got
//    into the account, leaving their session alive would remediate
//    nothing. rotateAccount already does this.
//
// A THROTTLED REQUEST IS NOT A FAILURE. The email sent moments ago
// still contains a working password, so declining to send a second one
// is correct behaviour rather than a degraded path — and it keeps the
// generic response honest rather than merely vague.
// =============================================================

import { rotateAccount } from "./rotation.js";
import { userKey } from "./entitlements.js";

/** One reset per address per fifteen minutes. */
export const RESET_THROTTLE_SECONDS = 15 * 60;

export const throttleKey = (email) =>
  `miw:reset_throttle:${String(email).toLowerCase().trim()}`;

/**
 * The single sentence every caller gets back, whatever happened.
 * Deliberately true in all four cases: sent, throttled, no such
 * account, and malformed address.
 */
export const GENERIC_RESPONSE =
  "If that address has an account, a new password has been emailed to it. " +
  "Please also check your spam folder.";

/**
 * @param {object} o
 * @param {string} o.email
 * @param {object} o.store   {get, set, del, countSessions, claim}
 *                           claim(key, ttl) -> true for exactly one caller
 * @param {function} o.sendMail
 * @param {function} o.buildEmail
 * @returns {Promise<{outcome: string}>}
 *   outcome is for LOGS AND TESTS ONLY and must never reach the client:
 *   "sent" | "throttled" | "no_account" | "invalid_email" | "send_failed"
 */
export async function requestReset({ email, store, sendMail, buildEmail, makePassword }) {
  const addr = String(email || "").toLowerCase().trim();

  // Shape check only. Anything that cannot be an address is rejected
  // before it reaches Redis, but the caller is told the same thing as
  // everyone else.
  if (!addr || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(addr)) {
    return { outcome: "invalid_email" };
  }

  // Throttle BEFORE the existence check. Doing it the other way round
  // leaks: an attacker could time the difference between "no account"
  // (fast, no Redis write) and "throttled" (slow) to enumerate.
  const claimed = await store.claim(throttleKey(addr), RESET_THROTTLE_SECONDS);
  if (!claimed) return { outcome: "throttled" };

  const stored = await store.get(userKey(addr));
  if (!stored) return { outcome: "no_account" };

  const result = await rotateAccount({
    email: addr,
    store,
    sendMail,
    buildEmail,
    makePassword,
    // Every production record is a hash, so a reset must be willing to
    // replace one. Without this the function would decline every real
    // account as "already safe".
    includeHashed: true,
  });

  if (result.status === "rotated") return { outcome: "sent" };
  if (result.status === "rotated_email_failed") {
    // The password WAS changed and the customer was not told. The
    // throttle is released so they can immediately try again rather
    // than being locked out for fifteen minutes holding a dead
    // credential — the one case where clearing it is the safe move.
    await store.del(throttleKey(addr)).catch(() => {});
    return { outcome: "send_failed" };
  }
  return { outcome: "no_account" };
}
