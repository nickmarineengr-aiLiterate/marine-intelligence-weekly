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
//   field === "1"       -> PERPETUAL  Candidate-Lifecycle; no clock
//   field === "<epoch>" -> ACTIVE until that second, then EXPIRED
//   field === "passed:<closedAt>:<prior>"
//                       -> PASSED_CLOSED  lifecycle closed by the Founder
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
// exactly what it always meant: no clock-based expiry.
//
// ─────────────────────────────────────────────────────────────
// WHAT "1" DOES AND DOES NOT MEAN (Founder decision, 16 Aug 2026)
//
// "1" is a TECHNICAL SHAPE — no clock-based expiry — and nothing more.
// The COMMERCIAL term those customers hold is Candidate-Lifecycle
// Access: access for the duration of their MEO Class I preparation,
// which the Founder may close once MIW has reliable confirmation that
// they passed. The two are not the same statement, and reading "1" as
// "access until the purchaser dies" was always an over-reading of an
// implementation detail.
//
// PASSED_CLOSED is how that closure is recorded. It is a value in the
// SAME field rather than a separate miw:member_status:<email> key, for
// three reasons that all point the same way:
//
//   ONE READER.  Every access decision on the platform — the edge
//                middleware, /api/session, the pay page, the admin
//                tool — already ends up in grantAllowsAccess() with a
//                value from this field. A second key would be a second
//                source of truth that can drift from the first, and the
//                last time this repo held two opinions about an
//                entitlement the weaker one would have handed the whole
//                Written library to every Oral customer.
//
//   ONE HOP.     Authorising a request is one HGET at the edge. Reading
//                a status key too would double that on the hottest path
//                in the system, to answer a question the field it
//                already fetched can answer by itself.
//
//   FAILS CLOSED. "passed:..." is not numeric, so code that predates
//                this change reads it as corrupt and DENIES. A closure
//                cannot be defeated by a stale deployment.
//
// The prior value is carried inside the string, so closing a lifecycle
// grant PRESERVES what the customer held rather than erasing it. That
// is what makes `reopen-candidate` exact rather than a guess, and it
// keeps "purchased, then passed, then closed" distinguishable from
// "never purchased" — which is a field that was never set at all.
// ─────────────────────────────────────────────────────────────
//
// Pure: no imports, no I/O. Runs unchanged in Edge middleware and in the
// Node functions, and the whole policy is provable offline.
// =============================================================

export const GRANT_NONE = "none";
export const GRANT_PERPETUAL = "perpetual";
export const GRANT_ACTIVE = "active";
export const GRANT_EXPIRED = "expired";
export const GRANT_PASSED_CLOSED = "passed_closed";

/** The literal stored for a grant with no clock-based expiry. */
export const PERPETUAL = "1";

/** Marks a Candidate-Lifecycle grant the Founder has closed. */
export const PASSED_PREFIX = "passed:";

/** True for the stored shape of a Candidate-Lifecycle grant. */
export function isLifecycleValue(raw) {
  return raw === PERPETUAL || raw === 1;
}

/** True for a value recording a closed lifecycle. */
export function isPassedValue(raw) {
  return typeof raw === "string" && raw.startsWith(PASSED_PREFIX);
}

/**
 * Split "passed:<closedAt>:<prior>" apart.
 *
 * `prior` may itself contain nothing surprising — it is either "1" or a
 * digit string — but it is recovered with the REST of the string rather
 * than the second segment, so a future value carrying a colon still
 * round-trips through mark-passed → reopen-candidate unchanged.
 */
export function parsePassedValue(raw) {
  if (!isPassedValue(raw)) return null;
  const rest = raw.slice(PASSED_PREFIX.length);
  const cut = rest.indexOf(":");
  if (cut === -1) return null;
  const closedAt = Number(rest.slice(0, cut));
  const prior = rest.slice(cut + 1);
  if (!Number.isFinite(closedAt) || closedAt <= 0 || prior === "") return null;
  return { closedAt, prior };
}

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
  if (isLifecycleValue(raw)) {
    return { status: GRANT_PERPETUAL, expires: null, perpetual: true };
  }

  // Before the arithmetic, because "passed:..." is not a number and the
  // corrupt-value branch below would otherwise swallow it into EXPIRED —
  // which denies correctly but loses the reason and the prior value.
  if (isPassedValue(raw)) {
    const parsed = parsePassedValue(raw);
    return {
      status: GRANT_PASSED_CLOSED,
      expires: null,
      perpetual: false,
      closedAt: parsed ? parsed.closedAt : null,
      prior: parsed ? parsed.prior : null,
    };
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

/**
 * True only for a grant that once existed and has now RUN OUT — a clock
 * reached its end.
 *
 * A closed lifecycle is deliberately NOT "lapsed". The surfaces that ask
 * this question offer a renewal and print the end date beside it, and a
 * closure has no end date to print. More to the point, a member's exam
 * result is private (Founder policy): the pay page must not turn it into
 * a visible "your access ended" banner. A closed member simply sees the
 * ordinary product offer, like anyone else without access.
 */
export function grantHasLapsed(raw, nowSeconds) {
  return grantState(raw, nowSeconds).status === GRANT_EXPIRED;
}

/**
 * The value to store when the Founder records that a member passed.
 *
 * Returns null when the grant is NOT a Candidate-Lifecycle one, and that
 * null is the whole product-separation guarantee: a dated grant, an
 * absent grant and an already-closed grant are all left exactly as they
 * are. Marking a member passed can only ever move PERPETUAL →
 * PASSED_CLOSED, so a customer's separately-bought one-year Written
 * entitlement cannot be collateral damage of closing their legacy Oral
 * one. The caller reports the null rather than writing anything.
 */
export function markPassedValue(existing, nowMs) {
  if (!isLifecycleValue(existing)) return null;
  return `${PASSED_PREFIX}${Math.floor(nowMs / 1000)}:${PERPETUAL}`;
}

/**
 * The value to restore when a closure was a mistake.
 *
 * Returns the exact value held before closure — recovered from the
 * record, not reconstructed — or null if this grant was never closed.
 * Restoring by reconstruction would quietly mint a perpetual grant for
 * anyone the operator named, which is why the prior value is carried in
 * the stored string in the first place.
 */
export function reopenedGrantValue(existing) {
  const parsed = parsePassedValue(existing);
  return parsed ? parsed.prior : null;
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
  if (isLifecycleValue(existing)) return PERPETUAL;
  if (termDays === null || termDays === undefined) return PERPETUAL;

  // A member whose lifecycle was closed and who then BUYS is a new
  // dated customer, not a restoration. Number("passed:...") is NaN, so
  // the base below already falls through to "now" — this is stated
  // rather than left to the arithmetic, because a closure silently
  // extending into a fresh perpetual grant would undo the closure.
  if (isPassedValue(existing)) {
    return String(Math.floor(nowMs / 1000) + Math.round(termDays * 86400));
  }

  const nowSeconds = Math.floor(nowMs / 1000);
  const current = Number(existing);
  // Renew from the later of "now" and the existing expiry, so renewing
  // early does not throw away the time already paid for.
  const base = Number.isFinite(current) && current > nowSeconds ? current : nowSeconds;
  return String(base + Math.round(termDays * 86400));
}
