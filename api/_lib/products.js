// =============================================================
// Marine Intelligence Weekly — Canonical Product Catalogue
// File: api/_lib/products.js
//
// THIS FILE IS THE ONLY PLACE A PRICE IS DECIDED.
//
// The browser may DISPLAY a price. It may never CHOOSE one.
// Every server path (create-order, verify-payment, webhook) reads
// the amount from here, keyed by product + tier, and ignores any
// amount present in the request body.
//
// Files under api/_lib/ are not routed as endpoints by Vercel
// (leading underscore), so this is server-only.
// =============================================================

export const ENTITLEMENTS = {
  ORAL_QB_NOTES: "ORAL_QB_NOTES",
  SOLVED_QP: "SOLVED_QP",
};

// All known entitlement keys, in a stable order (used by the
// migration tool and the admin runbook so output is diffable).
export const ALL_ENTITLEMENTS = [
  ENTITLEMENTS.ORAL_QB_NOTES,
  ENTITLEMENTS.SOLVED_QP,
];

// -------------------------------------------------------------
// ACCESS TERM
//
// Founder decision, 14 August 2026: purchases made from now on carry a
// ONE-YEAR term. Candidates who pass in three to six months should not
// leave a live credential behind them indefinitely, and the price is
// now tied to a growing library rather than to a single payment.
//
// This is NOT retroactive and cannot be made retroactive by changing
// this number. Every existing customer holds the literal "1" in
// miw:ent:<email>, which api/_lib/grants.js reads as perpetual before
// it looks at any date. Nothing in this file can reach those records.
//
// null would mean perpetual, and is deliberately left reachable so a
// future Founder decision (a genuine lifetime SKU, a comped account)
// has an obvious lever rather than needing new code.
// -------------------------------------------------------------
export const DEFAULT_TERM_DAYS = 365;

export const PRODUCTS = {
  // -----------------------------------------------------------
  // Existing paid Oral product. Amounts below are the ALREADY
  // APPROVED live prices, moved here verbatim from the storefront
  // (SQ/index.html PRICES) and the old verify-payment email copy.
  // This is not a pricing change — it is the same value, relocated
  // to a place the browser cannot reach.
  // -----------------------------------------------------------
  ORAL_QB_NOTES: {
    id: "ORAL_QB_NOTES",
    label: "MEO Class I Oral — Question Bank + Notes",
    currency: "INR",
    grants: [ENTITLEMENTS.ORAL_QB_NOTES],
    protectedRoots: ["/meoclass1/"],
    tiers: {
      standard: { amount: 149900, label: "Standard Access", display: "₹1,499" },
      founders: { amount: 89900, label: "Founders Access", display: "₹899" },
    },
    defaultTier: "standard",
  },

  // -----------------------------------------------------------
  // NEW paid Written product. Founder-approved price: ₹1,500.
  // -----------------------------------------------------------
  // -----------------------------------------------------------
  // Written product. Founder-approved price: ₹1,500.
  //
  // PRICE LADDER (Founder decision, 14 August 2026): the price is
  // ₹500 per exam year in the library. It steps to ₹2,000 when 2026
  // reaches its eleventh paper and becomes a complete year.
  //
  // That step is a FOUNDER DECISION and nothing computes it. What is
  // automated is the reminder: tools/pastpapers/solvedqp_check.py warns
  // when a year completes and the amount here has not been revisited,
  // so the ladder cannot silently stall — but no script may ever change
  // what a candidate is charged.
  //
  // A price rise never touches an existing customer: their grant is
  // already in miw:ent:<email> and is not re-read from here.
  // -----------------------------------------------------------
  SOLVED_QP: {
    id: "SOLVED_QP",
    label: "MIW Solved Question Papers — Written",
    currency: "INR",
    grants: [ENTITLEMENTS.SOLVED_QP],
    protectedRoots: ["/solvedQP/"],
    tiers: {
      standard: { amount: 150000, label: "Solved QP Access", display: "₹1,500" },
    },
    defaultTier: "standard",
    priceLadder: { perExamYear: 50000, nextAmount: 200000, stepsWhenYearCompletes: 2026 },
  },

  // -----------------------------------------------------------
  // BUNDLE is deliberately NOT a third authorization mechanism.
  // It is a purchasable SKU that grants both atomic entitlements.
  // No bundle price has been approved by the Founder, so it is
  // marked unavailable: create-order will refuse it until an
  // amount is set. Middleware never consults BUNDLE — it only
  // ever asks "does this account hold ORAL_QB_NOTES / SOLVED_QP".
  // -----------------------------------------------------------
  BUNDLE: {
    id: "BUNDLE",
    label: "MIW Complete — Oral + Written",
    currency: "INR",
    grants: [ENTITLEMENTS.ORAL_QB_NOTES, ENTITLEMENTS.SOLVED_QP],
    protectedRoots: [],
    tiers: {},
    defaultTier: null,
    unavailable: "No bundle price has been approved.",
  },
};

