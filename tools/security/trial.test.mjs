// =============================================================
// Marine Intelligence Weekly — Free trial test suite
// Run: node --test tools/security/
//
// Offline by design, exactly like security.test.mjs beside it: no
// network, no Redis, no SMTP, no secrets. The REAL decision logic in
// api/_lib/ is what gets exercised.
//
// Each block ends with a POSITIVE CONTROL — a deliberately bad fixture
// that must be REJECTED — because a guard that never fires is not a
// guard.
//
// The letters in the test names map to the Founder's acceptance matrix
// so a reader can check coverage against it directly. The rows that
// need a live browser or a real payment (Chrome autofill, Razorpay
// capture) are proven elsewhere and are named at the bottom of this
// file rather than silently omitted.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const {
  TRIAL_HOURS, INDEPENDENCE_DAY, IST_OFFSET_MINUTES,
  istDateString, isIndependenceDayActivation, trialDurationHours,
  trialExpiryFor, trialState, trialGrantsAccess, trialOffer, trialKey,
  isTrialProduct, TRIAL_AVAILABLE, TRIAL_ACTIVE, TRIAL_EXPIRED,
} = await import("../../api/_lib/trial.js");

const { authorizeRequest, requiredEntitlementForPath } =
  await import("../../api/_lib/routes.js");
const { sessionCookies, UI_FLAG_COOKIE } = await import("../../api/_lib/session.js");
const {
  requestTrialAccount, SIGNUP_RESPONSE, signupThrottleKey, GENERIC_RESPONSE,
} = await import("../../api/_lib/reset.js");
const { userKey } = await import("../../api/_lib/entitlements.js");

const HOUR = 3600;

/** Epoch ms for an IST wall-clock time, built from the fixed offset. */
function ist(dateTime) {
  return Date.parse(dateTime + "+05:30");
}

// -------------------------------------------------------------
// 1. DURATIONS — the Founder-frozen numbers
// -------------------------------------------------------------
describe("trial durations", () => {

  test("G/H: both products offer a 12-hour trial by default", () => {
    const ordinary = ist("2026-09-20T10:00:00");
    assert.equal(trialDurationHours("ORAL_QB_NOTES", ordinary), 12);
    assert.equal(trialDurationHours("SOLVED_QP", ordinary), 12);
  });

  test("G: a 12-hour grant expires exactly 12 hours later", () => {
    const now = ist("2026-09-20T10:00:00");
    assert.equal(trialExpiryFor("ORAL_QB_NOTES", now), Math.floor(now / 1000) + 12 * HOUR);
  });

  test("I: SolvedQP activated on 15 August IST gets 24 hours", () => {
    const now = ist("2026-08-15T09:00:00");
    assert.equal(trialDurationHours("SOLVED_QP", now), 24);
    assert.equal(trialExpiryFor("SOLVED_QP", now), Math.floor(now / 1000) + 24 * HOUR);
  });

  test("I: the campaign is SolvedQP only — Oral stays 12h on 15 August", () => {
    const now = ist("2026-08-15T09:00:00");
    assert.equal(trialDurationHours("ORAL_QB_NOTES", now), 12,
      "the Independence Day offer was approved for SolvedQP alone");
  });

  test("J: activation at 23:59 IST on the 15th still gets a FULL 24 hours", () => {
    // The offer is 24 hours from activation, NOT "until midnight".
    const now = ist("2026-08-15T23:59:00");
    assert.equal(trialDurationHours("SOLVED_QP", now), 24);
    const expiry = trialExpiryFor("SOLVED_QP", now);
    assert.equal(expiry, Math.floor(ist("2026-08-16T23:59:00") / 1000),
      "must run into the 16th rather than being truncated at midnight");
  });

  test("J: activation at 00:01 IST on the 15th is eligible", () => {
    // 00:01 IST on the 15th is still 14 August in UTC. Deciding
    // eligibility in UTC would wrongly give this candidate 12 hours.
    const now = ist("2026-08-15T00:01:00");
    assert.equal(new Date(now).toISOString().slice(0, 10), "2026-08-14",
      "fixture must actually straddle the UTC date boundary, or it proves nothing");
    assert.equal(trialDurationHours("SOLVED_QP", now), 24);
  });

  test("the campaign switches itself off — 16 August is 12 hours again", () => {
    assert.equal(trialDurationHours("SOLVED_QP", ist("2026-08-16T00:01:00")), 12);
    assert.equal(trialDurationHours("SOLVED_QP", ist("2026-08-14T23:59:00")), 12);
  });

  test("IST is UTC+05:30 and the date helper reads the IST wall clock", () => {
    assert.equal(IST_OFFSET_MINUTES, 330);
    assert.equal(istDateString(ist("2026-08-15T00:00:00")), "2026-08-15");
    assert.equal(istDateString(ist("2026-08-15T23:59:59")), "2026-08-15");
    assert.equal(istDateString(ist("2026-08-16T00:00:00")), "2026-08-16");
  });

  test("POSITIVE CONTROL: the 24-hour window is not open on an ordinary day", () => {
    assert.equal(isIndependenceDayActivation("SOLVED_QP", ist("2026-09-01T12:00:00")), false);
    assert.notEqual(trialDurationHours("SOLVED_QP", ist("2026-09-01T12:00:00")), 24,
      "a permanently-24h SolvedQP trial would be undetectable to the other tests");
    assert.equal(INDEPENDENCE_DAY.hours, 24);
    assert.equal(TRIAL_HOURS.SOLVED_QP, 12, "the NORMAL trial must stay 12 hours");
  });

  test("unknown products are offered no trial at all", () => {
    assert.equal(trialDurationHours("BUNDLE", Date.now()), null);
    assert.equal(trialDurationHours("FREE_STUFF", Date.now()), null);
    assert.equal(isTrialProduct("BUNDLE"), false);
    assert.equal(isTrialProduct("SOLVED_QP"), true);
  });
});

