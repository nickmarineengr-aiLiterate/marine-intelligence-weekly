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
//   node tools/security/entitlement_admin.mjs mark-passed      <email> [product] --confirm
//   node tools/security/entitlement_admin.mjs reopen-candidate <email> [product] --confirm
//   node tools/security/entitlement_admin.mjs summary
//
// revoke touches exactly one field and requires --confirm, because it takes
// away access somebody may have paid for. logout drops the active session so
// the next request re-authenticates.
//
// ─────────────────────────────────────────────────────────────
// CANDIDATE-LIFECYCLE CLOSURE (Founder decision, 16 August 2026)
//
// Access sold before the one-year term is Candidate-Lifecycle Access:
// it runs for the member's MEO Class I preparation and the Founder may
// close it once MIW has RELIABLE CONFIRMATION that they passed.
//
// Nothing in this repo detects a pass. There is no cron, no inactivity
// rule, no results scraping, and no bulk mode — the entire mechanism is
// one operator naming one account, because the input is a fact only a
// human can establish. Inactivity is not passing; a member still
// preparing keeps their access however long they are away.
//
// mark-passed can ONLY move a lifecycle grant to closed. A dated
// one-year grant, an absent grant and an already-closed grant are left
// untouched and reported as such. That is what stops closing somebody's
// legacy Oral access from destroying the Written year they paid for
// separately — the two are different fields holding different shapes,
// and only one shape is eligible.
//
// The closure keeps the prior value, so reopen-candidate restores what
// was actually held rather than minting a fresh perpetual grant, and a
// closed member stays distinguishable from someone who never bought.
// ─────────────────────────────────────────────────────────────
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
  markPassedValue,
  reopenedGrantValue,
  grantAllowsAccess,
  GRANT_NONE,
  GRANT_PERPETUAL,
  GRANT_ACTIVE,
  GRANT_EXPIRED,
  GRANT_PASSED_CLOSED,
  GRANT_REFUNDED,
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
  "  entitlement_admin.mjs mark-passed      <email> [entitlement|BOTH] --confirm",
  "  entitlement_admin.mjs reopen-candidate <email> [entitlement|BOTH] --confirm",
  "  entitlement_admin.mjs summary",
  "",
  "mark-passed records that the member passed MEO Class I and closes their",
  "Candidate-Lifecycle access. With no entitlement named it applies to EVERY",
  "lifecycle grant on the account. It never touches a dated one-year grant,",
  "so a separately-bought Written year survives closing a legacy Oral one.",
  "Use it only on reliable confirmation — the member told you, or sent",
  "evidence. Never infer it from silence or inactivity.",
  "  --remove-credential  also delete the password, so the account cannot be",
  "                       signed into at all. REFUSED while any other valid",
  "                       entitlement remains on the same email.",
  "",
  "reopen-candidate undoes a closure, restoring the exact grant that was held",
  "before it. Use it when somebody was marked passed in error.",
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
      return "Candidate-Lifecycle / ACTIVE (no expiry date; close with mark-passed)";
    case GRANT_PASSED_CLOSED: {
      const when = s.closedAt
        ? new Date(s.closedAt * 1000).toISOString().slice(0, 10)
        : "date unrecorded";
      return `Candidate-Lifecycle / PASSED_CLOSED (closed ${when}; reopen-candidate restores it)`;
    }
    // Kept distinct from EXPIRED and from PASSED_CLOSED on purpose. All
    // three deny, but they are three different answers to "why did this
    // person lose access", and only one of them has money behind it.
    case GRANT_REFUNDED: {
      const when = s.refundedAt
        ? new Date(s.refundedAt * 1000).toISOString().slice(0, 10)
        : "date unrecorded";
      return `REFUNDED (money returned ${when}; see miw:refund:* for the payment)`;
    }
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

