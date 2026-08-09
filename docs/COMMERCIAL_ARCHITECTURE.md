# MIW Commercial Architecture — Security V2

Status: **on branch `commerce/solvedqp-security-v2`, awaiting Founder review.
Nothing merged to `main`.**

---

## 1. Product layout

Three sibling surfaces at the site root. `/solvedQP/` is **not** inside
`/meoclass1/`.

```
/
├── SQ/           PUBLIC   storefront, free samples, login, product hub
├── meoclass1/    PAID     Oral QB + Notes          → ORAL_QB_NOTES
└── solvedQP/     PAID     Solved Written papers    → SOLVED_QP
```

They share one `api/`, one Redis, one session, one Razorpay account and one
Brevo sender — but **entitlements are separate**. Owning one product never
opens the other.

---

## 2. What was wrong

Established by reading the code, not by assumption:

| # | Defect | Evidence |
|---|--------|----------|
| 1 | No server-side gate existed at all | no `middleware.js`, no `vercel.json` |
| 2 | Paid pages "gated" themselves in the browser | `if(!/miw_auth=1/.test(document.cookie)) location.replace(...)` in 171 files — runs *after* the full document is delivered |
| 3 | The auth cookie was forgeable and anonymous | `miw_auth=1` — readable, unsigned, no identity |
| 4 | The browser set the price | `create-order.js`: `Math.round(amount * 100)` from the request body |
| 5 | Payment verification never checked the amount | `verify-payment.js` trusted `tier` from the request body |
| 6 | No per-product entitlement existed | nothing in Redis beyond a password |
| 7 | Passwords were stored in plaintext | `miw:user:<email>` = the password itself |
| 8 | The raw password was kept in the browser | `localStorage.setItem('miw_auth', JSON.stringify({email, pwd, expiry}))` |
| 9 | The Written papers were already public | `meoclass1/pastpapers/QP2601.html`, 512 KB of complete answers, ungated |

The combination that mattered: **a ₹1 payment with `tier:"founders"` in the
JSON produced full access, and the Razorpay signature was valid** — because a
signature proves a payment belongs to an order, and says nothing about price.

---

## 3. What protects it now

### The boundary

`middleware.js` — Vercel **Edge Middleware**, which runs *before* static file
serving. An unauthorized request is answered with a 302 and the protected
bytes are never read from the CDN.

Per request to a protected path:

1. verify the HMAC-signed session token (Web Crypto);
2. one Upstash pipeline call → `ZSCORE` on the session set + the required
   entitlement;
3. the session id must still be a member of the account's set (**up to two**
   live sessions — mobile + laptop);
4. entitlement field must be `"1"`;
5. otherwise redirect to `/SQ/pay.html?next=…&reason=…`.

It **fails closed**: a missing secret or unreachable Redis denies. It never
reads `miw_auth`.

### Route policy — `api/_lib/routes.js`

One definition, shared by middleware and the tests.

| Path | Requires |
|------|----------|
| `/solvedQP/*` | `SOLVED_QP` |
| `/meoclass1/pastpapers/*` | `SOLVED_QP` |
| `/meoclass1/oralnotes/*` | `ORAL_QB_NOTES` |
| `/meoclass1/*` | `ORAL_QB_NOTES` |
| `/SQ/*`, `/api/*`, everything else | public |

`/meoclass1/pastpapers/` maps to **SOLVED_QP** deliberately: it holds the
built Written papers. Mapping it to the Oral entitlement would hand the whole
₹1,500 library to every Oral customer.

Every `.html` under `/meoclass1/` was checked individually — all carry
`noindex`, so there is no free page to carve out.

### Session — `api/_lib/session.js`

`v1.<base64url(payload)>.<base64url(HMAC-SHA256)>`, payload `{e, s, x}` =
email, session id, expiry. Signed with `MIW_SESSION_SECRET`.

- `miw_session` — **HttpOnly, Secure, SameSite=Lax, 30 days**. The authority.
- `miw_auth=1` — retained as a readable UI hint. Authorizes nothing.

Passwords: new accounts are stored `sha256$salt$hash`. Legacy plaintext
records still verify and are **transparently upgraded on next login**, so no
customer is locked out.

### Two active sessions — `api/_lib/sessions.js`

