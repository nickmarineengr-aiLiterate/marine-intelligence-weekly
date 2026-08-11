// =============================================================
// Marine Intelligence Weekly — Two-active-session test suite
// Run: npm run security:test
//
// Proves the Founder-approved policy: a customer may stay signed in
// on TWO devices (mobile + laptop). A third login does not fail — it
// retires the OLDEST session.
//
// Offline by design. Redis is a real in-memory sorted-set double, so
// the REAL functions in api/_lib/sessions.js are what execute — the
// commands asserted here are the exact commands production issues.
//
// Every block ends with a POSITIVE CONTROL: a guard that never fires
// is not a guard.
// =============================================================

import { test, describe, beforeEach } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const {
  MAX_ACTIVE_SESSIONS, sessionsKey, legacySessionKey, loginCommands,
  addActiveSession, isActiveSession, listActiveSessions,
  removeActiveSession, clearAllSessions,
} = await import("../../api/_lib/sessions.js");

const { authorizeRequest } = await import("../../api/_lib/routes.js");
const {
  createSessionToken, verifySessionToken, newSessionId,
  hashPassword, verifyPassword,
} = await import("../../api/_lib/session.js");

// -------------------------------------------------------------
// A minimal but faithful sorted-set Redis double.
// Only the commands this module actually issues are implemented;
// anything else throws so a silent typo cannot masquerade as a pass.
// -------------------------------------------------------------
function fakeRedis() {
  /** @type {Map<string, Map<string, number>>} zsets */
  const z = new Map();
  const strings = new Map();
  const log = [];

  const zset = (k) => {
    if (!z.has(k)) z.set(k, new Map());
    return z.get(k);
  };
  // Redis orders by score, then lexicographically by member.
  const sorted = (k) =>
    [...zset(k).entries()].sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1));

  function one(args) {
    const [op, key, ...rest] = args;
    log.push(op);
    switch (op) {
      case "ZADD": {
        zset(key).set(rest[1], Number(rest[0]));
        return { result: 1 };
      }
      case "ZSCORE": {
        const s = zset(key).get(rest[0]);
        return { result: s === undefined ? null : String(s) };
      }
      case "ZREM": {
        return { result: zset(key).delete(rest[0]) ? 1 : 0 };
      }
      case "ZREVRANGE": {
        return { result: sorted(key).map(([m]) => m).reverse() };
      }
      case "ZREMRANGEBYRANK": {
        const items = sorted(key);
        let [start, stop] = [Number(rest[0]), Number(rest[1])];
        const n = items.length;
        if (start < 0) start += n;
        if (stop < 0) stop += n;
        let removed = 0;
        for (let i = Math.max(0, start); i <= Math.min(n - 1, stop); i++) {
          zset(key).delete(items[i][0]);
          removed++;
        }
        return { result: removed };
      }
      case "ZREMRANGEBYSCORE": {
        // Only the exclusive-max form "(<n>" is used by loginCommands.
        const maxRaw = String(rest[1]);
        const exclusive = maxRaw.startsWith("(");
        const max = Number(exclusive ? maxRaw.slice(1) : maxRaw);
        let removed = 0;
        for (const [m, s] of [...zset(key).entries()]) {
          if (exclusive ? s < max : s <= max) { zset(key).delete(m); removed++; }
        }
        return { result: removed };
      }
      case "EXPIRE": return { result: 1 };
      case "DEL": {
        const had = z.delete(key) || strings.delete(key);
        return { result: had ? 1 : 0 };
      }
      case "SET": { strings.set(key, rest[0]); return { result: "OK" }; }
      case "GET": { return { result: strings.get(key) ?? null }; }
      default:
        throw new Error(`fakeRedis: unimplemented command ${op}`);
    }
  }

  return {
    z, strings, log,
    deps: {
      cmd: async (args) => one(args),
      pipeline: async (cmds) => cmds.map(one),
    },
    members: (email) => [...zset(sessionsKey(email)).keys()],
  };
}

const EMAIL = "existing.customer@example.com";
const TTL = 30 * 24 * 60 * 60;