/**
 * What mark-passed would do to each named entitlement, decided BEFORE
 * anything is written.
 *
 * Every entry carries an explicit action, including the ones left alone,
 * so the operator sees the whole account rather than only the part that
 * changed. Silence about a skipped product is how somebody concludes
 * their Written year was closed too.
 *
 * @param {object} held   stored values, keyed by entitlement
 * @param {string[]} list entitlements to consider
 * @returns {Array<{entitlement, action, reason, value}>}
 */
export function planMarkPassed(held, list, nowMs) {
  return list.map((e) => {
    const raw = held[e];
    const value = markPassedValue(raw, nowMs);
    if (value) {
      return { entitlement: e, action: "close", reason: "Candidate-Lifecycle access closed", value };
    }
    const status = grantState(raw, Math.floor(nowMs / 1000)).status;
    const reason =
      status === GRANT_PASSED_CLOSED ? "already closed — no change" :
      status === GRANT_ACTIVE        ? "dated one-year access — UNTOUCHED, it was paid for separately" :
      status === GRANT_EXPIRED       ? "dated access already ended — nothing to close" :
                                       "no grant on this account — nothing to close";
    return { entitlement: e, action: "skip", reason, value: null };
  });
}

/** The mirror of planMarkPassed: what reopen-candidate would restore. */
export function planReopen(held, list) {
  return list.map((e) => {
    const raw = held[e];
    const value = reopenedGrantValue(raw);
    if (value) {
      return { entitlement: e, action: "reopen", reason: "restored to the grant held before closure", value };
    }
    return {
      entitlement: e,
      action: "skip",
      reason: "not closed — reopen-candidate only undoes a mark-passed",
      value: null,
    };
  });
}

/**
 * Roll a set of stored account records into the four counts the Founder
 * asked for. Pure, so the arithmetic is provable without Redis.
 *
 * Counts ENTITLEMENTS, not people: one email holding a closed legacy
 * Oral grant and a live Written year is one of each, which is the honest
 * answer. An account is named in `accounts` once regardless.
 *
 * @param {Array<{email, held}>} records
 */
export function summariseCounts(records, nowSeconds, known) {
  const counts = {
    accounts: records.length,
    lifecycleActive: 0,
    lifecyclePassedClosed: 0,
    fixedTermActive: 0,
    fixedTermExpired: 0,
    refunded: 0,
    corrupt: 0,
  };
  for (const { held } of records) {
    for (const e of known) {
      const s = grantState(held[e], nowSeconds);
      if (s.status === GRANT_PERPETUAL) counts.lifecycleActive++;
      else if (s.status === GRANT_PASSED_CLOSED) counts.lifecyclePassedClosed++;
      else if (s.status === GRANT_REFUNDED) counts.refunded++;
      else if (s.status === GRANT_ACTIVE) counts.fixedTermActive++;
      else if (s.status === GRANT_EXPIRED) {
        if (s.expires) counts.fixedTermExpired++;
        else if (held[e] !== undefined && held[e] !== null) counts.corrupt++;
      }
    }
  }
  return counts;
}

const [, , action, emailArg, entArg] = process.argv;
const CONFIRM = process.argv.includes("--confirm");
const REMOVE_CREDENTIAL = process.argv.includes("--remove-credential");

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

/**
 * Refuse to act, with a non-zero exit status.
 *
 * process.exitCode, NOT process.exit(). Calling process.exit() here
 * aborts the process while the HTTP connection pool from the reads
 * above is still tearing down, and on Windows that trips a libuv
 * assertion: the operator sees a crash and a nonsense exit status
 * (0xC0000409) instead of a clean "2". Anything wrapping this tool in a
 * script would read that as an unrecognised failure rather than "not
 * confirmed". Setting the code and returning lets the runtime close its
 * handles and exit properly — measured at ~300ms, no hang.
 *
 * Refusals that happen BEFORE any network call are still process.exit(),
 * because there is nothing outstanding for them to race.
 */
function refuse(message) {
  console.error(message);
  process.exitCode = 2;
}

function mask(e) {
  const [u, d] = String(e).split("@");
  return d ? `${u.slice(0, 2)}***@${d}` : "***";
}