// Legacy compatibility: the live storefront posts {tier:"standard"|
// "founders"} with no product field. Those tiers only ever meant the
// Oral product, so map them rather than break checkout mid-flight.
const LEGACY_TIER_PRODUCT = {
  standard: "ORAL_QB_NOTES",
  founders: "ORAL_QB_NOTES",
};

/**
 * Resolve a purchase request to a canonical {product, tier, amount}.
 * Throws on anything unrecognised. NEVER reads an amount from input.
 *
 * @param {object} input - { product?, tier? } straight off the wire.
 * @returns {{productId, tier, amount, currency, label, grants}}
 */
export function resolvePurchase(input = {}) {
  const rawProduct = String(input.product || "").trim();
  const rawTier = String(input.tier || "").trim().toLowerCase();

  let productId = rawProduct;
  if (!productId) {
    productId = LEGACY_TIER_PRODUCT[rawTier];
    if (!productId) {
      throw new PurchaseError("Unknown product", 400);
    }
  }

  const product = PRODUCTS[productId];
  if (!product) throw new PurchaseError("Unknown product", 400);
  if (product.unavailable) throw new PurchaseError(product.unavailable, 400);

  const tier = rawTier && product.tiers[rawTier] ? rawTier : product.defaultTier;
  const tierDef = tier && product.tiers[tier];
  if (!tierDef) throw new PurchaseError("Unsupported tier for product", 400);

  return {
    productId: product.id,
    tier,
    amount: tierDef.amount, // paise — server truth
    currency: product.currency,
    label: `${product.label} — ${tierDef.label}`,
    display: tierDef.display,
    grants: product.grants,
    // How long the purchase lasts. Server truth, exactly like the
    // amount: the browser may display a term but never chooses one.
    // A per-tier override wins, so a future perpetual SKU is a data
    // change rather than a code change.
    termDays: tierDef.termDays !== undefined
      ? tierDef.termDays
      : (product.termDays !== undefined ? product.termDays : DEFAULT_TERM_DAYS),
  };
}

// -----------------------------------------------------------
// NOTE: route policy deliberately does NOT live here.
//
// This file previously also exported requiredEntitlementForPath(),
// derived from each product's `protectedRoots`. Nothing imported it —
// middleware.js and the tests both use api/_lib/routes.js — but it
// disagreed with routes.js on the case that matters most:
// /meoclass1/pastpapers/ resolved to ORAL_QB_NOTES here, which would
// hand the entire ₹1,500 Written library to every Oral customer.
//
// Two definitions of "who may read this URL" is one too many, and the
// wrong one was the easier import to reach for. It has been removed.
// api/_lib/routes.js is the single source of route policy.
// -----------------------------------------------------------

export class PurchaseError extends Error {
  constructor(message, status = 400) {
    super(message);
    this.name = "PurchaseError";
    this.status = status;
  }
}
