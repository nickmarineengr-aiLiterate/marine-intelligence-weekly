// =============================================================
// Marine Intelligence Weekly — Credential rotation (incident response)
// File: api/_lib/rotation.js
//
// WHY THIS EXISTS
// ---------------
// A historical commit in this repository's PUBLIC git history carried
// customer credentials in plaintext. Deleting the blob would not undo
// that: anyone who cloned the repository at any point holds a copy.
// The credentials must therefore be treated as PERMANENTLY compromised,
// and the only real remedy is to make them stop working.
//
// `api/_lib/session.js` still verifies a legacy plaintext record, so
// every exposed password is currently a working password. Rotation is
// what closes that, and removing the legacy verify branch is only safe
// AFTER rotation — otherwise a customer whose record was never upgraded
// is locked out of a product they paid for.
//
// WHAT ROTATION MUST DO, ALL FOUR OR NONE
//   1. replace the stored credential with a hash of a fresh, random one
//   2. revoke every live session, or an attacker already inside stays in
//   3. leave miw:ent:<email> untouched — access paid for is access kept
//   4. deliver the new credential to the customer exactly once, by email
//
// This module is PURE POLICY with every external effect injected. The
// operator CLI in tools/security/rotate_credentials.mjs binds it to the
// real Redis and SMTP; tools/security/rotation.test.mjs binds it to an
// in-memory double, which is how the whole path is rehearsed without a
// real customer and without production credentials.
//
// THE PLAINTEXT RULE
// ------------------
// A generated password exists in exactly two places: this process's
// memory, and the body of one email. It is never returned to a caller
// that logs, never printed, and never written to disk. `rotateAccount`
// deliberately returns no password field — see the return shape below.
// =============================================================

import crypto from "crypto";
import { hashPassword } from "./session.js";
import { userKey } from "./entitlements.js";
import { sessionsKey, legacySessionKey } from "./sessions.js";

/**
 * Ambiguity-free alphabet. The customer retypes this from an email on
 * a phone, so 0/O and 1/l/I are excluded — a support round-trip caused
 * by a misread character is a worse outcome than two fewer bits.
 * 32 symbols x 16 positions = 80 bits of entropy.
 */
const ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
export const PASSWORD_LENGTH = 16;

/**
 * crypto.randomInt, not randomBytes % len. The modulo of a byte over a
 * 32-symbol alphabet happens to be unbiased here, but it stops being
 * unbiased the moment somebody edits ALPHABET — so the unbiased call is
 * used unconditionally rather than relying on a coincidence of length.
 */
export function generatePassword(length = PASSWORD_LENGTH) {
  let out = "";
  for (let i = 0; i < length; i++) out += ALPHABET[crypto.randomInt(ALPHABET.length)];
  return out;
}

/**
 * What form is this account's stored credential in?
 *
 *   "absent"           no credential record — nothing to rotate
 *   "hashed"           already a sha256$salt$digest — safe as stored
 *   "legacy_plaintext" the exposed form — REQUIRES ROTATION
 *
 * Mirrors the discrimination in session.js#verifyPassword exactly. If
 * that prefix test ever changes, this one must change with it, which is
 * why both are a single `startsWith("sha256$")` and nothing cleverer.
 */
export function classifyStored(stored) {
  if (stored === null || stored === undefined || stored === "") return "absent";
  return String(stored).startsWith("sha256$") ? "hashed" : "legacy_plaintext";
}

/**
 * "Already safe" means the stored form cannot be replayed from the
 * leaked blob. A hashed record qualifies even though the customer's
 * password is unchanged, because the leak exposed STORED VALUES.
 *
 * Note the deliberate limit of this, stated plainly rather than papered
 * over: a customer whose record was hash-upgraded on login still types
 * a password that appeared in public history. Rotation is offered for
 * those accounts too — see `includeHashed` on rotateAccount's caller.
 */
export function needsRotation(stored) {
  return classifyStored(stored) === "legacy_plaintext";
}

export class RotationError extends Error {
  constructor(message, code) {
    super(message);
    this.name = "RotationError";
    this.code = code;
  }
}

/**
 * Rotate ONE account.
 *
 * ORDERING IS THE WHOLE DESIGN. The credential is replaced FIRST, then
 * sessions are revoked, then the email is sent:
 *
 *   - credential before sessions: if we revoked first and then failed to
 *     write, the old password would still work and we would merely have
 *     signed the customer out. Harmless, but no remediation happened.
 *   - sessions before email: a live session is the compromised access.
 *     It must be gone before we tell anyone anything.
 *   - email last: it is the only step we cannot roll back, and it is
 *     the only step whose failure leaves a RECOVERABLE state — the
 *     account is secure, the customer simply has not been told yet.
 *     That case is reported as "rotated_email_failed", never as success.
 *
 * @param {object} o
 * @param {string} o.email
 * @param {object} o.store    {get, set, del} over the credential/session keys
 * @param {function} o.sendMail
 * @param {function} [o.buildEmail]  (email, password) => message
 * @param {function} [o.makePassword]
 * @returns {Promise<{email, status, sessionsRevoked}>}
 *          status: "rotated" | "rotated_email_failed" | "skipped_absent"
 *                | "skipped_already_hashed"
 *          NOTE: no password field. Nothing downstream may log it.
 */
export async function rotateAccount({
  email,
  store,
  sendMail,
  buildEmail,
  makePassword = generatePassword,
  includeHashed = false,
}) {
  const addr = String(email).toLowerCase().trim();
  if (!addr) throw new RotationError("No email supplied", "no_email");

  const stored = await store.get(userKey(addr));
  const form = classifyStored(stored);

  // Nothing to rotate. Reported, not silently counted as success —
  // "affected" and "remediated" must never be conflated in the tally.
  if (form === "absent") return { email: addr, status: "skipped_absent", sessionsRevoked: 0 };
  if (form === "hashed" && !includeHashed) {
    return { email: addr, status: "skipped_already_hashed", sessionsRevoked: 0 };
  }

  // ---- 1. Replace the credential ----
  const password = makePassword();
  await store.set(userKey(addr), hashPassword(password));

  // Read back and re-verify the invariant rather than trusting the write.
  // A store that silently no-ops would otherwise let us report a rotation
  // that never happened — the single worst failure this tool could have.
  const after = await store.get(userKey(addr));
  if (classifyStored(after) !== "hashed") {
    throw new RotationError(`Credential did not persist as a hash for ${addr}`, "write_failed");
  }

  // ---- 2. Revoke every live session ----
  // Both keys: the bounded sorted set AND the pre-V2 single-session key,
  // because a pre-V2 remnant would otherwise outlive the rotation.
  const live = await store.countSessions(addr);
  await store.del(sessionsKey(addr));
  await store.del(legacySessionKey(addr));

  // ---- 3. Tell the customer, exactly once ----
  try {
    await sendMail(buildEmail(addr, password));
  } catch (e) {
    // The account IS secure. Only the notification failed, and the
    // password is now unrecoverable by design — the operator must
    // re-run rotation for this account to issue a fresh one.
    return {
      email: addr,
      status: "rotated_email_failed",
      sessionsRevoked: live,
      error: e.message,
    };
  }

  return { email: addr, status: "rotated", sessionsRevoked: live };
}

/** Masked form for every operator-facing line of output. */
export function maskEmail(email) {
  const [u, d] = String(email).split("@");
  if (!d) return "***";
  return `${u.slice(0, 2)}***@${d}`;
}