/** The stored entitlement values for one account, Upstash shape absorbed. */
async function readHeld(addr) {
  const res = await cmd(["HGETALL", `miw:ent:${addr}`]);
  const raw = res.result;
  const held = {};
  if (Array.isArray(raw)) {
    for (let i = 0; i + 1 < raw.length; i += 2) held[raw[i]] = raw[i + 1];
  } else if (raw && typeof raw === "object") Object.assign(held, raw);
  return held;
}

async function show() {
  const held = await readHeld(email);

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

  // One line naming the member's standing, because the per-product lines
  // answer "what may they read" and the Founder also needs "who is this
  // on my books" — an account with a closed lifecycle grant is a former
  // customer, not a stranger, and the two must not look alike.
  const states = KNOWN.map((k) => grantState(held[k], now).status);
  const lifecycle =
    states.includes(GRANT_PERPETUAL)     ? "ACTIVE_CANDIDATE (Candidate-Lifecycle access running)" :
    states.includes(GRANT_PASSED_CLOSED) ? "PASSED_CLOSED (recorded as passed; access closed)" :
    states.includes(GRANT_REFUNDED)      ? "REFUNDED (purchase money returned; access ended)" :
    states.some((s) => s !== GRANT_NONE) ? "fixed-term customer — no Candidate-Lifecycle grant" :
                                           "no entitlement on record";
  console.log(`lifecycle : ${lifecycle}`);
  return held;
}

/**
 * mark-passed / reopen-candidate.
 *
 * Both follow the same shape on purpose: read, PLAN, show the operator
 * the whole account, and write only on --confirm. The plan is printed
 * even when refusing, so the confirmation step is where the operator
 * discovers they named the wrong person — not afterwards.
 */
async function lifecycleCommand(action) {
  const passing = action === "mark-passed";

  // The entitlement argument is optional here, unlike grant/revoke. With
  // none given the command applies to every lifecycle grant on the
  // account, which is the ordinary case: a member who passed has passed,
  // whatever they bought. A leading "--" is a flag, not a product.
  const named = entArg && !entArg.startsWith("--") ? entArg : "BOTH";
  const list = named === "BOTH" ? KNOWN : [named];
  for (const e of list) {
    if (!KNOWN.includes(e)) {
      console.error(`unknown entitlement: ${e}. Known: ${KNOWN.join(", ")}, BOTH`);
      process.exit(2);
    }
  }

  const held = await readHeld(email);
  const now = Date.now();
  const nowSeconds = Math.floor(now / 1000);

  // An account with no credential and no grant is almost always a typo.
  // Refusing outright beats writing a closure onto an address nobody
  // holds, where it would sit unnoticed until the real member complained.
  const acct = await cmd(["EXISTS", `miw:user:${email}`]);
  const anyGrant = KNOWN.some((k) => held[k] !== undefined && held[k] !== null);
  if (!acct.result && !anyGrant) {
    return refuse(
      `no account and no entitlement exist for ${mask(email)}.\n` +
      "Nothing was changed. Check the address against the original purchase."
    );
  }

  const plan = passing ? planMarkPassed(held, list, now) : planReopen(held, list);

  console.log(`account   : ${mask(email)}`);
  for (const k of KNOWN) console.log(`  ${k.padEnd(15)} ${describeGrant(held[k], nowSeconds)}`);
  console.log(action === "mark-passed" ? "\nmark-passed would:" : "\nreopen-candidate would:");
  for (const p of plan) {
    console.log(`  ${p.entitlement.padEnd(15)} ${p.action === "skip" ? "no change" : p.action.toUpperCase()} — ${p.reason}`);
  }

  const changes = plan.filter((p) => p.action !== "skip");
  if (changes.length === 0) {
    console.log(
      `\nnothing to do — no ${passing ? "Candidate-Lifecycle grant to close" : "closed grant to restore"} here.`
    );
    return;
  }

  if (!CONFIRM) {
    return refuse("\nNothing was changed. Re-run with --confirm to apply.");
  }

  const args = ["HSET", `miw:ent:${email}`];
  for (const p of changes) args.push(p.entitlement, p.value);
  await cmd(args);

  if (passing) {
    // Sign every device out. The edge gate re-reads the entitlement on
    // each request so a live session would lose access anyway, but a
    // closure the member can still see a signed-in page behind is a
    // support call waiting to happen. This costs a login to anyone who
    // still holds a valid dated product, and costs them nothing else.
    await cmd(["DEL", `miw:sessions:${email}`]);
    await cmd(["DEL", `miw:active_session:${email}`]);
    console.log("\nsessions cleared.");

    if (REMOVE_CREDENTIAL) {
      // The password is ACCOUNT identity; entitlements are per product.
      // Deleting it while another product is still valid would lock a
      // paying customer out of something this command never touched.
      const after = await readHeld(email);
      const stillValid = KNOWN.filter((k) => grantAllowsAccess(after[k], Math.floor(Date.now() / 1000)));
      if (stillValid.length) {
        console.error(
          `credential NOT removed: ${mask(email)} still holds valid access to ` +
          `${stillValid.join(" + ")}.\nThe lifecycle closure above stands. Re-run ` +
          "--remove-credential only once nothing valid remains."
        );
      } else {
        await cmd(["DEL", `miw:user:${email}`]);
        console.log("credential removed — this account can no longer sign in.");
      }
    }
  }

  console.log("");
  await show();
}