// -------------------------------------------------------------
// 2. STATE DERIVATION — one field, three states
// -------------------------------------------------------------
describe("trial state", () => {
  const now = 1_800_000_000;

  test("an absent field means the trial is still available", () => {
    for (const raw of [null, undefined, ""]) {
      assert.equal(trialState(raw, now).status, TRIAL_AVAILABLE);
    }
  });

  test("a future expiry is active and reports the remaining seconds", () => {
    const s = trialState(String(now + 5 * HOUR), now);
    assert.equal(s.status, TRIAL_ACTIVE);
    assert.equal(s.secondsRemaining, 5 * HOUR);
  });

  test("K: a past expiry is expired, and stays expired", () => {
    assert.equal(trialState(String(now - 1), now).status, TRIAL_EXPIRED);
    assert.equal(trialState(String(now - 400 * 24 * HOUR), now).status, TRIAL_EXPIRED);
  });

  test("the boundary second is exact: expiry == now is over", () => {
    assert.equal(trialState(String(now + 1), now).status, TRIAL_ACTIVE);
    assert.equal(trialState(String(now), now).status, TRIAL_EXPIRED);
  });

  test("a corrupt value fails CLOSED, not open", () => {
    // HSETNX will refuse to overwrite whatever is in there, so calling
    // it "available" would advertise a trial that cannot be started.
    for (const raw of ["banana", "NaN", "-1", "0"]) {
      assert.equal(trialState(raw, now).status, TRIAL_EXPIRED,
        `${raw} must not read as an available trial`);
    }
  });

  test("Q: the state comes from the STORE, so a cleared browser changes nothing", () => {
    // There is no input to any of this that a browser controls. The
    // only argument other than the stored value is the server's clock.
    const spent = String(now - 1);
    assert.equal(trialGrantsAccess(spent, now), false);
    assert.equal(trialState(spent, now).status, TRIAL_EXPIRED);
  });

  test("POSITIVE CONTROL: an active trial is distinguishable from an expired one", () => {
    assert.notEqual(
      trialState(String(now + HOUR), now).status,
      trialState(String(now - HOUR), now).status,
      "if these collapsed, every expiry test above would pass vacuously"
    );
  });
});