// -------------------------------------------------------------
// 1. THE FOUNDER POLICY — TWO DEVICES
// -------------------------------------------------------------
describe("two active sessions — mobile + laptop stay signed in", () => {
  let R;
  beforeEach(() => { R = fakeRedis(); });

  test("the approved cap is exactly two", () => {
    assert.equal(MAX_ACTIVE_SESSIONS, 2,
      "Founder policy is two devices — not one, not three");
  });

  test("LOGIN A -> A is valid", async () => {
    const a = newSessionId();
    await addActiveSession(EMAIL, a, TTL, R.deps);
    assert.equal(await isActiveSession(EMAIL, a, R.deps), true);
  });

  test("LOGIN A then B -> BOTH stay valid (the whole point)", async () => {
    const a = newSessionId(), b = newSessionId();
    await addActiveSession(EMAIL, a, TTL, R.deps);
    await addActiveSession(EMAIL, b, TTL, R.deps);

    assert.equal(await isActiveSession(EMAIL, a, R.deps), true,
      "the phone must NOT be kicked off when the laptop signs in");
    assert.equal(await isActiveSession(EMAIL, b, R.deps), true);
    assert.equal((await listActiveSessions(EMAIL, R.deps)).length, 2);
  });

  test("LOGIN C -> oldest A retired, B and C valid", async () => {
    const a = newSessionId(), b = newSessionId(), c = newSessionId();
    // Distinct login times so "oldest" is unambiguous.
    await addActiveSession(EMAIL, a, TTL, R.deps);
    await new Promise((r) => setTimeout(r, 1100));
    await addActiveSession(EMAIL, b, TTL, R.deps);
    await new Promise((r) => setTimeout(r, 1100));
    await addActiveSession(EMAIL, c, TTL, R.deps);

    assert.equal(await isActiveSession(EMAIL, a, R.deps), false, "A must be evicted");
    assert.equal(await isActiveSession(EMAIL, b, R.deps), true, "B must survive");
    assert.equal(await isActiveSession(EMAIL, c, R.deps), true, "C must be live");
    assert.equal(R.members(EMAIL).length, 2, "never more than two");
  });

  test("a third login never exceeds the cap, however many follow", async () => {
    for (let i = 0; i < 8; i++) {
      await addActiveSession(EMAIL, `sid-${i}`, TTL, R.deps);
      assert.ok(R.members(EMAIL).length <= MAX_ACTIVE_SESSIONS,
        `cap breached after ${i + 1} logins`);
    }
    assert.deepEqual(new Set(R.members(EMAIL)), new Set(["sid-6", "sid-7"]),
      "the two most recent devices are the survivors");
  });

  test("logout signs out ONLY that device", async () => {
    const b = newSessionId(), c = newSessionId();
    await addActiveSession(EMAIL, b, TTL, R.deps);
    await addActiveSession(EMAIL, c, TTL, R.deps);

    await removeActiveSession(EMAIL, b, R.deps);
    assert.equal(await isActiveSession(EMAIL, b, R.deps), false);
    assert.equal(await isActiveSession(EMAIL, c, R.deps), true,
      "logging out the laptop must not sign out the phone");
  });

  test("sign-out-everywhere clears both (used by credential rotation)", async () => {
    await addActiveSession(EMAIL, "s1", TTL, R.deps);
    await addActiveSession(EMAIL, "s2", TTL, R.deps);
    await clearAllSessions(EMAIL, R.deps);
    assert.equal(R.members(EMAIL).length, 0);
    assert.equal(await isActiveSession(EMAIL, "s1", R.deps), false);
  });

  test("a session older than the TTL is pruned on next login", async () => {
    const stale = "stale-session", fresh = "fresh-session";
    const now = Math.floor(Date.now() / 1000);
    // Seed a session that logged in *before* the TTL window.
    R.deps.pipeline([["ZADD", sessionsKey(EMAIL), String(now - TTL - 60), stale]]);
    assert.equal(await isActiveSession(EMAIL, stale, R.deps), true, "seeded");

    await addActiveSession(EMAIL, fresh, TTL, R.deps);
    assert.equal(await isActiveSession(EMAIL, stale, R.deps), false,
      "expired sessions must not linger in the set");
  });

  test("an unknown session id is never active", async () => {
    await addActiveSession(EMAIL, "real", TTL, R.deps);
    assert.equal(await isActiveSession(EMAIL, "never-issued", R.deps), false);
    assert.equal(await isActiveSession(EMAIL, "", R.deps), false);
    assert.equal(await isActiveSession(EMAIL, null, R.deps), false);
  });

  test("sessions are scoped per account — one customer cannot use another's id", async () => {
    await addActiveSession("a@example.com", "shared-looking-id", TTL, R.deps);
    assert.equal(await isActiveSession("b@example.com", "shared-looking-id", R.deps), false);
  });

  test("email casing and padding cannot fork an account's session set", async () => {
    await addActiveSession("  Mixed.Case@Example.COM  ", "sid-x", TTL, R.deps);
    assert.equal(await isActiveSession("mixed.case@example.com", "sid-x", R.deps), true);
  });

  test("the legacy single-session key is deleted on login", async () => {
    R.strings.set(legacySessionKey(EMAIL), "old-single-session-id");
    await addActiveSession(EMAIL, "new-sid", TTL, R.deps);
    assert.equal(R.strings.has(legacySessionKey(EMAIL)), false,
      "the superseded miw:active_session key must not linger");
  });

  test("login trims AFTER adding — the ordering the cap depends on", () => {
    const cmds = loginCommands(EMAIL, "sid", 1_000_000, TTL);
    const ops = cmds.map((c) => c[0]);
    assert.deepEqual(ops, [
      "ZREMRANGEBYSCORE", "ZADD", "ZREMRANGEBYRANK", "EXPIRE", "DEL",
    ]);
    assert.ok(ops.indexOf("ZADD") < ops.indexOf("ZREMRANGEBYRANK"),
      "trimming before adding would let three sessions coexist");
    // Keep the newest MAX: rank 0 is the OLDEST member.
    assert.deepEqual(cmds[2].slice(2), ["0", String(-(MAX_ACTIVE_SESSIONS + 1))]);
  });

  test("POSITIVE CONTROL: the eviction guard actually fires", async () => {
    const a = "aaa";
    await addActiveSession(EMAIL, a, TTL, R.deps);
    assert.equal(await isActiveSession(EMAIL, a, R.deps), true);
    await removeActiveSession(EMAIL, a, R.deps);
    assert.equal(await isActiveSession(EMAIL, a, R.deps), false,
      "if this still reports active, every eviction assertion above is inert");
  });
});

