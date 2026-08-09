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
//   node tools/security/entitlement_admin.mjs grant  <email> ORAL_QB_NOTES
//   node tools/security/entitlement_admin.mjs grant  <email> SOLVED_QP
//   node tools/security/entitlement_admin.mjs grant  <email> BOTH
//   node tools/security/entitlement_admin.mjs revoke <email> SOLVED_QP
//   node tools/security/entitlement_admin.mjs logout <email>
//
// grant is additive and idempotent. revoke touches exactly one field and
// requires --confirm, because it takes away access somebody may have paid
// for. logout drops the active session so the next request re-authenticates.
//
// Requires KV_REST_API_URL and KV_REST_API_TOKEN in the environment.
// =============================================================

const [, , action, emailArg, entArg] = process.argv;
const CONFIRM = process.argv.includes("--confirm");

const URL_BASE = process.env.KV_REST_API_URL;
const TOKEN = process.env.KV_REST_API_TOKEN;
const KNOWN = ["ORAL_QB_NOTES", "SOLVED_QP"];

if (!URL_BASE || !TOKEN) {
  console.error("KV_REST_API_URL and KV_REST_API_TOKEN must be set.");
  process.exit(2);
}
if (!action || !emailArg) {
  console.error("usage: entitlement_admin.mjs <show|grant|revoke|logout> <email> [entitlement]");
  process.exit(2);
}

const email = String(emailArg).toLowerCase().trim();

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

  console.log(`account   : ${mask(email)}`);
  console.log(`credential: ${acct.result ? "present" : "NONE — no login exists"}`);
  console.log(`sessions  : ${live} of 2 active`);
  for (const k of KNOWN) console.log(`  ${k.padEnd(15)} ${held[k] === "1" ? "YES" : "no"}`);
}

async function main() {
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
    const args = ["HSET", `miw:ent:${email}`];
    for (const e of list) args.push(e, "1");
    await cmd(args);
    console.log(`granted ${list.join(" + ")} to ${mask(email)}`);
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

  console.error(`unknown action: ${action}`);
  process.exit(2);
}

main().catch((e) => {
  console.error("failed:", e.message);
  process.exit(1);
});
