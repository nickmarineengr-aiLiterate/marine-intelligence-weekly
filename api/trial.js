// =============================================================
// Marine Intelligence Weekly — Free trial activation
// File: api/trial.js
// Endpoints:
//   GET  /api/trial                    -> who am I, what do I own,
//                                         and what trial state is each
//                                         product in?
//   POST /api/trial {product:"..."}    -> start the trial for ONE product
//
// The trial clock starts HERE and nowhere else.
//
// Not on page load, not on sign-in, not on a marketing click, and not
// when middleware bounces someone. A candidate spends their one trial
// only by deliberately POSTing to this endpoint, which the UI does only
// from an explicit "Start free trial" button.
//
// Authentication is the SAME session the rest of the site uses — the
// HttpOnly miw_session cookie, verified by signature and then checked
// against the account's live session set. There is no second login, no
// trial-only token, and no anonymous grant: a trial is attached to an
// account, which is what makes "one per candidate" enforceable and what
// stops clearing a browser from producing a fresh one.
//
// Policy (durations, the Independence Day rule, state derivation) lives
// in api/_lib/trial.js as pure functions. This file is I/O and nothing
// else, so the rules can be proven offline.
// =============================================================

import { parseCookies, verifySessionToken, SESSION_COOKIE } from "./_lib/session.js";
import { isActiveSession, getEntitlements, getEntitlementDetail } from "./_lib/entitlements.js";
import { redisCmd } from "./_lib/redis.js";
import { ALL_ENTITLEMENTS } from "./_lib/products.js";
import {
  trialKey, trialOffer, trialExpiryFor, isTrialProduct, TRIAL_ACTIVE,
} from "./_lib/trial.js";

/** Read every trial field for an account in one command. */
async function readTrials(email) {
  const data = await redisCmd(["HGETALL", trialKey(email)]);
  const raw = data.result;

  // Upstash returns HGETALL as a flat [k,v,k,v] array. Same shape
  // handling as getEntitlements() — see api/_lib/entitlements.js.
  const held = {};
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
  } else if (raw && typeof raw === "object") {
    Object.assign(held, raw);
  }
  return held;
}

/** Build the full candidate-facing picture from server truth only. */
function buildOffers({ entitlements, trials, nowMs }) {
  const offers = {};
  for (const product of ALL_ENTITLEMENTS) {
    if (!isTrialProduct(product)) continue;
    offers[product] = trialOffer(product, {
      owned: entitlements[product] === true,
      raw: trials[product],
      nowMs,
    });
  }
  return offers;
}

/**
 * Resolve the caller to a live account, or send the standard
 * unauthenticated body. Returns null when it has already responded.
 */
async function requireSession(req, res) {
  const cookies = parseCookies(req.headers.cookie);
  const payload = verifySessionToken(cookies[SESSION_COOKIE]);
  if (!payload) {
    res.status(200).json({ authenticated: false, offers: {}, entitlements: {} });
    return null;
  }
  // A valid signature is not enough — the session must still be one of
  // the account's live sessions, exactly as /api/session requires.
  if (!(await isActiveSession(payload.e, payload.s))) {
    res.status(200).json({
      authenticated: false, reason: "evicted", offers: {}, entitlements: {},
    });
    return null;
  }
  return payload;
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://marineintelligenceweekly.com");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Cache-Control", "no-store, private");
  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method !== "GET" && req.method !== "POST") return res.status(405).end();

  const payload = await requireSession(req, res);
  if (!payload) return;

  const email = String(payload.e).toLowerCase();

  // ---------------------------------------------------------
  // GET — report state. Never mutates, so a candidate can read
  // the offer as often as they like without spending it.
  // ---------------------------------------------------------
  if (req.method === "GET") {
    const nowMs = Date.now();
    const [entitlements, access, trials] = await Promise.all([
      getEntitlements(email), getEntitlementDetail(email), readTrials(email),
    ]);
    return res.status(200).json({
      authenticated: true,
      email,
      entitlements,
      access,
      offers: buildOffers({ entitlements, trials, nowMs }),
      serverTime: Math.floor(nowMs / 1000),
    });
  }

  // ---------------------------------------------------------
  // POST — activate. The one mutating path in the trial system.
  // ---------------------------------------------------------
  const body = req.body || {};
  const product = String(body.product || "").trim();

  if (!isTrialProduct(product)) {
    return res.status(400).json({ error: "Unknown product" });
  }

  const entitlements = await getEntitlements(email);

  // Already a customer. Refuse rather than burn their trial on a
  // product they have already paid for — if they later want the trial
  // it will still be there, and meanwhile they simply have access.
  if (entitlements[product] === true) {
    const trials = await readTrials(email);
    return res.status(200).json({
      authenticated: true,
      email,
      started: false,
      reason: "owned",
      offer: trialOffer(product, { owned: true, raw: trials[product], nowMs: Date.now() }),
    });
  }

  // The duration is decided HERE, from this server's clock, at the
  // instant of activation — which is what makes the Independence Day
  // window a property of when the candidate pressed the button rather
  // than of anything the browser claimed.
  const nowMs = Date.now();
  const expiry = trialExpiryFor(product, nowMs);

  // ATOMIC ONE-SHOT. HSETNX writes only if the field is absent, so
  // exactly one caller can ever start this account's trial for this
  // product. A double tap, two devices, or a replayed request all
  // resolve to the same single grant with no race window.
  const write = await redisCmd(["HSETNX", trialKey(email), product, String(expiry)]);
  const created = write.result === 1 || write.result === "1";

  // Re-read rather than assume. If HSETNX lost, the stored value is
  // someone else's earlier grant and IT is the truth, not `expiry`.
  const trials = await readTrials(email);
  const offer = trialOffer(product, {
    owned: false, raw: trials[product], nowMs: Date.now(),
  });

  if (created) {
    return res.status(200).json({
      authenticated: true, email, started: true, offer,
    });
  }

  // Lost the race, or the trial was spent long ago. Both are "you
  // already used this", and the offer body says which.
  return res.status(offer.status === TRIAL_ACTIVE ? 200 : 409).json({
    authenticated: true,
    email,
    started: false,
    reason: offer.status === TRIAL_ACTIVE ? "already_active" : "already_used",
    offer,
  });
}