// -------------------------------------------------------------
// 3. AUTHORIZATION — the deny/allow matrix, as the edge runs it
// -------------------------------------------------------------
describe("authorizeRequest with trials", () => {
  const now = 1_800_000_000;
  const base = {
    pathname: "/solvedQP/index.html",
    configured: true,
    payload: { e: "cand@example.com", s: "sess-1", x: now + 9999 },
    sessionScore: "1700000000",
    now,
  };

  test("A/B: an anonymous request is denied regardless of trial state", () => {
    const d = authorizeRequest({ ...base, payload: null, trialExpiry: String(now + HOUR) });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "nosession");
  });

  test("a running trial opens the paid route", () => {
    const d = authorizeRequest({ ...base, entitled: null, trialExpiry: String(now + HOUR) });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "trial");
  });

  test("K/U: an expired trial denies, and says so distinctly", () => {
    const d = authorizeRequest({ ...base, entitled: null, trialExpiry: String(now - 1) });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "trialexpired",
      "the candidate must be told the trial ended, not that they never had access");
  });

  test("F: no entitlement and no trial is still the plain denial", () => {
    const d = authorizeRequest({ ...base, entitled: null, trialExpiry: null });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "noentitlement");
  });

  test("N/V: a PAID customer is unaffected by an expired trial", () => {
    const d = authorizeRequest({ ...base, entitled: "1", trialExpiry: String(now - 99999) });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "ok", "paid access must not be reported as a trial");
  });

  test("O: buying during a trial yields durable paid access", () => {
    // The entitlement lands; the trial row is left exactly as it was.
    // Once expiry passes, the customer still gets in — via `ok`.
    const afterExpiry = now + 100 * HOUR;
    const d = authorizeRequest({
      ...base, now: afterExpiry,
      payload: { ...base.payload, x: afterExpiry + 9999 },
      entitled: "1", trialExpiry: String(now + HOUR),
    });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "ok");
  });

  test("V: a paid customer who never took a trial is unchanged", () => {
    const d = authorizeRequest({ ...base, entitled: "1", trialExpiry: null });
    assert.equal(d.allow, true);
    assert.equal(d.reason, "ok");
  });

  test("an evicted session cannot be rescued by an active trial", () => {
    const d = authorizeRequest({
      ...base, sessionScore: null, entitled: null, trialExpiry: String(now + HOUR),
    });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "evicted");
  });

  test("a misconfigured edge denies even a valid running trial", () => {
    const d = authorizeRequest({
      ...base, configured: false, entitled: null, trialExpiry: String(now + HOUR),
    });
    assert.equal(d.allow, false);
    assert.equal(d.reason, "misconfigured");
  });

  test("L/M: the trial is read per-product, so one cannot spend the other", () => {
    // The edge asks for exactly ONE field — the one this path requires.
    // An Oral trial is simply not consulted on a Written path.
    const oralTrialOnly = { ORAL_QB_NOTES: String(now + HOUR) };

    const written = authorizeRequest({
      ...base, pathname: "/solvedQP/index.html",
      entitled: null, trialExpiry: oralTrialOnly.SOLVED_QP ?? null,
    });
    assert.equal(written.allow, false, "an Oral trial must not open Written content");
    assert.equal(written.required, "SOLVED_QP");

    const oral = authorizeRequest({
      ...base, pathname: "/meoclass1/index.html",
      entitled: null, trialExpiry: oralTrialOnly.ORAL_QB_NOTES,
    });
    assert.equal(oral.allow, true);
    assert.equal(oral.required, "ORAL_QB_NOTES");
  });

  test("the Written build folder under /meoclass1/ still requires SOLVED_QP", () => {
    const d = authorizeRequest({
      ...base, pathname: "/meoclass1/pastpapers/QP2601.html",
      entitled: null, trialExpiry: String(now + HOUR),
    });
    // Allowed because the SOLVED_QP trial is what was passed — the
    // point is that `required` resolved to SOLVED_QP, not Oral.
    assert.equal(d.required, "SOLVED_QP");
  });

  test("public paths are untouched by any of this", () => {
    for (const p of ["/SQ/trial.html", "/SQ/pay.html", "/api/trial", "/index.html"]) {
      const d = authorizeRequest({ ...base, pathname: p, entitled: null, trialExpiry: null });
      assert.equal(d.allow, true);
      assert.equal(d.reason, "public");
    }
  });

  test("POSITIVE CONTROL: the trial branch can actually deny", () => {
    // If trialGrantsAccess ever returned true unconditionally, every
    // allow-test above would still pass. This is the one that breaks.
    const d = authorizeRequest({ ...base, entitled: null, trialExpiry: null });
    assert.equal(d.allow, false,
      "no entitlement and no trial must NEVER open a paid route");
  });

  test("POSITIVE CONTROL: a browser-supplied future clock cannot help", () => {
    // `now` is injected by middleware from the server clock. Passing a
    // stale expiry with an honest clock denies; the only way to flip it
    // is to change the STORED value, which the browser cannot reach.
    const honest = authorizeRequest({ ...base, entitled: null, trialExpiry: String(now - 1) });
    assert.equal(honest.allow, false);
  });
});

