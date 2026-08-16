# SOLVED QP — COMMERCIAL, ACCESS AND DELIVERY ARCHITECTURE

**Review session, 2026-08-09.** Branch `pastpapers/2026-v1-product-review`.
Traced from the actual files in this repository, not inferred. Every claim below names the file and
line that supports it.

> **NOTHING IN THIS DOCUMENT WAS DEPLOYED, AND NO EXISTING SQ OR API FILE WAS MODIFIED.**
> The two new artefacts are additive and `noindex`.

---

## 1. WHAT EXISTS TODAY — TRACED

> **Dated snapshot.** §1 records the tree **as audited before the Security V2 work**. It is
> kept verbatim as the "before" state the rest of this document argues against; do not read
> it as current. Since then, on `commerce/solvedqp-recovery` (2026-08-11):
> `api/check-db.js` and `api/migrate-users.js` are **deleted**; `vercel.json`,
> `middleware.js`, `api/session.js` and `api/_lib/*` **now exist**; and route authorization
> lives in `api/_lib/routes.js` with price in `api/_lib/products.js`. None of it is deployed.
> Current state is in `CURRENT_STATUS.md` §4 and §6.

### 1.1 Files

| Area | Files |
|---|---|
| Storefront | `SQ/index.html`, `SQ/pay.html`, `SQ/examiner-index.html`, `SQ/QB1_A.html`, `SQ/simon-notes-p1.html`, `SQ/simon-notes-p2.html`, `SQ/miw-notes-mgmt-p1.html` |
| Backend | `api/create-order.js`, `api/verify-payment.js`, `api/check-password.js`, `api/razorpay-webhook.js`, `api/check-db.js`, `api/migrate-users.js` |
| Config | `package.json` only. **There is no `vercel.json` and no `middleware.js` anywhere in the repository.** |
| Store | Upstash Redis via `KV_REST_API_URL` / `KV_REST_API_TOKEN` |
| Email | Brevo SMTP relay (`smtp-relay.brevo.com:587`) through `nodemailer` |
| Payments | Razorpay, server-side HMAC-SHA256 signature verification |

### 1.2 Current flow, exactly as implemented

```
  BROWSER  SQ/index.html
     |  user picks a tier (founders / standard) and enters name + email
     v
  POST /api/create-order          <-- { amount, tier, buyer_email }   *** amount comes from the CLIENT
     |  create-order.js:77-98  builds the Razorpay order with THAT amount
     v
  RAZORPAY CHECKOUT  (user pays)
     |
     v
  POST /api/verify-payment        <-- { order_id, payment_id, signature, buyer_email, tier }
     |  verify-payment.js:214-219  HMAC-SHA256(order_id|payment_id, KEY_SECRET) -- CORRECT
     |  verify-payment.js:228-233  atomic SET NX lock, shared with the webhook -- CORRECT
     |  verify-payment.js:70-103   assignPassword(): pops the next value from QB_PASSWORD_POOL
     |                             and stores it in Redis as PLAINTEXT
     |  verify-payment.js:238      Brevo sends the password to the buyer
     v
  REDIS   miw:user:<email>            = <plaintext password>
          miw:pwd:<password>          = <email>
          miw:password_counter        = integer
          miw:active_device:<email>   = <device_id>, 30-day TTL
          miw:send_lock:<payment_id>  = claim marker, 24h TTL
     |
     v
  BROWSER  SQ/pay.html   user types email + password
     |  POST /api/check-password  { email, password, device_id }
     |  check-password.js:76   storedPassword === password.trim()   (plaintext compare)
     |  check-password.js:82-92 single-active-device, "last login wins"
     |  check-password.js:95-97 Set-Cookie: miw_auth=1; Path=/; Max-Age=2592000; SameSite=Lax; Secure
     |  pay.html:138            localStorage.setItem('miw_auth', {email, pwd, expiry})
     v
  REDIRECT /meoclass1/
     |
     v
  PROTECTED CONTENT   meoclass1/QB1_A.html:165
          <script>if(!/miw_auth=1/.test(document.cookie)){ location.replace('/SQ/pay.html') }</script>
```

### 1.3 The trust boundary

**The trust boundary is the Razorpay signature check in `verify-payment.js`, and nothing else.**
Everything after it — entitlement, price, and access to the paid files — is enforced in the browser.

---

## 2. SECURITY FINDINGS

Ordered by exploitability. These describe the **existing Oral QB product**; they matter here because
the Founder asked whether Solved QP should reuse this architecture, and the answer depends on them.

