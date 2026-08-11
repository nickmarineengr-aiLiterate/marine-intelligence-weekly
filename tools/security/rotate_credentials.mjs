#!/usr/bin/env node
// =============================================================
// Marine Intelligence Weekly — credential rotation (operator only)
// File: tools/security/rotate_credentials.mjs
//
// Incident response for credentials exposed in public git history.
// The exposed passwords are permanently compromised; this tool is what
// makes them stop working. See api/_lib/rotation.js for the policy and
// the ordering argument — this file is only the binding to the real
// Redis and the real SMTP relay.
//
// Like entitlement_admin.mjs this is a LOCAL script and not an endpoint,
// for the same reason: an authenticated admin route would be a permanent
// attack surface added to solve a one-off problem. Anyone who can run
// this already holds the Redis credentials.
//
// USAGE
//   node tools/security/rotate_credentials.mjs audit
//   node tools/security/rotate_credentials.mjs rotate              # dry run
//   node tools/security/rotate_credentials.mjs rotate --confirm
//   node tools/security/rotate_credentials.mjs rotate --confirm --no-email
//   node tools/security/rotate_credentials.mjs rotate --confirm --email a@b.com
//
// `audit` never writes. `rotate` is a DRY RUN unless --confirm is given,
// because it is customer-impacting and irreversible: the replaced
// password is not recoverable, so a mistaken run means every affected
// customer must be emailed a second time.
//
// --no-email rotates and revokes WITHOUT notifying. Use it only if the
// mail relay is down; the customer is then locked out until a later run
// with delivery restored. It prints a loud warning for that reason.
//
// OUTPUT DISCIPLINE
//   No password is ever printed. No full email address is ever printed.
//   Counts and masked addresses only, so this transcript is safe to keep.
//
// Requires KV_REST_API_URL and KV_REST_API_TOKEN in the environment.
// Source them the way the Vercel project does; do not paste them into a
// shell that records history.
// =============================================================

import { rotateAccount, classifyStored, maskEmail } from "../../api/_lib/rotation.js";
import { userKey } from "../../api/_lib/entitlements.js";
import { sessionsKey } from "../../api/_lib/sessions.js";
import { buildRotationEmail, makeTransport } from "../../api/_lib/email.js";

const action = process.argv[2];
const CONFIRM = process.argv.includes("--confirm");
const NO_EMAIL = process.argv.includes("--no-email");
const INCLUDE_HASHED = process.argv.includes("--include-hashed");
const onlyIdx = process.argv.indexOf("--email");
const ONLY = onlyIdx > -1 ? String(process.argv[onlyIdx + 1] || "").toLowerCase().trim() : null;

const URL_BASE = process.env.KV_REST_API_URL;
const TOKEN = process.env.KV_REST_API_TOKEN;

if (!URL_BASE || !TOKEN) {
  console.error("KV_REST_API_URL and KV_REST_API_TOKEN must be set.");
  process.exit(2);
}
if (action !== "audit" && action !== "rotate") {
  console.error("usage: rotate_credentials.mjs <audit|rotate> [--confirm] [--no-email] [--email <addr>]");
  process.exit(2);
}