// -------------------------------------------------------------
// 4. THE OFFER SHOWN TO A CANDIDATE
// -------------------------------------------------------------
describe("trialOffer — what the UI is allowed to render", () => {

  test("an owner is never shown trial state", () => {
    const o = trialOffer("SOLVED_QP", {
      owned: true, raw: String(Math.floor(Date.now() / 1000) - 5), nowMs: Date.now(),
    });
    assert.equal(o.status, "owned");
    assert.equal(o.secondsRemaining, 0);
  });

  test("an untouched product offers its hours", () => {
    const nowMs = ist("2026-08-15T20:30:00");
    const o = trialOffer("SOLVED_QP", { owned: false, raw: null, nowMs });
    assert.equal(o.status, "available");
    assert.equal(o.offerHours, 24);
    assert.equal(o.independenceDay, true);
  });

  test("the key is namespaced per account and lower-cased", () => {
    assert.equal(trialKey(" Cand@Example.COM "), "miw:trial:cand@example.com");
  });
});

// -------------------------------------------------------------
// 5. ACCOUNT CREATION FOR TRIAL CANDIDATES
//
// The dangerous property is not "can a candidate get a password" but
// "can a stranger reset a paying customer's password from this form".
// -------------------------------------------------------------
describe("requestTrialAccount", () => {

  function makeStore({ users = {}, claims = {} } = {}) {
    const store = {
      users: { ...users },
      claims: { ...claims },
      get: async (k) => store.users[k] ?? null,
      del: async (k) => { delete store.claims[k]; return 1; },
      claim: async (k) => {
        if (store.claims[k]) return false;
        store.claims[k] = "1";
        return true;
      },
      createNX: async (k, v) => {
        if (store.users[k] !== undefined) return false;
        store.users[k] = v;
        return true;
      },
    };
    return store;
  }

  const buildEmail = (to, password) => ({ to, password, subject: "Your MIW password" });

  test("a new address gets an account and a password", async () => {
    const store = makeStore();
    const sent = [];
    const r = await requestTrialAccount({
      email: "New@Example.com", store,
      sendMail: async (m) => sent.push(m),
      buildEmail, makePassword: () => "PW-TEST-000000",
    });
    assert.equal(r.outcome, "created");
    assert.equal(sent.length, 1);
    assert.equal(sent[0].to, "new@example.com");
    // The password is delivered, but only a HASH is stored.
    const stored = store.users[userKey("new@example.com")];
    assert.match(stored, /^sha256\$/);
    assert.ok(!stored.includes("PW-TEST-000000"), "plaintext must never be stored");
  });

  test("SECURITY: an EXISTING account is never touched and never emailed", async () => {
    // This is the attack: type a customer's address into the trial
    // signup box and hope it rotates their password.
    const store = makeStore({ users: { [userKey("paid@example.com")]: "sha256$abc$def" } });
    const sent = [];
    const r = await requestTrialAccount({
      email: "paid@example.com", store,
      sendMail: async (m) => sent.push(m), buildEmail,
    });
    assert.equal(r.outcome, "existing_account");
    assert.equal(sent.length, 0, "an existing customer must receive nothing");
    assert.equal(store.users[userKey("paid@example.com")], "sha256$abc$def",
      "the stored credential must be byte-identical afterwards");
  });

  test("throttled: one attempt per address per window", async () => {
    const store = makeStore();
    const first = await requestTrialAccount({
      email: "a@b.com", store, sendMail: async () => {}, buildEmail,
    });
    const second = await requestTrialAccount({
      email: "a@b.com", store, sendMail: async () => {}, buildEmail,
    });
    assert.equal(first.outcome, "created");
    assert.equal(second.outcome, "throttled");
  });

  test("the throttle is claimed BEFORE the existence check", async () => {
    // Otherwise "no account" is fast and "throttled" is slow, and the
    // timing difference enumerates customers.
    const store = makeStore({ users: { [userKey("paid@example.com")]: "sha256$a$b" } });
    await requestTrialAccount({
      email: "paid@example.com", store, sendMail: async () => {}, buildEmail,
    });
    assert.ok(store.claims[signupThrottleKey("paid@example.com")],
      "an existing account must still consume the throttle slot");
  });

  test("a lost create race sends no password", async () => {
    const store = makeStore();
    store.createNX = async () => false;   // somebody else won
    const sent = [];
    const r = await requestTrialAccount({
      email: "race@example.com", store, sendMail: async (m) => sent.push(m), buildEmail,
    });
    assert.equal(r.outcome, "race_lost");
    assert.equal(sent.length, 0, "sending a password that is not the stored one is worse than sending none");
  });

  test("malformed addresses are refused before Redis is touched", async () => {
    const store = makeStore();
    for (const bad of ["", "   ", "nope", "a@b", "a b@c.com", null, undefined]) {
      const r = await requestTrialAccount({
        email: bad, store, sendMail: async () => {}, buildEmail,
      });
      assert.equal(r.outcome, "invalid_email");
    }
    assert.equal(Object.keys(store.claims).length, 0);
  });

  test("NO ENUMERATION: every outcome maps to one identical sentence", () => {
    // The endpoint returns SIGNUP_RESPONSE unconditionally. This pins
    // the fact that the message says nothing about which path ran.
    assert.ok(!/exists|already registered|not found|no account/i.test(SIGNUP_RESPONSE));
    assert.ok(SIGNUP_RESPONSE.length > 40);
    assert.notEqual(SIGNUP_RESPONSE, GENERIC_RESPONSE,
      "signup and reset are different asks and may read differently, " +
      "but each must be constant across its own outcomes");
  });

  test("POSITIVE CONTROL: the existing-account guard can be seen to fire", async () => {
    const empty = makeStore();
    const occupied = makeStore({ users: { [userKey("x@y.com")]: "sha256$a$b" } });
    const a = await requestTrialAccount({
      email: "x@y.com", store: empty, sendMail: async () => {}, buildEmail,
    });
    const b = await requestTrialAccount({
      email: "x@y.com", store: occupied, sendMail: async () => {}, buildEmail,
    });
    assert.notEqual(a.outcome, b.outcome,
      "if these matched, the guard would be untested in both directions");
  });
});

