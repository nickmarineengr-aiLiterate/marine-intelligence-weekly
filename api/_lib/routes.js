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
