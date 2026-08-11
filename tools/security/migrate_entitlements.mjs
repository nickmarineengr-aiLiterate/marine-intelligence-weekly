#!/usr/bin/env node
// =============================================================
// Marine Intelligence Weekly — back-fill existing customers
// File: tools/security/migrate_entitlements.mjs
//
// Every existing paid account predates per-product entitlements: the old
// model was a single global "has a password => can open /meoclass1/".
// Those customers bought the ORAL product, so they are back-filled to
// exactly ORAL_QB_NOTES.
//
// SOLVED_QP IS NEVER GRANTED BY THIS TOOL. The Written product did not
// exist when these accounts were created, so nobody paid for it. A
// blanket migration would hand the entire 1500 rupee library to every
// historical customer — which is precisely the failure this whole piece
// of work exists to prevent.
//
// SAFETY
//   * dry run by default; --apply is required to write anything
//   * additive only — it can grant, and has no code path that removes
//   * idempotent — re-running changes nothing after the first pass
//   * prints masked emails only; no address is ever written to stdout
//     in full, and nothing is written to the repository
//
// USAGE
//   node tools/security/migrate_entitlements.mjs            # dry run
//   node tools/security/migrate_entitlements.mjs --apply    # execute
//   node tools/security/migrate_entitlements.mjs --verify   # report only
//
// Requires KV_REST_API_URL and KV_REST_API_TOKEN in the environment.
// Do not paste those into a shell history file; source them from the
// same place the Vercel project reads them.
// =============================================================

const APPLY = process.argv.includes("--apply");
const VERIFY_ONLY = process.argv.includes("--verify");

const URL_BASE = process.env.KV_REST_API_URL;
const TOKEN = process.env.KV_REST_API_TOKEN;

if (!URL_BASE || !TOKEN) {
  console.error("KV_REST_API_URL and KV_REST_API_TOKEN must be set.");
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

function mask(email) {
  const [u, d] = String(email).split("@");
  if (!d) return "***";
  return `${u.slice(0, 2)}***@${d}`;
}

async function scanUsers() {
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

async function main() {
  console.log(`MIW entitlement back-fill — ${APPLY ? "APPLY" : "DRY RUN"}`);
  console.log("target: ORAL_QB_NOTES only. SOLVED_QP is never granted here.\n");

  const emails = await scanUsers();
  console.log(`accounts found: ${emails.length}`);

  let alreadyOral = 0, toGrant = 0, granted = 0, alreadySolved = 0;
  const pending = [];

  for (const email of emails) {
    const res = await cmd(["HGETALL", `miw:ent:${email}`]);
    const raw = res.result;
    const held = {};
    if (Array.isArray(raw)) {
      for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
    } else if (raw && typeof raw === "object") {
      Object.assign(held, raw);
    }

    if (held.SOLVED_QP === "1") alreadySolved++;
    if (held.ORAL_QB_NOTES === "1") {
      alreadyOral++;
    } else {
      toGrant++;
      pending.push(email);
    }
  }

  console.log(`  already ORAL_QB_NOTES : ${alreadyOral}`);
  console.log(`  need ORAL_QB_NOTES    : ${toGrant}`);
  console.log(`  hold SOLVED_QP        : ${alreadySolved}  (purchases; untouched)`);

  if (VERIFY_ONLY) {
    console.log("\n--verify: reporting only, nothing written.");
    return;
  }

  if (toGrant === 0) {
    console.log("\nNothing to do — migration is already complete and idempotent.");
    return;
  }

  console.log(`\n${APPLY ? "granting" : "would grant"} ORAL_QB_NOTES to ${toGrant} account(s):`);
  for (const email of pending.slice(0, 10)) console.log(`   ${mask(email)}`);
  if (pending.length > 10) console.log(`   ... and ${pending.length - 10} more`);

  if (!APPLY) {
    console.log("\nDRY RUN — nothing was written. Re-run with --apply to execute.");
    return;
  }

  for (const email of pending) {
    // HSET on one field. Additive: any other field on the hash, including a
    // SOLVED_QP granted by a real purchase, is left exactly as it was.
    await cmd(["HSET", `miw:ent:${email}`, "ORAL_QB_NOTES", "1"]);
    granted++;
  }

  console.log(`\ngranted: ${granted}`);
  console.log("Re-run without --apply to confirm it now reports nothing to do.");
  console.log("\nROLLBACK, if ever needed, is per-account and deliberately manual:");
  console.log('  HDEL miw:ent:<email> ORAL_QB_NOTES');
  console.log("There is no bulk revoke in this tool by design.");
}

main().catch((e) => {
  console.error("migration failed:", e.message);
  process.exit(1);
});
