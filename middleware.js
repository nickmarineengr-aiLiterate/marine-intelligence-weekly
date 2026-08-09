// =============================================================
// Marine Intelligence Weekly — Edge access gate (Security V2)
// File: middleware.js  (project root — Vercel Edge Middleware)
//
// THIS IS THE SECURITY BOUNDARY.
//
// Before this file existed, protected pages "gated" themselves with:
//     if(!/miw_auth=1/.test(document.cookie)) location.replace(...)
// which runs only AFTER Vercel has already streamed the full paid
// document to the client. `curl` ignored it completely, and forging
// the cookie was one line of JavaScript.
//
// Edge Middleware runs BEFORE static file serving, so an unauthorized
// request is answered with a redirect and the protected bytes are
// never read from the CDN, let alone sent.
//
// Everything below is authorization. The JS/CSS deterrence on the
// pages themselves (noindex, watermark, copy guards) is NOT security
// and is not relied upon here.
// =============================================================

import { next } from "@vercel/edge";
import { requiredEntitlementForPath } from "./api/_lib/routes.js";

export const config = {
  // Gate the two paid product roots. /SQ/, /api/ and the marketing
  // site are deliberately excluded so the storefront, the samples
  // and login keep working with no session.
  matcher: ["/meoclass1/:path*", "/solvedQP/:path*"],
};

const LOGIN_URL = "/SQ/pay.html";

// -------------------------------------------------------------
// Token verification — Web Crypto mirror of api/_lib/session.js.
// Edge has no node:crypto, so the HMAC is recomputed here with
// crypto.subtle. Format must stay identical: v1.<payload>.<sig>
// -------------------------------------------------------------
function b64urlToBytes(str) {
  const pad = str.length % 4 === 0 ? "" : "=".repeat(4 - (str.length % 4));
  const bin = atob(str.replace(/-/g, "+").replace(/_/g, "/") + pad);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function bytesToB64url(bytes) {
  let bin = "";
  for (const b of new Uint8Array(bytes)) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function verifyToken(token, secret) {
  if (!token || typeof token !== "string") return null;
  const parts = token.split(".");
  if (parts.length !== 3 || parts[0] !== "v1") return null;
  const [, payloadB64, sig] = parts;

  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const mac = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(payloadB64)
  );
  const expected = bytesToB64url(mac);

  // Constant-time-ish comparison. Lengths first, then accumulate diff.
  if (expected.length !== sig.length) return null;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ sig.charCodeAt(i);
  if (diff !== 0) return null;

  let payload;
  try {
    payload = JSON.parse(new TextDecoder().decode(b64urlToBytes(payloadB64)));
  } catch {
    return null;
  }
  if (!payload?.e || !payload?.s || !payload?.x) return null;
  if (Math.floor(Date.now() / 1000) >= payload.x) return null;
  return payload;
}

function parseCookies(header) {
  const out = {};
  if (!header) return out;
  for (const part of header.split(";")) {
    const i = part.indexOf("=");
    if (i < 0) continue;
    out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  return out;
}

function deny(request, reason) {
  const url = new URL(request.url);
  const to = new URL(LOGIN_URL, url.origin);
  to.searchParams.set("next", url.pathname);
  to.searchParams.set("reason", reason);
  return new Response(null, {
    status: 302,
    headers: {
      Location: to.toString(),
      // Never let an intermediary cache an authorization outcome.
      "Cache-Control": "no-store, private",
      "X-MIW-Gate": reason,
    },
  });
}

export default async function middleware(request) {
  const url = new URL(request.url);
  const required = requiredEntitlementForPath(url.pathname);

  // Public path — nothing to enforce.
  if (!required) return next();

  const secret = process.env.MIW_SESSION_SECRET;
  const redisUrl = process.env.KV_REST_API_URL;
  const redisToken = process.env.KV_REST_API_TOKEN;

  // Fail CLOSED. Paid content must never be served because a
  // dependency was missing or unreachable.
  if (!secret || !redisUrl || !redisToken) return deny(request, "misconfigured");

  const cookies = parseCookies(request.headers.get("cookie"));
  // NOTE: cookies.miw_auth is deliberately NOT consulted. It is a
  // readable UI hint and carries no authority.
  const payload = await verifyToken(cookies.miw_session, secret);
  if (!payload) return deny(request, "nosession");

  const email = String(payload.e).toLowerCase();

  let results;
  try {
    const r = await fetch(`${redisUrl}/pipeline`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${redisToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify([
        ["GET", `miw:active_session:${email}`],
        ["HGET", `miw:ent:${email}`, required],
      ]),
    });
    if (!r.ok) return deny(request, "authstore");
    results = await r.json();
  } catch {
    return deny(request, "authstore");
  }

  const activeSession = results?.[0]?.result ?? null;
  const entitled = results?.[1]?.result;

  // Single active session: a token minted before a newer login
  // no longer matches the stored id and is refused.
  if (!activeSession || activeSession !== payload.s) return deny(request, "evicted");

  if (!(entitled === "1" || entitled === 1)) return deny(request, "noentitlement");

  const res = next();
  res.headers.set("Cache-Control", "no-store, private");
  return res;
}
