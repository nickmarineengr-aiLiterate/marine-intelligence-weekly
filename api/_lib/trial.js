// =============================================================
// Marine Intelligence Weekly — Free trial policy
// File: api/_lib/trial.js
//
// A trial is a TEMPORARY ENTITLEMENT, not a second product and not a
// second security mechanism. Everything else — session, device cap,
// route policy, middleware — is reused unchanged. The only new fact
// in the system is "this account may read this product until T".
//
// SCHEMA
// ------
//   miw:trial:<email>        Redis HASH
//       field ORAL_QB_NOTES = "<expiry epoch seconds>"
//       field SOLVED_QP     = "<expiry epoch seconds>"
//
// ONE FIELD CARRIES ALL THREE STATES:
//
//     field absent          -> AVAILABLE   (never taken)
//     value  > now          -> ACTIVE      (running)
//     value <= now          -> EXPIRED     (taken, and over)
//
// WHY AN EXPIRY RATHER THAN A FLAG PLUS A TIMESTAMP
//   Two fields can disagree. One cannot. There is no state where the
//   store says "used" but not "when", or "expires at T" but "unused".
//
// WHY HSETNX
//   The write is `HSETNX miw:trial:<email> <product> <expiry>`, which
//   succeeds for exactly ONE caller and is a no-op for every caller
//   after it. That is what makes "one trial per account per product"
//   true rather than merely intended — two simultaneous taps, two
//   devices, or a replayed request all collapse to a single grant, with
//   no read-modify-write window to race.
//
// WHY THE RECORD IS NEVER DELETED AND CARRIES NO TTL
//   The expired row IS the proof of consumption. Expiring the key
//   would silently hand the account a fresh trial, so clearing cookies,
//   clearing localStorage, using a different browser, or signing out
//   and back in cannot restart a trial. The clock is a server
//   timestamp; the browser's clock is never consulted.
//
// PER-PRODUCT INDEPENDENCE
//   Separate HASH FIELDS, exactly as miw:ent:<email> does it. Taking
//   the Oral trial writes ORAL_QB_NOTES and leaves SOLVED_QP absent,
//   so the Written trial is still available. One never consumes the
//   other.
//
// PAID ALWAYS WINS
//   Nothing here can downgrade a purchase. authorizeRequest() checks
//   the entitlement hash FIRST and only consults a trial when the
//   account does not own the product, so an expired trial is invisible
//   to a paying customer. A purchase made mid-trial simply makes the
//   trial irrelevant — no conversion step, nothing to clean up.
//
// This module is PURE: no I/O, no imports beyond the product
// vocabulary, so it runs unchanged in the Node functions and in Edge
// middleware, and the whole policy can be proven offline.
// =============================================================

import { ALL_ENTITLEMENTS } from "./products.js";

export const trialKey = (email) => `miw:trial:${String(email).toLowerCase().trim()}`;

// -------------------------------------------------------------
// Durations — Founder-frozen.
// -------------------------------------------------------------

/** Normal permanent trial length, per product, in hours. */
export const TRIAL_HOURS = {
  ORAL_QB_NOTES: 12,
  SOLVED_QP: 12,
};

/**
 * INDEPENDENCE DAY CAMPAIGN.
 *
 * A SolvedQP trial ACTIVATED on 15 August 2026, India time, runs for 24
 * hours from the moment of activation. It is not "until midnight": a
 * candidate who starts at 20:30 IST on the 15th keeps access until
 * 20:30 IST on the 16th.
 *
 * TIMEZONE RULE — read this before changing anything here.
 *
 * Eligibility is decided on the IST CALENDAR DATE of the server's
 * activation instant, because the campaign is an Indian public holiday
 * and MIW's candidates are in India. Deciding it in UTC would be wrong
 * at both ends of the day: 15 Aug 00:30 IST is still 14 Aug in UTC, and
 * 15 Aug 23:59 IST is already 15 Aug in UTC only by luck of the offset.
 * An Indian candidate celebrating on the 15th must not get 12 hours
 * because a server in another timezone disagreed about the date.
 *
 * IST is UTC+05:30 with no daylight saving and no historical change in
 * the relevant period, so the offset is a constant and needs no
 * timezone database. We shift the instant by +5h30m and read the UTC
 * calendar date of the shifted instant — that is the IST wall-clock
 * date, computed deterministically from a server timestamp.
 *
 * The window is a single named date rather than a start/end pair so
 * there is nothing to forget to switch off: on 16 August the comparison
 * simply stops matching and SolvedQP returns to 12 hours by itself.
 */