**Founder policy: a customer may stay signed in on TWO devices** (typically a
mobile and a laptop). This is a standing commitment to existing customers, and
it overrides the earlier single-session draft.

| Event | Result |
|---|---|
| Login A | A valid |
| Login B | A **and** B valid |
| Login C | oldest (A) retired; B and C valid |
| Logout on B | B invalid; C still valid |
| Expired / tampered token | invalid |

`miw:sessions:<email>` is a **sorted set**: member = session id, score = login
time. Login runs one pipeline — prune by score, `ZADD`, trim to the newest two
(`ZREMRANGEBYRANK key 0 -3`), refresh TTL, delete the superseded
`miw:active_session` key. Trimming *after* adding is what enforces the cap.
Two concurrent logins converge on "the newest two" under every interleaving,
so no transaction is required.

Authorization is one `ZSCORE` — the same single-command cost as the previous
single-session `GET`. **There is no device fingerprinting**: the server counts
independent session ids and nothing more.

Entitlements are per **account**, never per device. Both sessions see exactly
the same product set. Logout signs out only the calling device;
`{action:"logout", scope:"all"}` signs out everywhere and is what credential
rotation must use.

The decision itself lives in `api/_lib/routes.js` as `authorizeRequest()`, a
pure function, so the full deny/allow matrix is proven offline in
`tools/security/sessions.test.mjs` exactly as it runs at the edge.

### Entitlements — Redis

```
miw:ent:<email>              HASH   ORAL_QB_NOTES = "1", SOLVED_QP = "1"
miw:sessions:<email>         ZSET   up to TWO live session ids,
                                    member = session id, score = login epoch
miw:user:<email>             STRING sha256$salt$hash (legacy: plaintext)
miw:send_lock:<paymentId>    STRING fulfilment idempotency claim
```

A HASH, not a JSON blob, because `HSET` on one field is additive, idempotent
and race-free — a Written purchase cannot clobber an Oral grant when the
webhook and the client callback fire concurrently. **Absence means no
access; there is no default-true.**

`BUNDLE` is not a third authorization mechanism. It is a SKU that grants both
atomic entitlements. Middleware only ever asks about `ORAL_QB_NOTES` and
`SOLVED_QP`. No bundle price is approved, so `create-order` refuses it.

---

## 4. Money

### Catalogue — `api/_lib/products.js`

The only place a price is decided.

| Product | Tier | Amount | Display |
|---------|------|--------|---------|
| `ORAL_QB_NOTES` | standard | `149900` paise | ₹1,499 |
| `ORAL_QB_NOTES` | founders | `89900` paise | ₹899 |
| `SOLVED_QP` | standard | **`150000` paise** | **₹1,500** |

Oral amounts are the existing approved prices, relocated — not a pricing
change.

### create-order

Takes a **product**, not an amount. Any `amount` in the body is logged and
discarded. Writes `product`, `tier`, `buyer_email` into Razorpay **order
notes**, which only the server can set.

### Fulfilment — `api/_lib/fulfil.js`

Shared by `verify-payment.js` and `razorpay-webhook.js`, so the two can no
longer drift. After the caller verifies the signature, fulfilment
independently re-reads the order **and** the payment from Razorpay and checks:

- product and tier come from server-authored order notes;
- the amount matches the catalogue for that product/tier;
- currency is INR;
- the payment is `captured` and belongs to that order.

Any mismatch throws and grants nothing. Then: claim `miw:send_lock:<paymentId>`
(NX, exactly one winner), grant additively, email once.

**On failure inside the lock, the lock is released** so a Razorpay retry can
genuinely re-attempt. The old code left it claimed, which silently blocked
retries until someone cleared the key by hand.

---

## 5. One answer truth

```
                    meoclass1/pastpapers/specs/*.json
                                 │
     ┌───────────────┬───────────┴────────────┬─────────────────────┐
     ▼               ▼                        ▼                     ▼
 review build   /solvedQP/ paid       SQ/ January teaser   oralnotes/ January
 (Founder)      (customer)            (public, 2 of 9)     promo (Oral subs)
```

All four are projections of the same specs. No answer text is copied or
separately edited. `build_paper.py` modes: default (review), `--deliver`
(paid), `--oral-promo` (Oral-subscriber sample).