### FINDING 1 — the paid content is not access-controlled at all. **CRITICAL**

`meoclass1/QB1_A.html:165` is the entire gate:

```js
if(!/miw_auth=1/.test(document.cookie)){ window.location.replace("/SQ/pay.html"); }
```

- The cookie value is the **constant string `1`**. It is not a token, not signed, not a session id.
- It is **not `HttpOnly`**, so page JavaScript can set it.
- There is **no `vercel.json` and no `middleware.js`**, so nothing checks it server-side.

Consequently `document.cookie = "miw_auth=1"` in DevTools grants full access, and
`curl https://marineintelligenceweekly.com/meoclass1/QB1_A.html` returns the complete paid file
without any credential, because the redirect is client-side JavaScript that curl never runs.

> **This answers the Founder's question 29 directly.** The `localStorage` object in `pay.html:138` is
> UI convenience — but the alternative is **not** a trusted server check. It is a *weaker* client
> check. Option **B** is the true state of affairs, and the honest framing is that the paid static
> files are **publicly readable today**.

### FINDING 2 — the client sets the price. **CRITICAL**

`api/create-order.js:77` reads `amount` from the request body and `:84-98` passes it straight to
Razorpay. The server never consults a price list.

```
POST /api/create-order  { "amount": 1, "tier": "founders", "buyer_email": "x@y.com" }
```

creates a genuine ₹1 order. The buyer pays ₹1, Razorpay returns a **valid** signature over that real
payment, `verify-payment.js` verifies it correctly — and **never checks the amount** — then issues a
password and emails full access. Signature verification is doing its job; it proves the payment is
real, not that it was for the right sum.

### FINDING 3 — passwords are stored and transmitted in plaintext. **HIGH**

- `verify-payment.js:99` — `redisSet('miw:user:'+email, password)`, unhashed.
- `check-password.js:76` — `storedPassword === password.trim()`, a direct string compare.
- `verify-payment.js:97` and `:240`, `check-password.js:94` — passwords are written to the **server
  logs**.
- `verify-payment.js:79` — the pool `QB_PASSWORD_POOL` is a fixed shared list, so passwords are
  drawn from a finite known set rather than generated per user.
- `verify-payment.js:100` — the reverse index `miw:pwd:<password>` makes the whole set enumerable
  from a Redis dump.

### FINDING 4 — there is no entitlement model. **HIGH, and it is the blocker for Solved QP**

Redis stores `miw:user:<email> = password`. There is **no record of what the user bought**. `tier`
travels through `create-order` and `verify-payment` and is used only to choose an email template
(`verify-payment.js:105-113`); it is never persisted.

> **Adding Solved QP on top of this would give every existing Oral QB customer the written papers
> for free, and vice versa**, because the only thing `miw_auth=1` can express is "someone, once,
> paid for something".

### FINDING 5 — no rate limiting on `check-password`. **MEDIUM**

`api/check-password.js` has no attempt counter and no lockout. With a finite shared password pool
(Finding 3) and known customer emails, that is brute-forceable.

### FINDING 6 — `SameSite=Lax` without `HttpOnly` on a cross-purpose cookie. **LOW in isolation**

`check-password.js:95-97` sets `Secure` and `SameSite=Lax` correctly, but omits `HttpOnly`. Given
Finding 1 the cookie carries no secret, so this is currently harmless — it becomes important the
moment the cookie starts carrying a real session.

---

## 3. TARGET SOLVED QP FLOW

```
  SQ/index.html
     |  user selects product: ORAL_QB_NOTES | SOLVED_QP | BUNDLE
     v
  POST /api/create-order   { product, tier, buyer_email }        <-- NO amount from the client
     |  server looks the price up in a SERVER-SIDE PRICE TABLE
     |  order.notes carries { product, tier, price_id }
     v
  RAZORPAY CHECKOUT
     |
     v
  POST /api/verify-payment { order_id, payment_id, signature, ... }
     |  1. verify HMAC signature                     (already correct today)
     |  2. RE-FETCH the order from Razorpay and CHECK amount + currency == the price table
     |  3. read product/tier from order.notes, NOT from the request body
     |  4. atomic SET NX claim                        (already correct today)
     |  5. GRANT ENTITLEMENT
     |         miw:ent:<email> = { "ORAL_QB_NOTES": {...}, "SOLVED_QP": {...} }
     |  6. create a credential (hashed) and a session
     |  7. send the product-specific email
     v
  LOGIN  ->  server-signed, HttpOnly session cookie carrying the ENTITLEMENT SET
     |
     v
  SERVER-SIDE GATE  (Vercel middleware or a serving function)
     |  /meoclass1/pastpapers/QP*.html  requires  SOLVED_QP
     |  /meoclass1/QB*.html             requires  ORAL_QB_NOTES
     v
  PROTECTED CONTENT
```

