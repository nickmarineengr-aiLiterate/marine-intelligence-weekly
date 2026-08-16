#!/usr/bin/env node
// =============================================================
// Marine Intelligence Weekly — entitlement admin (operator only)
// File: tools/security/entitlement_admin.mjs
//
// A small platform run by one person needs a way to fix the exceptional
// case: a refund, a support grant, a mis-typed address at checkout.
//
// This is a LOCAL script, not an endpoint. There is deliberately no
// admin route on the site — an authenticated admin API is a permanent
// attack surface added to solve an occasional problem. Anyone who can
// run this already holds the Redis credentials.
//
// USAGE
//   node tools/security/entitlement_admin.mjs show   <email>
//   node tools/security/entitlement_admin.mjs grant  <email> SOLVED_QP
//   node tools/security/entitlement_admin.mjs grant  <email> BOTH --days 365
//   node tools/security/entitlement_admin.mjs grant  <email> SOLVED_QP --until 2027-08-14
//   node tools/security/entitlement_admin.mjs grant  <email> SOLVED_QP --perpetual
//   node tools/security/entitlement_admin.mjs revoke <email> SOLVED_QP --confirm
//   node tools/security/entitlement_admin.mjs logout <email>
//
// revoke touches exactly one field and requires --confirm, because it takes
// away access somebody may have paid for. logout drops the active session so
// the next request re-authenticates.
//
// ─────────────────────────────────────────────────────────────
// WHY THIS TOOL NO LONGER WRITES "1" BY DEFAULT
//
// It used to write the literal "1" for every support grant, and to print
// a grant as YES only when it equalled "1". Both were correct in the
// single-model world where a purchase was forever. Since August 2026 they
// are actively dangerous, in opposite directions:
//
//   READING  a live, in-term one-year customer was printed as "no",
//            which invites an operator to "fix" an account that is fine
//            — or worse, to tell a paying customer they have no access.
//
//   WRITING  every support correction minted a PERPETUAL grant. A
//            one-year buyer whose checkout failed got lifetime access
//            from the repair, silently, and nothing would ever reveal it.
//
// Both halves now defer to api/_lib/grants.js. That file is the single
// definition of what a stored value MEANS, and this tool must not carry a
// second opinion — the last time two definitions of an entitlement
// existed in this repo (products.js vs routes.js) the weaker one would
// have handed the entire Written library to every Oral customer.
//
// The write path goes through extendedGrantValue(), which is what makes a
// support grant safe: it can only ever move an expiry FORWARD, and a
// customer already holding "1" stays "1". An operator repairing a legacy
// account therefore cannot downgrade them by accident, whatever they type.
// ─────────────────────────────────────────────────────────────
//
// Requires KV_REST_API_URL and KV_REST_API_TOKEN in the environment.
// =============================================================

import {
  PERPETUAL,
  grantState,
  extendedGrantValue,
  GRANT_NONE,
  GRANT_PERPETUAL,
  GRANT_ACTIVE,
  GRANT_EXPIRED,
} from "../../api/_lib/grants.js";
import { DEFAULT_TERM_DAYS } from "../../api/_lib/products.js";
import { pathToFileURL } from "node:url";

const KNOWN = ["ORAL_QB_NOTES", "SOLVED_QP"];

const USAGE = [
  "usage:",
  "  entitlement_admin.mjs show   <email>",
  "  entitlement_admin.mjs grant  <email> <ORAL_QB_NOTES|SOLVED_QP|BOTH> [term]",
  "  entitlement_admin.mjs revoke <email> <entitlement> --confirm",
  "  entitlement_admin.mjs logout <email>",
  "",
  "grant term (choose one; default is the catalogue term, " + DEFAULT_TERM_DAYS + " days):",
  "  --days <n>          n days of access, counted from NOW",
  "  --until YYYY-MM-DD  access to the END of that day (UTC)",
  "  --perpetual         NEVER EXPIRES. Legacy restoration only — use this",
  "                      solely to put back access a customer bought before",
  "                      the one-year term began. It is not the repair for a",
  "                      current one-year buyer.",
  "",
  "A grant NEVER shortens what the account already holds: an existing",
  "perpetual grant survives any --days/--until, and a dated grant is",
  "extended from its own expiry rather than from today. So if you are",
  "repairing a purchase made months ago, --days simply adds time — it",
  "cannot cut the customer's term short. Use --until when you need the",
  "end date to match the original purchase exactly.",
].join("\n");