export const INDEPENDENCE_DAY = {
  product: "SOLVED_QP",
  istDate: "2026-08-15",
  hours: 24,
  label: "Independence Day Open Access",
};

/** IST is UTC+05:30. Fixed offset — no DST, no timezone database. */
export const IST_OFFSET_MINUTES = 330;

/**
 * The IST calendar date of an instant, as "YYYY-MM-DD".
 * @param {number} nowMs epoch milliseconds (server clock)
 */
export function istDateString(nowMs) {
  return new Date(nowMs + IST_OFFSET_MINUTES * 60000).toISOString().slice(0, 10);
}

/** Is this product, activated now, inside the Independence Day window? */
export function isIndependenceDayActivation(product, nowMs) {
  return product === INDEPENDENCE_DAY.product &&
         istDateString(nowMs) === INDEPENDENCE_DAY.istDate;
}

/**
 * How many hours a trial started RIGHT NOW would run for.
 * @returns {number|null} null if the product has no trial offer.
 */
export function trialDurationHours(product, nowMs) {
  if (!TRIAL_HOURS[product]) return null;
  if (isIndependenceDayActivation(product, nowMs)) return INDEPENDENCE_DAY.hours;
  return TRIAL_HOURS[product];
}

/** The expiry a trial started right now would be stamped with. */
export function trialExpiryFor(product, nowMs) {
  const hours = trialDurationHours(product, nowMs);
  if (hours === null) return null;
  return Math.floor(nowMs / 1000) + hours * 3600;
}

export function isTrialProduct(product) {
  return ALL_ENTITLEMENTS.includes(product) && Boolean(TRIAL_HOURS[product]);
}

// -------------------------------------------------------------
// State derivation
// -------------------------------------------------------------

export const TRIAL_AVAILABLE = "available";
export const TRIAL_ACTIVE = "active";
export const TRIAL_EXPIRED = "expired";

/**
 * Interpret one stored field.
 *
 * @param {*} raw            HGET result — string, number, null or undefined
 * @param {number} nowSeconds server time, epoch seconds
 * @returns {{status: string, expires: number|null, secondsRemaining: number}}
 */
export function trialState(raw, nowSeconds) {
  if (raw === null || raw === undefined || raw === "") {
    return { status: TRIAL_AVAILABLE, expires: null, secondsRemaining: 0 };
  }

  const expires = Number(raw);

  // A field that exists but does not parse means SOMETHING was written
  // here, and HSETNX will refuse to overwrite it. Calling that
  // "available" would advertise a trial the store will then decline to
  // start. Fail closed: the row exists, so the trial is spent.
  if (!Number.isFinite(expires) || expires <= 0) {
    return { status: TRIAL_EXPIRED, expires: null, secondsRemaining: 0 };
  }

  if (expires > nowSeconds) {
    return { status: TRIAL_ACTIVE, expires, secondsRemaining: expires - nowSeconds };
  }
  return { status: TRIAL_EXPIRED, expires, secondsRemaining: 0 };
}

/**
 * The single question middleware asks. Deliberately not "does a trial
 * exist" — an expired trial exists and grants nothing.
 */
export function trialGrantsAccess(raw, nowSeconds) {
  return trialState(raw, nowSeconds).status === TRIAL_ACTIVE;
}

/**
 * Everything a candidate-facing surface needs for one product, derived
 * from server truth only. `owned` short-circuits: a paying customer is
 * never shown trial state, because their trial row — taken or not — has
 * no bearing on their access.
 *
 * @returns {{product, owned, status, expires, secondsRemaining, offerHours, independenceDay}}
 *   status is one of: "owned" | "available" | "active" | "expired"
 */
export function trialOffer(product, { owned, raw, nowMs }) {
  const nowSeconds = Math.floor(nowMs / 1000);
  const state = trialState(raw, nowSeconds);
  return {
    product,
    owned: Boolean(owned),
    status: owned ? "owned" : state.status,
    expires: state.expires,
    secondsRemaining: owned ? 0 : state.secondsRemaining,
    offerHours: trialDurationHours(product, nowMs),
    independenceDay: isIndependenceDayActivation(product, nowMs),
  };
}
