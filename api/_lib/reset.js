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

import { rotateAccount, generatePassword } from "./rotation.js";
import { userKey } from "./entitlements.js";
import { hashPassword } from "./session.js";

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

// =============================================================
// ACCOUNT CREATION FOR TRIAL CANDIDATES
//
// WHY THIS EXISTS AT ALL
// ----------------------
// Before the free trial, an MIW account came into being in exactly one
// place: fulfilPayment(), after Razorpay captured money. There was no
// self-serve signup, and there did not need to be — everyone with an
// account had bought something.
//
// A trial has to be attached to an account, because that is the only
// identity the system can hold on to. Cookies, localStorage and device
// ids are all things the candidate can throw away, and a trial that a
// candidate can restart by opening an incognito window is not a trial.
// So a candidate who has never bought anything needs a way to obtain a
// credential without paying.
//
// WHY IT IS THE SAME DOOR, NOT A NEW ONE
// --------------------------------------
// This is deliberately modelled on requestReset() above and inherits
// all three of its safety properties, for the same reasons:
// no enumeration, throttled, one atomic claim per address per window.
// It shares the hashing, the password generator and the mail path with
// the purchase flow, so there is still exactly ONE definition of what
// an MIW credential is.
//
// THE ONE RULE THAT MAKES IT SAFE TO EXPOSE
// -----------------------------------------
// IT WILL NOT TOUCH AN EXISTING ACCOUNT. If the address already has a
// credential, this function does nothing at all — no rotation, no
// email, no session revocation. Without that rule an anonymous form
// that "creates an account" would be a password reset for any customer
// on earth, which is precisely the attack requestReset() throttles
// itself to avoid. A customer who has genuinely forgotten their
// password uses the reset link; that path already exists and already
// revokes sessions.
//
// The write is SET NX, so even if two requests somehow got past the
// throttle simultaneously, only one credential can ever be created and
// the loser sends no mail.
// =============================================================

/** One account-creation attempt per address per fifteen minutes. */
export const SIGNUP_THROTTLE_SECONDS = 15 * 60;

export const signupThrottleKey = (email) =>
  `miw:signup_throttle:${String(email).toLowerCase().trim()}`;

/**
 * The single sentence every caller gets back, whatever happened.
 *
 * It has to stay true in all five cases — created, throttled, address
 * already has an account, malformed, and internal failure — AND it has
 * to tell an existing customer what to do instead, without confirming
 * to a stranger that they are one. Naming both paths unconditionally
 * is what lets it do both: the reader learns which sentence applies to
 * them from what lands in their inbox, and an attacker learns nothing.
 */
export const SIGNUP_RESPONSE =
  "Check your email. If that address is new to MIW, a password is on its way. " +
  "If it already has an account, use “Email me a new one” on the sign-in page " +
  "to get a fresh password. Please also check your spam folder.";

/**
 * Create an account for an address that does not have one, and email
 * the credential.
 *
 * @param {object} o
 * @param {string} o.email
 * @param {object} o.store  {get, createNX(key,value) -> bool, claim(key,ttl) -> bool, del}
 * @param {function} o.sendMail
 * @param {function} o.buildEmail  (email, password) -> message
 * @param {function} [o.makePassword]  test seam only
 * @returns {Promise<{outcome: string}>}
 *   LOGS AND TESTS ONLY, never returned to the client:
 *   "created" | "throttled" | "existing_account" | "invalid_email"
 *   | "race_lost" | "send_failed"
 */
export async function requestTrialAccount({
  email, store, sendMail, buildEmail, makePassword,
}) {
  const addr = String(email || "").toLowerCase().trim();

  if (!addr || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(addr)) {
    return { outcome: "invalid_email" };
  }

  // Throttle BEFORE the existence check, for the timing reason spelled
  // out in requestReset(): checking first would make "no account" fast
  // and "throttled" slow, and the difference is an enumeration oracle.
  const claimed = await store.claim(signupThrottleKey(addr), SIGNUP_THROTTLE_SECONDS);
  if (!claimed) return { outcome: "throttled" };

  const existing = await store.get(userKey(addr));
  if (existing) return { outcome: "existing_account" };

  const password = (makePassword || generatePassword)();

  // SET NX — durable, no TTL. Returns false if anything raced us here,
  // in which case that other request owns the credential and this one
  // must not send a password that is not the stored one.
  const created = await store.createNX(userKey(addr), hashPassword(password));
  if (!created) return { outcome: "race_lost" };

  try {
    await sendMail(buildEmail(addr, password));
  } catch (e) {
    // The account exists but the candidate never received the password.
    // Release the throttle so they can retry immediately — on the retry
    // the address now HAS an account, so they will be pointed at the
    // reset link, which can deliver a working credential.
    await store.del(signupThrottleKey(addr)).catch(() => {});
    return { outcome: "send_failed" };
  }

  return { outcome: "created" };
}