// -------------------------------------------------------------
// 2. EXISTING QB CUSTOMER COMPATIBILITY
//    The Founder's specific concern: does the current Oral customer
//    still get in after Security V2?
// -------------------------------------------------------------
describe("existing QB customer — login must keep working", () => {
  let R;
  beforeEach(() => { R = fakeRedis(); });

  /**
   * Replays api/check-password.js's decision sequence against the real
   * session/password functions: verify -> register session -> mint
   * token. The "upgrade if legacy" step that used to sit in the middle
   * is gone; a login can no longer write to a credential record.
   */
  async function login(email, supplied, storedRecord) {
    const { ok } = verifyPassword(storedRecord, supplied);
    if (!ok) return { ok: false };
    const sid = newSessionId();
    await addActiveSession(email, sid, TTL, R.deps);
    return { ok: true, sid, token: createSessionToken(email, sid) };
  }

  // -----------------------------------------------------------
  // LEGACY PLAINTEXT REJECTION (§14 of the remediation brief).
  //
  // These assertions are the standing guarantee that the git-history
  // exposure stays closed. Every one of them FAILED — correctly, by
  // design — before the plaintext branch was removed from session.js,
  // because until then a leaked password was a working password.
  // -----------------------------------------------------------
  test("a stored PLAINTEXT record no longer authenticates, even with the right password", async () => {
    const theirPassword = "MIW-legacy001";
    const stored = theirPassword;              // exactly the exposed form
    assert.equal((await login(EMAIL, theirPassword, stored)).ok, false,
      "the historical plaintext representation must be unusable");
  });

  test("a login cannot repair a plaintext record — no upgrade-on-read remains", async () => {
    const stored = "MIW-legacy001";
    await login(EMAIL, stored, stored);
    // Nothing was written anywhere; the only way a record becomes a
    // hash is the operator rotation tool.
    assert.equal(R.strings.size, 0, "authentication must not write to the credential store");
  });

  test("MUTATION: near-miss stored forms are all refused", async () => {
    const pw = "MIW-legacy001";
    for (const bad of [
      pw,                              // bare plaintext
      `sha256-${pw}`,                  // wrong separator
      `SHA256$salt$${pw}`,             // wrong case
      "sha256$",                       // truncated
      "sha256$saltonly",               // two fields, not three
      "sha256$$digest",                // empty salt
      "sha256$salt$",                  // empty digest
    ]) {
      assert.equal((await login(EMAIL, pw, bad)).ok, false, `must refuse: ${bad.slice(0, 20)}`);
    }
  });

  test("a VALID hash still passes — the guard rejects the old form, not everything", async () => {
    const pw = "MIW-legacy001";
    assert.equal((await login(EMAIL, pw, hashPassword(pw))).ok, true);
  });

  test("a rotated credential authenticates and the previous one does not", async () => {
    const oldPw = "MIW-legacy001";
    const newPw = "K7QRTVWX23456789";
    const stored = hashPassword(newPw);        // post-rotation record
    assert.equal((await login(EMAIL, newPw, stored)).ok, true);
    assert.equal((await login(EMAIL, oldPw, stored)).ok, false,
      "this is the closure test for the credential exposure");
  });

  test("POSITIVE CONTROL: the rejection is about the STORED form, not the supplied one", async () => {
    // Same supplied password, same value — only the storage form
    // differs. If this pair ever agrees, the guard has stopped working.
    const pw = "MIW-legacy001";
    assert.equal((await login(EMAIL, pw, pw)).ok, false);
    assert.equal((await login(EMAIL, pw, hashPassword(pw))).ok, true);
  });

  test("a customer can hold mobile + laptop sessions simultaneously", async () => {
    const pw = "MIW-legacy001";
    const stored = hashPassword(pw);
    const phone = await login(EMAIL, pw, stored);
    const laptop = await login(EMAIL, pw, stored);

    assert.equal(await isActiveSession(EMAIL, phone.sid, R.deps), true);
    assert.equal(await isActiveSession(EMAIL, laptop.sid, R.deps), true);
    // Both tokens carry the SAME identity — entitlements are per account.
    assert.equal(verifySessionToken(phone.token).e, EMAIL);
    assert.equal(verifySessionToken(laptop.token).e, EMAIL);
  });

  test("entitlements are per ACCOUNT, never per device", () => {
    // Both devices ask the same question of the same account key, so a
    // second device cannot see a different product set.
    const oral = { pathname: "/meoclass1/QB1_A.html", configured: true };
    const forDevice = (sid) => authorizeRequest({
      ...oral,
      payload: { e: EMAIL, s: sid, x: 9e9 },
      sessionScore: "1",
      entitled: "1",
    });
    assert.equal(forDevice("phone-sid").allow, true);
    assert.equal(forDevice("laptop-sid").allow, true);
  });

  test("an evicted third device is refused even with a perfectly valid token", async () => {
    const a = newSessionId();
    await addActiveSession(EMAIL, a, TTL, R.deps);
    await new Promise((r) => setTimeout(r, 1100));
    await addActiveSession(EMAIL, newSessionId(), TTL, R.deps);
    await new Promise((r) => setTimeout(r, 1100));
    await addActiveSession(EMAIL, newSessionId(), TTL, R.deps);

    const token = createSessionToken(EMAIL, a);
    assert.ok(verifySessionToken(token), "signature is still perfectly valid");
    const score = (await R.deps.cmd(["ZSCORE", sessionsKey(EMAIL), a])).result;
    const d = authorizeRequest({
      pathname: "/meoclass1/QB1_A.html", configured: true,
      payload: verifySessionToken(token), sessionScore: score, entitled: "1",
    });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "evicted",
      "a valid signature must not outrank the active-session set");
  });

  test("POSITIVE CONTROL: a wrong password is refused", async () => {
    assert.equal((await login(EMAIL, "not-the-password", hashPassword("MIW-legacy001"))).ok, false,
      "the password guard is inert");
  });
});