### Third-party recurrence — fixed

The specs carry recurrence annotations copied from the third-party source
copy: sittings MIW has **never read** (each spec's own `recurrence_note` says
so). These were reaching candidates in three places — a "Recurrence recorded
on the source paper: 2018/APR…" note, a "12 prior sittings" tag, and the same
tokens baked into every page's invisible `data-search` payload.

All three are now review-build only. Candidates see recurrence MIW actually
verified: another MIW-built sitting whose wording was compared directly
("MIW has also built this question in July 2026"), from `reused_from`.

`recurrence_class` is an authoring verdict and no longer reaches a candidate
in any build, visible or in the search payload.

Provenance is **not deleted** from the editorial source — only the view
changed. `solvedqp_check.py` guards it.

---

## 6. Existing customers

`tools/security/migrate_entitlements.mjs` back-fills every existing account to
**`ORAL_QB_NOTES` only**. It has no code path that grants `SOLVED_QP` — those
accounts predate the Written product and nobody paid for it.

Dry run by default, additive, idempotent, masked output, nothing written to
the repository.

```bash
node tools/security/migrate_entitlements.mjs            # dry run
node tools/security/migrate_entitlements.mjs --apply    # execute
node tools/security/migrate_entitlements.mjs            # confirm: nothing to do
```

Rollback is per-account and deliberately manual: `HDEL miw:ent:<email> ORAL_QB_NOTES`.

Exceptional cases: `tools/security/entitlement_admin.mjs` (`show`, `grant`,
`revoke --confirm`, `logout`). Local script, **not** an endpoint — an
authenticated admin route would be a permanent attack surface for an
occasional problem.

---

## 7. Required environment

| Variable | Purpose | New? |
|----------|---------|------|
| `MIW_SESSION_SECRET` | signs session tokens (≥16 chars, random) | **YES — must be set before deploy** |
| `KV_REST_API_URL` / `KV_REST_API_TOKEN` | Upstash | existing |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | orders, verification | existing |
| `RAZORPAY_WEBHOOK_SECRET` | webhook signature | existing |
| `BREVO_SMTP_LOGIN` / `BREVO_SMTP_KEY` | email | existing |
| `QB_PASSWORD_POOL` | new-account credentials | existing |

`MIW_SESSION_SECRET` must be available to **both** the Edge runtime
(middleware) and the Node functions. Without it middleware fails closed and
denies everything, and login refuses to issue sessions.

---

## 8. Verification

```bash
npm run security:test                                  # 34 offline tests
python tools/pastpapers/run_toolchain.py --self-test   # full product build
```

Neither needs network, Redis, Razorpay or secrets.

Every guard is paired with a **positive control** — a deliberately bad fixture
that must be rejected — because a guard that cannot fail is not a guard.

---

## 9. Deliberately not done

- **No DRM.** Server gate = security. `noindex`, watermark and copy
  deterrence on the pages are deterrence only, and nothing relies on them.
- **No device fingerprinting.** Single active session is a Redis id
  comparison.
- **No bundle price.** None approved; `create-order` refuses `BUNDLE`.
- **No 2025 production.** Unchanged and untouched.

---

## 10. URGENT — two live credential-leaking endpoints, found and removed

Not named in the original audit. Both were live in production and both are in
a **public** GitHub repository.

### `api/check-db.js` — unauthenticated password oracle

```
GET /api/check-db?email=<anyone>   →   { "password": "<their password>" }
```

No authentication of any kind. Anyone who knew a customer's email address
could read that customer's password. The file's own first line called it a
"temporary debug endpoint, delete after use".

### `api/migrate-users.js` — 28 real customers' credentials in source

Contained **28 real customer email addresses and their plaintext passwords
hard-coded in the file**, in a public repository. Guarded only by a
hard-coded secret that is written in the same public file, so the guard was
decorative:

```
GET /api/migrate-users?secret=<the secret printed above it>
```

Calling it **reset all 28 accounts** to those passwords and echoed every
address and password back in the response body. It would also have silently
undone the password hashing introduced in this work, rewriting hashed
records back to plaintext.

### Action taken

Both files are deleted on this branch.

### Action the Founder must take — this cannot be fixed in code

Deleting the files stops them being served. It does **not** remove them from
git history, and this repository is public, so those 28 credentials must be
treated as **publicly disclosed**.