// -------------------------------------------------------------
// 6. THE miw_auth COUPLING
//
// 164 pages under /meoclass1/ still open with a legacy client-side
// gate: read document.cookie, and if miw_auth is not "1", redirect to
// /SQ/pay.html. It is the pre-Security-V2 mechanism, and it is NOT
// security -- middleware.js refuses to read that cookie, every one of
// those paths is behind the /meoclass1/:path* matcher, and the gate is
// one line of JavaScript to forge. It protects nothing and, because
// the bytes are never served to an unauthorised request in the first
// place, it exposes nothing either.
//
// What it IS is a tripwire. The cookie is a UI hint set by
// sessionCookies(). If a future change stops setting it -- tightening
// SameSite, dropping the "redundant" second cookie, moving login --
// then middleware will correctly ALLOW a paying customer or a trial
// candidate, the page will be served, and the page will then throw
// them out from the client. 164 pages would break at once, for
// legitimate users only, with the gate that caused it invisible to
// every server-side test we have.
//
// So the coupling is pinned here rather than left implicit. Deleting
// the 164 gates is the cleaner end state and is worth doing on its own
// terms; until then this test is what makes the dependency loud.
// -------------------------------------------------------------
describe("legacy miw_auth UI hint", () => {

  test("a fresh login still sets the cookie 164 Oral pages read", () => {
    const cookies = sessionCookies("v1.payload.signature");
    const hint = cookies.find((c) => c.startsWith(UI_FLAG_COOKIE + "="));
    assert.ok(hint, `login must keep setting ${UI_FLAG_COOKIE} or 164 pages under ` +
      "/meoclass1/ will bounce signed-in customers and trial users client-side");
    assert.match(hint, /^miw_auth=1;/, "the pages compare it to exactly \"1\"");
    assert.match(hint, /Path=\//, "it must be readable on /meoclass1/, not just /SQ/");
    assert.ok(!/HttpOnly/.test(hint),
      "those gates read it from document.cookie, so it cannot be HttpOnly");
  });

  test("the session cookie, unlike the hint, IS HttpOnly", () => {
    const cookies = sessionCookies("v1.payload.signature");
    const session = cookies.find((c) => c.startsWith("miw_session="));
    assert.match(session, /HttpOnly/, "the real credential must stay unreadable");
  });

  test("the hint carries no authority: every gated path is middleware-protected", () => {
    // The reason the forgeable cookie is harmless. If any of these ever
    // resolved to null, that path would be served to anyone and the
    // client-side gate would become the only thing standing there.
    for (const p of ["/meoclass1/", "/meoclass1/QB10_B.html",
                     "/meoclass1/oralnotes/x.html", "/meoclass1/pastpapers/QP2601.html"]) {
      assert.ok(requiredEntitlementForPath(p),
        `${p} must require an entitlement at the edge`);
    }
  });

  test("POSITIVE CONTROL: the cookie name the pages read has not drifted", () => {
    assert.equal(UI_FLAG_COOKIE, "miw_auth",
      "renaming this constant silently breaks 164 pages that hardcode the old name");
  });
});

// -------------------------------------------------------------
// 7. COVERAGE NOTE — rows of the matrix NOT provable here
//
// Stating them is the point. A suite that quietly omits them reads as
// though it covered everything.
//
//   C/D/E  signed-in hub rendering for each ownership combination
//   R/S/T  no auto-open after login; `next` only highlights; Chrome
//          autofill cannot route the candidate
//          -> browser pass against a served build; the redirect itself
//             is gone from SQ/pay.html, which is the durable proof.
//   O      real Razorpay capture during an active trial
//          -> fulfilPayment is covered in security.test.mjs; no live
//             purchase is made to prove a flow.
//   P      logout/login preserving trial state
//          -> follows from the store: the trial row is keyed by email
//             and no login path writes miw:trial:*. Asserted indirectly
//             by "Q" above.
// -------------------------------------------------------------