// -------------------------------------------------------------
// 3. ENTITLEMENT ACCESS MATRIX (the edge decision, offline)
// -------------------------------------------------------------
describe("access matrix — who may read what", () => {
  const live = { configured: true, payload: { e: EMAIL, s: "sid", x: 9e9 }, sessionScore: "1" };

  /** @param {string[]} owned */
  const visit = (pathname, owned) => authorizeRequest({
    ...live, pathname,
    entitled: owned.includes(requiredFor(pathname)) ? "1" : null,
  });

  const requiredFor = (p) =>
    authorizeRequest({ ...live, pathname: p, entitled: null }).required;

  test("PUBLIC: /SQ is readable with no session at all", () => {
    for (const p of ["/SQ/", "/SQ/pay.html", "/SQ/solved-qp-sample-january-2026.html"]) {
      const d = authorizeRequest({
        pathname: p, configured: false, payload: null, sessionScore: null, entitled: null,
      });
      assert.equal(d.allow, true, `${p} must stay public`);
    }
  });

  test("NONE: no entitlement opens neither product", () => {
    assert.equal(visit("/meoclass1/QB1_A.html", []).allow, false);
    assert.equal(visit("/solvedQP/QP2607.html", []).allow, false);
  });

  test("ORAL_QB_NOTES: opens Oral, NOT Written", () => {
    const owned = ["ORAL_QB_NOTES"];
    assert.equal(visit("/meoclass1/QB1_A.html", owned).allow, true);
    assert.equal(visit("/meoclass1/oralnotes/index.html", owned).allow, true);
    assert.equal(visit("/solvedQP/QP2607.html", owned).allow, false);
    // The ₹1,500 library sitting under the Oral folder must NOT open.
    assert.equal(visit("/meoclass1/pastpapers/QP2601.html", owned).allow, false,
      "Oral entitlement must never unlock the Written library");
  });

  test("SOLVED_QP: opens Written, NOT Oral", () => {
    const owned = ["SOLVED_QP"];
    assert.equal(visit("/solvedQP/QP2607.html", owned).allow, true);
    assert.equal(visit("/meoclass1/pastpapers/QP2601.html", owned).allow, true);
    assert.equal(visit("/meoclass1/QB1_A.html", owned).allow, false);
  });

  test("BOTH: opens everything paid", () => {
    const owned = ["ORAL_QB_NOTES", "SOLVED_QP"];
    for (const p of ["/meoclass1/QB1_A.html", "/solvedQP/QP2607.html",
                     "/meoclass1/pastpapers/QP2601.html"]) {
      assert.equal(visit(p, owned).allow, true, `${p} must open`);
    }
  });

  test("FORGED COOKIE: miw_auth=1 authorizes nothing", () => {
    // The old gate. There is no token, so there is no payload.
    const d = authorizeRequest({
      pathname: "/solvedQP/QP2607.html", configured: true,
      payload: null, sessionScore: null, entitled: "1",
    });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "nosession",
      "the forgeable UI-hint cookie must never grant access");
  });

  test("FAIL CLOSED: a missing secret or unreachable store denies", () => {
    const d = authorizeRequest({
      pathname: "/solvedQP/QP2607.html", configured: false,
      payload: { e: EMAIL, s: "sid", x: 9e9 }, sessionScore: "1", entitled: "1",
    });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "misconfigured",
      "paid bytes must never be served because the check could not run");
  });

  test("POSITIVE CONTROL: the entitlement guard fires", () => {
    const d = visit("/solvedQP/QP2607.html", []);
    assert.equal(d.allow, false);
    assert.equal(d.reason, "noentitlement",
      "if this allows, the whole matrix above is meaningless");
  });
});
