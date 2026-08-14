// =============================================================
// Marine Intelligence Weekly — Route protection policy
// File: api/_lib/routes.js
//
// ONE definition of "what does this URL require", shared by
// middleware.js and the security tests. Ordered, first match wins,
// most specific first.
//
// Every rule below was derived by inspecting the actual files, not
// by assuming from folder names. Findings that shaped this table:
//
//  * Every .html under /meoclass1/ carries noindex,nofollow — none
//    of it is intended to be publicly readable, so there is no
//    "free page" exception to carve out.
//  * /meoclass1/pastpapers/ holds the built Written papers (e.g.
//    QP2601.html, 512KB of complete solved answers). That is the
//    SOLVED_QP product, sitting under the Oral product's folder for
//    historical build reasons. Mapping it to ORAL_QB_NOTES would
//    hand the entire ₹1,500 Written library to every Oral customer.
//    It therefore requires SOLVED_QP, overriding the parent rule.
//  * /meoclass1/oralnotes/ is Oral product content and also hosts
//    the approved January Written promo — Oral entitlement, by
//    Founder decision, is exactly what should open that.
// =============================================================

import { trialGrantsAccess } from "./trial.js";
import { grantAllowsAccess, grantHasLapsed } from "./grants.js";

export const ROUTE_RULES = [
  // --- Written product, customer delivery surface ---
  { prefix: "/solvedQP/", requires: "SOLVED_QP" },

  // --- Written product, internal/review build output ---
  // More specific than /meoclass1/ and MUST come first.
  { prefix: "/meoclass1/pastpapers/", requires: "SOLVED_QP" },

  // --- Oral product ---
  { prefix: "/meoclass1/oralnotes/", requires: "ORAL_QB_NOTES" },
  { prefix: "/meoclass1/", requires: "ORAL_QB_NOTES" },
];

// Paths that must stay reachable with no session at all.
// /SQ/ is the public storefront, samples and login surface.
export const PUBLIC_PREFIXES = ["/SQ/", "/api/", "/assets/"];

/**
 * @returns {string|null} required entitlement, or null if public.
 */
export function requiredEntitlementForPath(pathname) {
  const p = normalise(pathname);

  for (const pub of PUBLIC_PREFIXES) {
    if (p.startsWith(pub)) return null;
  }

  for (const rule of ROUTE_RULES) {
    // Match the prefix, and also the bare directory with no slash
    // (/solvedQP -> /solvedQP/) so a redirect can't slip past.
    if (p.startsWith(rule.prefix) || p === rule.prefix.replace(/\/$/, "")) {
      return rule.requires;
    }
  }
  return null;
}

/**
 * The authorization decision itself, as a pure function.
 *
 * middleware.js does the I/O (read cookie, verify HMAC, ask Redis) and
 * then calls this with what it found. Keeping the DECISION separate
 * from the FETCH means the deny/allow matrix can be proven offline,
 * exactly as it will run at the edge — no Vercel deployment required
 * to know that "no entitlement" denies.
 *
 * Every branch fails CLOSED: anything not explicitly allowed denies.
 *
 * @param {object}  i
 * @param {string}  i.pathname
 * @param {boolean} i.configured   secret + Redis credentials present
 * @param {object|null} i.payload  verified token payload, or null
 * @param {*}       i.sessionScore ZSCORE result (null ⇒ not a live session)
 * @param {*}       i.entitled     HGET result ("1" ⇒ owns the product)
 * @param {*}       i.trialExpiry  HGET on miw:trial:<email> — epoch seconds,
 *                                 or null/undefined if no trial was ever taken
 * @param {number}  [i.now]        server time in epoch SECONDS. Injectable so
 *                                 the expiry boundary can be tested exactly;
 *                                 never supplied by the client.
 * @returns {{allow: boolean, reason: string, required: string|null}}
 */
export function authorizeRequest({
  pathname, configured, payload, sessionScore, entitled,
  trialExpiry = null, now = Math.floor(Date.now() / 1000),
}) {
  const required = requiredEntitlementForPath(pathname);

  // Public surface — storefront, samples, login, API.
  if (!required) return { allow: true, reason: "public", required: null };

  // A missing secret or unreachable auth store must never serve paid
  // bytes "because the check could not run".
  if (!configured) return { allow: false, reason: "misconfigured", required };

  // No cookie, bad signature, expired, or forged.
  if (!payload) return { allow: false, reason: "nosession", required };

  // Signature valid, but this session id is no longer one of the
  // account's live sessions (retired by a third login, or logged out).
  if (sessionScore === null || sessionScore === undefined) {
    return { allow: false, reason: "evicted", required };
  }

  // Authenticated, live session — but does the account own THIS product?
  //
  // PAID IS CHECKED FIRST, AND THAT ORDER IS THE POLICY.
  // A purchase must never be weakened by anything a trial did or
  // failed to do, so a customer who owns the product is allowed here
  // without the trial row being read at all. It follows that a
  // candidate who buys DURING a trial simply becomes a customer — the
  // trial's expiry stops mattering the moment the entitlement lands,
  // with no conversion step and nothing to unwind.
  //
  // "Owns" now means "1" (grandfathered, never expires) OR a future
  // expiry stamp. grantAllowsAccess() compares the "1" as a STRING
  // before any arithmetic — see the trap note in grants.js, because the
  // arithmetic reading of "1" is 1970 and would lock out every
  // pre-August-2026 customer at once.
  if (grantAllowsAccess(entitled, now)) {
    return { allow: true, reason: "ok", required };
  }

  // Not owned, or owned and lapsed. A running trial is a real,
  // server-side grant of the full product — same routes, same bytes, no
  // crippled copy.
  //
  // EVERY LIVE GRANT IS CHECKED BEFORE ANY DENIAL IS CHOSEN.
  // This branch sits above the lapsed-customer branch on purpose. A
  // candidate whose paid year has run out but who never spent their
  // free trial can still start it, and when they do it must let them
  // in — the alternative is denying someone who is holding a valid,
  // unexpired grant, because of a DIFFERENT grant that ran out. The
  // ordering below is therefore: live paid, live trial, then the most
  // useful thing to say to someone with neither.
  if (trialGrantsAccess(trialExpiry, now)) {
    return { allow: true, reason: "trial", required };
  }

  // Paid once, term run out. Distinguished from "never bought" and from
  // "trial ended": this is a lapsed CUSTOMER, and the right thing to
  // show them is a renewal, not a first-time sales pitch.
  if (grantHasLapsed(entitled, now)) {
    return { allow: false, reason: "expired", required };
  }

  // Denied. Distinguish "your trial is over" from "you never had
  // access", because those are different sentences to the candidate
  // and different next actions. Any non-empty row means a trial was
  // taken and is not currently running.
  if (trialExpiry !== null && trialExpiry !== undefined && trialExpiry !== "") {
    return { allow: false, reason: "trialexpired", required };
  }

  return { allow: false, reason: "noentitlement", required };
}

function normalise(pathname) {
  let p = String(pathname || "/");
  // Defensive: collapse traversal and duplicate slashes before matching,
  // so /meoclass1/../solvedQP/x or //solvedQP/x cannot dodge a rule.
  p = p.replace(/\/{2,}/g, "/");
  const parts = [];
  for (const seg of p.split("/")) {
    if (seg === "..") parts.pop();
    else if (seg !== "." ) parts.push(seg);
  }
  p = parts.join("/") || "/";
  if (!p.startsWith("/")) p = "/" + p;
  return p;
}