// -------------------------------------------------------------
// PURE ARGUMENT / DISPLAY LOGIC
//
// Split out from the I/O so the dangerous decisions — "is this account
// entitled?" and "what value am I about to write?" — are provable
// offline, with no Redis and no secrets. See entitlement_admin.test.mjs.
// -------------------------------------------------------------

/** Human wording for one stored grant value. Never prints the raw value. */
export function describeGrant(raw, nowSeconds) {
  const s = grantState(raw, nowSeconds);
  switch (s.status) {
    case GRANT_NONE:
      return "none";
    case GRANT_PERPETUAL:
      return "PERPETUAL (grandfathered — never expires)";
    case GRANT_ACTIVE: {
      const days = Math.floor((s.expires - nowSeconds) / 86400);
      return `ACTIVE until ${new Date(s.expires * 1000).toISOString().slice(0, 10)}` +
             ` (${days} day${days === 1 ? "" : "s"} left)`;
    }
    case GRANT_EXPIRED:
      return s.expires
        ? `EXPIRED on ${new Date(s.expires * 1000).toISOString().slice(0, 10)}`
        : "EXPIRED (stored value is corrupt — treated as no access)";
    default:
      return "unknown";
  }
}

/**
 * Resolve the term flags to what should be written.
 *
 * Returns {perpetual:true} or {termDays:n}. Throws on a combination that
 * could mean two things, because an ambiguous grant is one an operator
 * cannot review before it takes effect.
 */
export function resolveTerm(argv, nowMs) {
  const has = (f) => argv.includes(f);
  const valueOf = (f) => {
    const i = argv.indexOf(f);
    return i === -1 ? null : argv[i + 1];
  };

  const wantsPerpetual = has("--perpetual");
  const wantsDays = has("--days");
  const wantsUntil = has("--until");

  if ([wantsPerpetual, wantsDays, wantsUntil].filter(Boolean).length > 1) {
    throw new Error("choose ONE of --days, --until or --perpetual");
  }
  if (wantsPerpetual) return { perpetual: true };

  if (wantsDays) {
    const n = Number(valueOf("--days"));
    if (!Number.isFinite(n) || n <= 0) throw new Error("--days needs a positive number of days");
    return { perpetual: false, termDays: n };
  }

  if (wantsUntil) {
    const d = String(valueOf("--until") || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) throw new Error("--until needs a date as YYYY-MM-DD");
    // End of the named day, so "--until 2027-08-14" includes the 14th.
    const endMs = Date.parse(`${d}T23:59:59Z`);
    if (!Number.isFinite(endMs)) throw new Error("--until is not a real date");
    const termDays = (endMs - nowMs) / 86400000;
    if (termDays <= 0) throw new Error(`--until ${d} is in the past; that would grant nothing`);
    return { perpetual: false, termDays };
  }

  return { perpetual: false, termDays: DEFAULT_TERM_DAYS };
}

/**
 * The value to store, given what the account already holds.
 * Delegates to grants.js so this tool holds no term arithmetic of its own.
 */
export function grantValueToWrite(existing, term, nowMs) {
  if (term.perpetual) return PERPETUAL;
  return extendedGrantValue(existing, term.termDays, nowMs);
}

const [, , action, emailArg, entArg] = process.argv;
const CONFIRM = process.argv.includes("--confirm");

const URL_BASE = process.env.KV_REST_API_URL;
const TOKEN = process.env.KV_REST_API_TOKEN;

const email = String(emailArg || "").toLowerCase().trim();