**The client is authoritative for nothing: not price, not product, not entitlement.**

---

## 4. RECOMMENDATIONS

### 4.1 Entitlements — extend, do not clone

```
ORAL_QB_NOTES     the existing Question Bank + Simon/MIW notes bundle
SOLVED_QP         MEO Class I solved written question papers
BUNDLE            grants both; stored as the two atoms, never as a third magic value
```

Stored per user, not per product endpoint:

```
miw:ent:<email> = {
  "ORAL_QB_NOTES": { "granted": "2026-08-09", "order": "order_xxx", "tier": "standard" },
  "SOLVED_QP":     { "granted": "2026-09-01", "order": "order_yyy", "tier": "standard" }
}
```

**Migration matters and is easy to get wrong.** Every existing customer must be back-filled with
`ORAL_QB_NOTES` **only**. A default of "has_access ⇒ everything" would hand the new product to the
entire existing customer base.

> **Superseded, 2026-08-11.** This paragraph named `api/migrate-users.js` as the natural home.
> That endpoint has been **deleted**: it was an unauthenticated handler performing a bulk user
> migration, reachable in production. Back-fill now runs offline through
> `tools/security/migrate_entitlements.mjs`, an operator tool with no HTTP surface. The
> requirement is unchanged — back-fill `ORAL_QB_NOTES` **only** — but it must never again be
> carried out by a public endpoint.

**RECOMMENDATION — extend the three existing endpoints with a `product` dimension. Do not create
`verify-qp-payment.js`, `check-qp-password.js` or `send-qp-email.js`.** Duplicating them would fork
the signature check, the atomic double-send lock and the device policy — three pieces of logic that
took real work to get right and that must not drift apart. The isolation argument does not apply
here, because the risky code is the part that would be duplicated.

### 4.2 Login UX — **OPTION A, a shared access page**

**Recommended: one login at `SQ/pay.html`, which after authentication shows the products the user
actually owns.**

- A Solved-QP-only buyer must never be walked through a page that behaves as though they bought the
  Oral QB. Option A solves that by rendering from the entitlement set.
- Option B (separate thin entry pages) doubles the login surface and the session bugs for no gain,
  and the two products already share one identity: the buyer's email.
- One page also makes the upsell natural: an Oral QB owner sees a locked Solved QP tile with a CTA.

### 4.3 Session and cookie

| Property | Target | Today |
|---|---|---|
| `HttpOnly` | yes | **no** |
| `Secure` | yes | yes |
| `SameSite` | `Lax` | `Lax` |
| Value | signed session id, server-side lookup | the literal `1` |
| Carries entitlement | yes, server-side | nothing |
| Expiry | 30 days, sliding | 30 days |

**Do not reuse the buyer's password as a Solved QP access token.** Keep the single-active-device
policy — it is a good, low-support design and it is the one part of the auth layer worth copying
forward as-is.

> **This is ACCESS CONTROL AND DETERRENCE, not DRM.** A paying customer can always copy what they
> can read. The goal is that an *unauthenticated stranger* cannot, which is not true today.

### 4.4 Email — extend Brevo, add nothing

Brevo SMTP through `nodemailer` works and is already wired. Add a product-specific template
alongside the existing one:

```
Subject:  MIW Solved Question Papers — your access details
Body:     purchase confirmed (product, tier, order id)
          login link -> /SQ/pay.html
          credential + how the single-device rule works
          what is included: the solved papers currently in the library, derived not hard-coded
          support + recovery -> contactus@marineintelligenceweekly.com
```

**Do not hard-code the paper list in the email.** Derive it the same way the sample page does
(`build_sample.newest_solved`), or the email will be wrong the first time a paper is added.

### 4.5 Static delivery — the honest V1 answer

Today `/meoclass1/**` is plain static hosting with a client-side redirect. **Any V1 that leaves the
solved papers as public static files under a guessable URL is not access control**, whatever the
page's JavaScript does.

Least-disruptive option that actually works, in preference order:

1. **Vercel middleware** (`middleware.js` at the repo root) matching `/meoclass1/pastpapers/QP*.html`,
   validating the session cookie and checking `SOLVED_QP`. **~40 lines, no framework, no rebuild of
   the site.** This is the recommendation.
2. A serving function that reads the generated HTML and returns it only on a valid entitlement.
   More control, more moving parts.
3. Signed time-limited URLs. Most work, and it breaks bookmarks — which this product's own design
   deliberately supports.

**Do not rebuild the site into a framework.** Option 1 is compatible with everything that exists.

---

## 5. SQ STOREFRONT INTEGRATION — DESIGNED, NOT APPLIED

### 5.1 Why `SQ/index.html` was not modified this session

1. **No price is approved.** The card would advertise something nobody can buy.
2. **No entitlement exists** (Finding 4), so a purchase could not be honoured distinctly.
3. `SQ/index.html` is a live production file. The brief forbids deploying unfinished product logic,
   and a storefront card is the single most deployable thing in this repository.

**Files proposed to change, when the Founder approves — and only then:**

| File | Change |
|---|---|
| `SQ/index.html` | add the free-sample card (§5.2) and the Solved QP product section (§5.3) |
| `SQ/pay.html` | after login, render owned products from the entitlement set (§4.2) |
| `api/create-order.js` | server-side price table; drop the client `amount` |
| `api/verify-payment.js` | re-fetch order, check amount, read product from `order.notes`, write entitlement |
| `api/check-password.js` | return the entitlement set; harden per §4.3 |
| ~~`api/migrate-users.js`~~ → `tools/security/migrate_entitlements.mjs` | back-fill every existing user with `ORAL_QB_NOTES` only. The endpoint was **deleted** 2026-08-11; back-fill is an offline operator tool with no HTTP surface |
| `middleware.js` | **new** — server-side gate for `/meoclass1/**` |

### 5.2 Free-sample card — ready to paste, uses existing SQ classes

```html
<!-- FREE SAMPLE — Solved Written Paper -->
<section class="sample-section">
  <div class="sample-card">
    <div class="sample-card-left">
      <div class="sample-q-count">9</div>
      <div class="sample-q-label">Questions</div>
    </div>
    <div class="sample-card-divider"></div>
    <div class="sample-card-body">
      <span class="sample-card-badge">FREE SAMPLE</span>
      <div class="sample-card-title">Solved Written Paper — January 2026</div>
      <p class="sample-card-desc">
        A complete MEO Class I Engineering Management sitting, exactly as printed.
        Two questions are worked in full with the MIW study method — Understand, Exam plan,
        Answer, Study guide, Recall. The remaining seven show how each answer is structured.
      </p>
      <div class="sample-tags">
        <span class="sample-tag">Model written answers</span>
        <span class="sample-tag">Exam plan</span>
        <span class="sample-tag">Knowledge map</span>
        <span class="sample-tag">Flashcards</span>
        <span class="sample-tag">Recurrence intelligence</span>
      </div>
      <a class="sample-card-btn" href="/SQ/solved-qp-sample-january-2026.html">
        Open the free written paper sample →
      </a>
    </div>
  </div>
</section>
```

The copy deliberately does **not** say "9 complete answers free". It says what is true, which is
also what converts: you get a whole sitting, two of them fully worked.

### 5.3 Product distinction — keep the two offers separate

The storefront must not blur them.

| | **Oral QB + Notes** | **Solved Written Question Papers** |
|---|---|---|
| Exam | Kochi MMD **oral** | The **written** examination |
| Content | 417+ real oral questions, Simon notes, MIW Engineering Management notes | Solved past written papers, month by month |
| Distinctive | organised **by examiner** — Nair, Simon, Rajappan, Srivastava, Senthil, Paul | model written answer · exam plan · knowledge map · study guide · recall · recurrence intelligence · yearly question sheet |
| Price | ₹1,499 for one year — **unchanged, do not touch** | ₹1,500 for one year |

> **There is no examiner-personality dimension in the written product and it must never be implied.**
> The written paper is nationally set; "know your examiner" is an oral-exam proposition. Borrowing it
> would be a false claim.

### 5.4 Pricing

**No price is invented anywhere.** The projection config carries `"price_display": "PRICE_TBD"`, and
`sample_check.py` **fails the build** if any rupee value renders while it is unset. Existing QB
prices are untouched.

---

## 6. JULY WITHOUT GIVING JULY AWAY

The Founder wants July as the conversion incentive. Three mechanisms, none of which exposes a July
answer:

1. **Derived, never hard-coded.** `build_sample.newest_solved()` computes the most recent *solved*
   sitting from the specs. The page renders **"newest solved paper: July 2026"** today and will say
   August the day an August spec lands, with no edit. A hand-written "latest" would become a lie on
   a schedule.
2. **Metadata only.** The offer block lists month names of solved papers. No July stem, no July
   answer, no July route. `sample_check.py` sweeps the shipped bytes for **every other paper's**
   answer prose and fails on a hit.
3. **The free year sheet does the rest.** `questions-2026.html` shows July's nine questions in full —
   questions, not answers — so a candidate can see exactly what July asks and that MIW has solved it.
   Wanting the answer is the conversion.

> **A commercial constraint that only became visible through the recurrence model:** the January
> sample's two full demos had to be **family singletons**. Six of January's nine questions are the
> first occurrence of a family that returns later in 2026, so publishing one in full also publishes
> its paid twin — and **January Q3's family reaches QP2607-Q5, the July paper itself**. `build_sample.py`
> enforces this and refuses to build if a configured demo has relatives.

---

## 7. WHERE THE PRODUCT SHOULD LIVE — **DO NOT MOVE**

**Recommendation: OPTION A. Canonical content stays at `meoclass1/pastpapers/`.**

| Layer | Location |
|---|---|
| Canonical source of truth | `meoclass1/pastpapers/specs/*.json` — **unchanged** |
| Generated solved papers | `meoclass1/pastpapers/QP*.html` — **unchanged**, to be gated by middleware |
| Free questions-only year sheet | `meoclass1/pastpapers/questions-<year>.html` — public |
| Free conversion sample | `SQ/solved-qp-sample-january-2026.html` — public, in the storefront |
| Storefront and checkout | `SQ/index.html`, `SQ/pay.html` |
| Projection config | `meoclass1/pastpapers/sample/*.sample.json` |

Why not Option B (physically move the product):

- **Every relative URL breaks at once** — cross-links between papers, the manifest, the topic pages,
  the `meoclass1/index.html` nav entry, and the `QB9_E` cross-links into the Question Bank.
- **The toolchain hard-codes `meoclass1/pastpapers`** in eight tools; a move is a rewrite of all of
  them plus their tests, with no product benefit.
- **Git history for six verified papers becomes harder to follow** at exactly the moment the
  verification records matter most.
- **Bookmarks and saved study state** are keyed to those URLs; `localStorage` progress survives, but
  a candidate's browser bookmarks do not.
- **It buys nothing.** Commercial separation is achieved by the *gate* and the *entitlement*, not by
  the directory name.

Why not Option C (emit a separate protected build): it creates a second copy of the answers, which
is precisely the "no answer text exists twice" rule the architecture is built on.

> **Commercial independence does not require duplicate canonical truth.** One canonical store, one
> generator, several delivery surfaces with different access rules.

---

## 8. QUESTIONS-ONLY YEAR SHEET — FREE, RECOMMENDED

**RECOMMENDATION: publish `questions-<year>.html` free and indexable, once the Founder approves.**

For:

- It is the natural discovery surface and the strongest SEO asset the product has — a candidate
  searching "MEO Class 1 Engineering Management January 2026 questions" lands on it.
- It is genuinely useful on its own, which builds the trust the storefront needs.
- The conversion path is built in: every question carries "Open the solved answer →".
- It gives away nothing that is sold. `questions_year_check.py` proves that against shipped bytes.

Against, and it needs a Founder answer before publication:

- **Provenance.** The questions are transcribed from third-party-hosted scans and
  `official_source_verified` is `false` on all six papers. The page must keep saying so.
- **No host branding, ever** — already enforced by `validate_spec.py` and trap 14.
- **No host recurrence annotation** — the new page uses MIW's own model and emits none (§2.4 of the
  intelligence review).

---

## 9. PUBLICATION STATE

| | |
|---|---|
| `questions-2026.html` | **NOINDEX**, Founder review copy |
| `SQ/solved-qp-sample-january-2026.html` | **NOINDEX**, Founder review copy |
| Six solved paper pages | unchanged, `noindex`, ungated |
| `SQ/index.html`, `SQ/pay.html`, `api/**` | **untouched** |
| Razorpay pricing | **untouched**. No test orders were issued. |

Both new pages carry `robots: noindex, nofollow, noarchive, nosnippet` and a visible review banner.
`--publish` flips them, and that switch is a Founder decision, not a session decision.