async function cmd(args) {
  const r = await fetch(URL_BASE, {
    method: "POST",
    headers: { Authorization: `Bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  if (!r.ok) throw new Error(`Redis HTTP ${r.status}`);
  return r.json();
}

/** The store shape api/_lib/rotation.js expects, bound to real Redis. */
const store = {
  get: async (key) => (await cmd(["GET", key])).result ?? null,
  set: async (key, value) => (await cmd(["SET", key, value])).result,
  del: async (key) => (await cmd(["DEL", key])).result,
  countSessions: async (email) => Number((await cmd(["ZCARD", sessionsKey(email)])).result || 0),
};

async function scanAccounts() {
  const emails = [];
  let cursor = "0";
  do {
    const res = await cmd(["SCAN", cursor, "MATCH", "miw:user:*", "COUNT", "200"]);
    const [next, keys] = res.result || ["0", []];
    cursor = next;
    for (const k of keys || []) emails.push(String(k).slice("miw:user:".length));
  } while (cursor !== "0");
  return [...new Set(emails)].sort();
}

/**
 * Classify the whole store. This is the answer to "how many accounts
 * actually need remediation", which must be derived from production
 * truth and never assumed from the size of the leaked blob — some
 * accounts will have been hash-upgraded by an ordinary login already,
 * and some may no longer exist at all.
 */
async function audit() {
  const emails = ONLY ? [ONLY] : await scanAccounts();
  const buckets = { legacy_plaintext: [], hashed: [], absent: [] };
  let liveSessions = 0;

  for (const email of emails) {
    const stored = await store.get(userKey(email));
    const form = classifyStored(stored);
    buckets[form].push(email);
    if (form !== "absent") liveSessions += await store.countSessions(email);
  }

  console.log("MIW credential audit — production store truth\n");
  console.log(`accounts with a credential record : ${emails.length}`);
  console.log(`  LEGACY PLAINTEXT (needs rotation): ${buckets.legacy_plaintext.length}`);
  console.log(`  already hashed (safe as stored)  : ${buckets.hashed.length}`);
  console.log(`  no record / absent               : ${buckets.absent.length}`);
  console.log(`live sessions across all accounts  : ${liveSessions}`);
  return buckets;
}

async function main() {
  if (action === "audit") {
    await audit();
    console.log("\naudit is read-only — nothing was written.");
    return;
  }

  const buckets = await audit();
  const targets = INCLUDE_HASHED
    ? [...buckets.legacy_plaintext, ...buckets.hashed]
    : buckets.legacy_plaintext;

  console.log(`\n--- ROTATE — ${CONFIRM ? "EXECUTING" : "DRY RUN"} ---`);
  console.log(`accounts in scope: ${targets.length}`);
  if (INCLUDE_HASHED) {
    console.log("--include-hashed: already-hashed accounts are ALSO being rotated,");
    console.log("because their password text still appeared in public history.");
  }

  if (targets.length === 0) {
    console.log("\nNothing to rotate. Re-run `audit` to confirm this is steady state.");
    return;
  }

  if (!CONFIRM) {
    for (const e of targets.slice(0, 10)) console.log(`   would rotate ${maskEmail(e)}`);
    if (targets.length > 10) console.log(`   ... and ${targets.length - 10} more`);
    console.log("\nDRY RUN — nothing was written and no email was sent.");
    console.log("Re-run with --confirm to execute. This is not reversible.");
    return;
  }

  if (NO_EMAIL) {
    console.log("\n!! --no-email: customers will NOT be told their new password.");
    console.log("!! Each rotated account is locked out until a later notified run.");
  }

  const transport = NO_EMAIL ? null : await makeTransport();
  const sendMail = NO_EMAIL
    ? async () => { throw new Error("email suppressed by --no-email"); }
    : async (message) => transport.sendMail(message);

  const tally = {
    rotated: 0, rotated_email_failed: 0,
    skipped_absent: 0, skipped_already_hashed: 0, failed: 0,
  };
  let sessionsRevoked = 0;

  for (const email of targets) {
    try {
      const r = await rotateAccount({
        email,
        store,
        sendMail,
        buildEmail: buildRotationEmail,
        includeHashed: INCLUDE_HASHED,
      });
      tally[r.status] = (tally[r.status] || 0) + 1;
      sessionsRevoked += r.sessionsRevoked;
      // Masked, and carrying the OUTCOME only — never the credential.
      console.log(`   ${maskEmail(email)}  ${r.status}  (sessions revoked: ${r.sessionsRevoked})`);
    } catch (e) {
      tally.failed++;
      console.error(`   ${maskEmail(email)}  FAILED  ${e.code || e.message}`);
    }
  }

  console.log("\n--- RESULT ---");
  console.log(`rotated + notified   : ${tally.rotated}`);
  console.log(`rotated, email FAILED: ${tally.rotated_email_failed}`);
  console.log(`already hashed       : ${tally.skipped_already_hashed}`);
  console.log(`no record            : ${tally.skipped_absent}`);
  console.log(`failed               : ${tally.failed}`);
  console.log(`sessions revoked     : ${sessionsRevoked}`);

  if (tally.rotated_email_failed > 0) {
    console.log("\nACTION REQUIRED: those accounts are secure but their owner was not");
    console.log("told. The password is unrecoverable by design — re-run rotation for");
    console.log("each with --email <addr> once mail delivery is working.");
  }

  console.log("\nClosure test: re-run `audit`. LEGACY PLAINTEXT must read 0.");
}

main().catch((e) => {
  console.error("rotation failed:", e.message);
  process.exit(1);
});