1. **Rotate all 28 passwords.** Issue new credentials and email them. Until
   then, anyone who has read the repository history can sign in as any of
   those 28 customers.
2. Decide separately whether to rewrite git history. It was **not** done here
   — this session was instructed not to rewrite history, and a force-push
   across a shared public repository is a decision for the repository owner,
   not an implementation detail.
3. The 28 addresses are real customer personal data. They are not reproduced
   in this document, in any commit message, or in any session output.

---

## 23. Status — 2026-08-09 (Security V2 preservation & handover session)

### 23a. CORRECTION: the exposure is not only in history

The section above says the two endpoints "are deleted on this branch". That is
true and it is not sufficient. Verified this session:

* `api/check-db.js` and `api/migrate-users.js` are **still present in the tree
  of `main`** (`f4d1058`), which is the branch production deploys.
* The deletion commit `76cc003` exists **only** on
  `commerce/solvedqp-security-v2`, which is **not merged**.
* The repository is **public** (confirmed via the GitHub API).

So the credential table is readable in the *current default branch* of a public
repository — not merely recoverable from history — and `/api/check-db` is
expected to still be deployed. That endpoint takes **no secret at all**:
`GET /api/check-db?email=<address>` returns that account's stored password.

**Consequence for sequencing:** rotating the 28 passwords while
`/api/check-db` is still live would simply disclose the *new* passwords by the
same mechanism. **Endpoint removal must come first.**

Recommended order, independent of the Solved QP launch schedule:

1. Remove both endpoints from `main`; redeploy production.
2. Confirm `/api/check-db` no longer resolves.
3. Back-fill entitlements (§23c step 3).
4. Rotate all 28 credentials and invalidate every session
   (`clearAllSessions`, i.e. `{action:"logout", scope:"all"}` semantics).
5. Notify affected customers.
6. Only then consider a history purge.

Steps 1–2 do not depend on Security V2, on the content roadmap, or on any
launch decision. They can be done at any time.

A private incident archive holding the exact historical files, a SHA-256
manifest and an incident record has been created **outside this repository**
so a future history purge can be considered without losing the reference. Its
contents are deliberately not described here and are not in Git.

### 23b. Session policy changed: ONE → TWO

Superseding the earlier single-session design. See "Two active sessions"
above. This honours the standing Founder promise that a customer may remain
signed in on both a mobile and a laptop.

### 23c. Production activation sequence — DEFERRED, do not execute early

Security V2 is **not** active in production and **must not** be activated
before the entitlement back-fill, or valid customers will authenticate
successfully and still be denied access.

1. Security code ready ✔ (this branch)
2. `MIW_SESSION_SECRET` configured in Vercel — Edge **and** Node runtimes
3. Entitlement migration prepared ✔ (`tools/security/migrate_entitlements.mjs`)
4. Controlled back-fill — dry run, then `--apply`
5. Validate an existing customer login
6. Deploy / activate middleware
7. Verify the access matrix
8. Activate Solved QP commerce **only** when the Founder launches the product

### 23d. Vercel preview verification — NOT PERFORMED

Preview verification could **not** be carried out in this session. The
environment has no Vercel CLI, no `.vercel` project link, no Vercel API token
and no Vercel connector, and the session is non-interactive so no login flow
could be completed. Nothing was changed in any Vercel environment, and
production was not touched — which is the correct outcome when Preview cannot
be cleanly isolated.

Still outstanding, to be run against a preview deployment once Vercel access
exists:

* unauthenticated `curl` of `/solvedQP/QP2607.html` and a paid `/meoclass1/`
  page must not return proprietary bytes;
* `miw_auth=1` alone must be denied;
* the two-session eviction matrix across separate cookie jars.

These are **deployment** proofs. The underlying **decision** logic is proven
offline: `authorizeRequest()` is the exact function the edge runs, and
`tools/security/sessions.test.mjs` drives the full matrix, including
fail-closed, forged-cookie and eviction cases.

### 23e. Launch posture

Solved QP is **not** live and no launch date is set. The product goes back to
content production first: complete 2025 → add available 2024 → multi-year
recurrence intelligence → derived Written study materials → Founder review →
Security V2 production activation → launch.