async function cmd(args) {
  const r = await fetch(URL_BASE, {
    method: "POST",
    headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  if (!r.ok) throw new Error(`Redis HTTP ${r.status}`);
  return r.json();
}

function mask(e) {
  const [u, d] = String(e).split("@");
  return d ? `${u.slice(0, 2)}***@${d}` : "***";
}

async function show() {
  const res = await cmd(["HGETALL", `miw:ent:${email}`]);
  const raw = res.result;
  const held = {};
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
  } else if (raw && typeof raw === "object") Object.assign(held, raw);

  const acct = await cmd(["EXISTS", `miw:user:${email}`]);
  // Up to TWO live sessions per account (mobile + laptop).
  const sess = await cmd(["ZCARD", `miw:sessions:${email}`]);
  const live = Number(sess.result || 0);

  const now = Math.floor(Date.now() / 1000);
  console.log(`account   : ${mask(email)}`);
  console.log(`credential: ${acct.result ? "present" : "NONE — no login exists"}`);
  console.log(`sessions  : ${live} of 2 active`);
  for (const k of KNOWN) {
    console.log(`  ${k.padEnd(15)} ${describeGrant(held[k], now)}`);
  }
}

async function main() {
  if (!URL_BASE || !TOKEN) {
    console.error("KV_REST_API_URL and KV_REST_API_TOKEN must be set.");
    process.exit(2);
  }
  if (!action || !emailArg) {
    console.error(USAGE);
    process.exit(2);
  }

  if (action === "show") return show();

  if (action === "logout") {
    // Signs out EVERY device for this account. The legacy single-session
    // key is cleared too so no pre-V2 remnant can linger.
    await cmd(["DEL", `miw:sessions:${email}`]);
    await cmd(["DEL", `miw:active_session:${email}`]);
    console.log(`all active sessions cleared for ${mask(email)}`);
    return;
  }

  if (action === "grant") {
    const list = entArg === "BOTH" ? KNOWN : [entArg];
    for (const e of list) {
      if (!KNOWN.includes(e)) {
        console.error(`unknown entitlement: ${e}. Known: ${KNOWN.join(", ")}`);
        process.exit(2);
      }
    }

    let term;
    try {
      term = resolveTerm(process.argv, Date.now());
    } catch (e) {
      console.error(`${e.message}\n\n${USAGE}`);
      process.exit(2);
    }

    // Perpetual is a legacy restoration, not a repair. Make the operator
    // say so out loud, on the same footing as revoke: it is the only
    // grant here that cannot be undone by simply waiting.
    if (term.perpetual && !CONFIRM) {
      console.error(
        `--perpetual writes a grant that NEVER expires for ${mask(email)}.\n` +
        "Use it only to restore access bought before the one-year term began.\n" +
        "If this is a current one-year customer, drop the flag (or use --until).\n" +
        "Re-run with --confirm."
      );
      process.exit(2);
    }

    // Read first: the value written depends on what is already held, so a
    // perpetual holder cannot be downgraded and a running term is extended
    // rather than restarted. That decision lives in grants.js.
    const before = await cmd(["HMGET", `miw:ent:${email}`, ...list]);
    const existing = Array.isArray(before.result) ? before.result : [];

    const args = ["HSET", `miw:ent:${email}`];
    list.forEach((e, i) => {
      args.push(e, grantValueToWrite(existing[i], term, Date.now()));
    });
    await cmd(args);

    const how = term.perpetual
      ? "PERPETUAL (legacy restoration)"
      : `${Math.round(term.termDays)} days`;
    console.log(`granted ${list.join(" + ")} to ${mask(email)} — ${how}`);
    return show();
  }

  if (action === "revoke") {
    if (!KNOWN.includes(entArg)) {
      console.error(`unknown entitlement: ${entArg}`);
      process.exit(2);
    }
    if (!CONFIRM) {
      console.error(`This removes ${entArg} from ${mask(email)}. Re-run with --confirm.`);
      process.exit(2);
    }
    await cmd(["HDEL", `miw:ent:${email}`, entArg]);
    console.log(`revoked ${entArg} from ${mask(email)}`);
    return show();
  }

  console.error(`unknown action: ${action}\n\n${USAGE}`);
  process.exit(2);
}

// Run only when invoked as a script. The test suite imports this file to
// prove the read and write decisions offline, and importing it must not
// reach for Redis credentials or exit the test runner.
const invokedDirectly =
  !!process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;

if (invokedDirectly) {
  main().catch((e) => {
    console.error("failed:", e.message);
    process.exit(1);
  });
}
