// =============================================================
// Marine Intelligence Weekly — What a stored grant VALUE means
// File: api/_lib/grants.js
//
// miw:ent:<email> used to be a set of boolean flags: the field was
// present and equal to "1", or it was absent. That encoded exactly one
// product model — buy once, keep forever — and it is the model every
// existing customer bought under.
//
// From August 2026 new purchases carry a TERM. The field therefore has
// to say not just "yes" but "yes, until when", and it has to keep
// saying the old thing for everyone who came before.
//
//   field absent        -> NONE       no access, never had it
//   field === "1"       -> PERPETUAL  grandfathered; never expires
//   field === "<epoch>" -> ACTIVE until that second, then EXPIRED
//
// ─────────────────────────────────────────────────────────────
// THE TRAP. READ THIS BEFORE CHANGING ANYTHING BELOW.
//
//   Number("1") === 1, which is 1 January 1970.
//
// So the obvious implementation —
//
//     const expires = Number(raw);
//     return expires > nowSeconds;          // WRONG
//
// — reads EVERY grandfathered customer as fifty-six years expired and
// locks all of them out at once, silently, on the first request after
// deploy. There is no error, no log, nothing to notice: the gate simply
// starts denying people who paid.
//
// The "1" comparison therefore happens FIRST, as a string, before any
// arithmetic touches the value. The test suite carries a positive
// control that fails if that ordering is ever reversed.
// ─────────────────────────────────────────────────────────────
//
// WHY "1" AND NOT A MIGRATION
// A migration would have to rewrite ~100 live records to some sentinel
// like "9999999999", get every one right, and be re-run correctly if it
// half-failed. Teaching the reader that "1" means perpetual costs one
// comparison and cannot half-succeed. The old value keeps meaning
// exactly what it always meant, which is also the honest encoding: those
// customers really do hold an unlimited grant.
//
// Pure: no imports, no I/O. Runs unchanged in Edge middleware and in the
// Node functions, and the whole policy is provable offline.
// =============================================================

export const GRANT_NONE = "none";
export const GRANT_PERPETUAL = "perpetual";
export const GRANT_ACTIVE = "active";
export const GRANT_EXPIRED = "expired";

/** The literal stored for a grant that never expires. */
export const PERPETUAL = "1";

/**
 * Interpret one stored entitlement field.
 *
 * @param {*} raw            HGET result — string, number, null or undefined
 * @param {number} nowSeconds server time, epoch seconds
 * @returns {{status: string, expires: number|null, perpetual: boolean}}
 */
export function grantState(raw, nowSeconds) {
  if (raw === null || raw === undefined || raw === "") {
    return { status: GRANT_NONE, expires: null, perpetual: false };
  }

  // FIRST, and as a string. See the trap note above.
  if (raw === PERPETUAL || raw === 1) {
    return { status: GRANT_PERPETUAL, expires: null, perpetual: true };
  }

  const expires = Number(raw);

  // A field that exists but is not "1" and does not parse is corrupt.
  // Fail CLOSED — but note this is a DENY for someone who may well have
  // paid, so it is worth alerting on rather than shrugging at.
  if (!Number.isFinite(expires) || expires <= 0) {
    return { status: GRANT_EXPIRED, expires: null, perpetual: false };
  }

  if (expires > nowSeconds) {
    return { status: GRANT_ACTIVE, expires, perpetual: false };
  }
  return { status: GRANT_EXPIRED, expires, perpetual: false };
}

/** The single question the gate asks of a paid entitlement. */
export function grantAllowsAccess(raw, nowSeconds) {
  const s = grantState(raw, nowSeconds).status;
  return s === GRANT_PERPETUAL || s === GRANT_ACTIVE;
}

/** True only for a grant that once existed and has now run out. */
export function grantHasLapsed(raw, nowSeconds) {
  return grantState(raw, nowSeconds).status === GRANT_EXPIRED;
}

/**
 * The value to store for a purchase.
 *
 * @param {number|null} termDays  null ⇒ perpetual (the grandfathered shape)
 * @param {number} nowMs
 */
export function grantValueFor(termDays, nowMs) {
  if (termDays === null || termDays === undefined) return PERPETUAL;
  return String(Math.floor(nowMs / 1000) + Math.round(termDays * 86400));
}

/**
 * Extending an existing grant must never SHORTEN it.
 *
 * A renewal should add a term to whatever the customer already holds,
 * and a perpetual holder who buys again stays perpetual — otherwise a
 * grandfathered customer who bought the other product, or renewed by
 * mistake, would be downgraded to a dated licence by their own payment.
 */
export function extendedGrantValue(existing, termDays, nowMs) {
  if (existing === PERPETUAL || existing === 1) return PERPETUAL;
  if (termDays === null || termDays === undefined) return PERPETUAL;

  const nowSeconds = Math.floor(nowMs / 1000);
  const current = Number(existing);
  // Renew from the later of "now" and the existing expiry, so renewing
  // early does not throw away the time already paid for.
  const base = Number.isFinite(current) && current > nowSeconds ? current : nowSeconds;
  return String(base + Math.round(termDays * 86400));
}