/**
 * Deterministic counts across every account on record.
 *
 * SCAN, not KEYS: KEYS blocks the server for the whole sweep, and even
 * at ~100 accounts that is a habit worth not having. The cursor loop is
 * bounded so a runaway cannot spin forever, and if the bound is reached
 * the output SAYS the figures are partial rather than quietly under-
 * reporting — a count the Founder cannot trust is worse than none.
 */
async function summary() {
  const PATTERN = "miw:ent:*";
  const MAX_PAGES = 500;

  let cursor = "0";
  let pages = 0;
  const keys = new Set();
  do {
    const res = await cmd(["SCAN", cursor, "MATCH", PATTERN, "COUNT", "200"]);
    const out = res.result;
    if (!Array.isArray(out) || out.length < 2) break;
    cursor = String(out[0]);
    for (const k of out[1] || []) keys.add(String(k));
    pages++;
  } while (cursor !== "0" && pages < MAX_PAGES);

  const records = [];
  for (const key of keys) {
    records.push({ email: key.slice("miw:ent:".length), held: await readHeld(key.slice("miw:ent:".length)) });
  }

  const c = summariseCounts(records, Math.floor(Date.now() / 1000), KNOWN);
  console.log(`accounts with an entitlement record : ${c.accounts}`);
  console.log("");
  console.log("counted per product, so one account may appear in two rows:");
  console.log(`  Candidate-Lifecycle ACTIVE        : ${c.lifecycleActive}`);
  console.log(`  Candidate-Lifecycle PASSED_CLOSED : ${c.lifecyclePassedClosed}`);
  console.log(`  Fixed-term ACTIVE                 : ${c.fixedTermActive}`);
  console.log(`  Fixed-term EXPIRED                : ${c.fixedTermExpired}`);
  console.log(`  REFUNDED (money returned)         : ${c.refunded}`);
  if (c.corrupt) console.log(`  UNREADABLE (denied — investigate)  : ${c.corrupt}`);
  if (cursor !== "0") {
    console.log("\nWARNING: the scan hit its page limit. These figures are PARTIAL.");
  }
}

async function main() {
  if (!URL_BASE || !TOKEN) {
    console.error("KV_REST_API_URL and KV_REST_API_TOKEN must be set.");
    process.exit(2);
  }
  if (action === "summary") return summary();

  if (!action || !emailArg) {
    console.error(USAGE);
    process.exit(2);
  }

  if (action === "show") {
    await show();
    return;
  }

  if (action === "mark-passed" || action === "reopen-candidate") {
    return lifecycleCommand(action);
  }

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
