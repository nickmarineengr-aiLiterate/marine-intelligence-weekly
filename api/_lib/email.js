// =============================================================
// Marine Intelligence Weekly — Access emails
// File: api/_lib/email.js
//
// verify-payment.js and razorpay-webhook.js previously each carried
// their own copy of the email builder with a "keep these in sync"
// comment. They are now one function, so a Written-product email can
// never exist in one path and not the other.
//
// Three shapes:
//   new ORAL buyer      — credentials + Oral orientation
//   new SOLVED_QP buyer — credentials + Written orientation
//   existing account    — "added to your existing access", no new
//                         password, because the account already has one
// =============================================================

export const LOGIN_URL = "https://marineintelligenceweekly.com/SQ/pay.html";

// nodemailer is imported lazily, inside makeTransport(), rather than at
// module load. buildAccessEmail() is a pure string builder and the
// security tests exercise it (and everything that imports this file)
// with no node_modules present and no SMTP anywhere near them.
export async function makeTransport() {
  const { default: nodemailer } = await import("nodemailer");
  return nodemailer.createTransport({
    host: "smtp-relay.brevo.com",
    port: 587,
    secure: false,
    auth: {
      user: process.env.BREVO_SMTP_LOGIN,
      pass: process.env.BREVO_SMTP_KEY,
    },
  });
}

const FROM = `"Marine Intelligence Weekly" <contactus@marineintelligenceweekly.com>`;

const shell = (bodyHtml, headline) => `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',system-ui,sans-serif">
<div style="max-width:560px;margin:2rem auto;background:#fff;border-radius:8px;border:1px solid #e2e8f0;overflow:hidden">
  <div style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:1.5rem">
    <p style="color:#0d9488;font-weight:700;font-size:1.1rem;margin:0">Marine Intelligence Weekly</p>
    <p style="color:#94a3b8;font-size:13px;margin:4px 0 0">${headline}</p>
  </div>
  <div style="padding:2rem">${bodyHtml}</div>
  <div style="background:#f1f5f9;padding:1rem;text-align:center;border-top:1px solid #e2e8f0">
    <p style="font-size:11px;color:#94a3b8;margin:0">© 2026 Marine Intelligence Weekly &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/terms.html" style="color:#64748b;text-decoration:none">Terms</a> &nbsp;|&nbsp;
      <a href="https://marineintelligenceweekly.com/privacy.html" style="color:#64748b;text-decoration:none">Privacy</a>
    </p>
  </div>
</div></body></html>`;

/**
 * When this credential was issued, in IST.
 *
 * WHY IT IS ON THE EMAIL AT ALL
 * -----------------------------
 * A password can be replaced several times in a day — a purchase, an
 * incident rotation, a self-service reset — and each replacement kills
 * the one before it. Two of those paths share a subject line, so a
 * recipient holding three emails had no way to tell which credential is
 * live except by inferring it from message order, which mail clients
 * reorder, thread and collapse. The Founder hit exactly this after four
 * emails in one night.
 *
 * The stamp makes the newest credential identifiable from the CONTENT
 * rather than from its position in an inbox.
 *
 * IST because that is where the readers are. `date` is injectable so the
 * tests are not time-dependent — a formatter that reads the clock is
 * untestable, and an untested formatter is how a mail goes out saying
 * "Invalid Date".
 */
export function issuedStamp(date = new Date()) {
  return new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Kolkata",
    day: "numeric", month: "short", year: "numeric",
    hour: "2-digit", minute: "2-digit", hour12: false,
  }).format(date).replace(",", "") + " IST";
}

const credentialsBlock = (email, password, issuedAt = new Date()) => password ? `
  <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
    <p style="font-size:12px;color:#64748b;margin:0 0 12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em">Your Login Credentials</p>
    <table style="width:100%;font-size:14px;border-collapse:collapse">
      <tr><td style="color:#64748b;padding:5px 0;width:90px;vertical-align:top">Login page</td>
          <td><a href="${LOGIN_URL}" style="color:#0d9488">${LOGIN_URL}</a></td></tr>
      <tr><td style="color:#64748b;padding:5px 0">Email</td>
          <td style="color:#0f172a;font-weight:500">${email}</td></tr>
      <tr><td style="color:#64748b;padding:5px 0">Password</td>
          <td style="color:#0f172a;font-weight:700;font-family:monospace;font-size:16px;letter-spacing:1px">${password}</td></tr>
      <tr><td style="color:#64748b;padding:5px 0;vertical-align:top">Issued</td>
          <td style="color:#0f172a;font-weight:500">${issuedStamp(issuedAt)}</td></tr>
    </table>
    <p style="font-size:12px;color:#64748b;margin:12px 0 0;line-height:1.5">
      If you have more than one email from us, <strong>use the one with the latest
      &ldquo;Issued&rdquo; time</strong> — earlier passwords stop working.
    </p>
  </div>` : `
  <div style="background:#f0fdfa;border-left:3px solid #0d9488;padding:12px 16px;margin:1.5rem 0">
    <p style="margin:0;font-size:14px;color:#134e4a">
      <strong>Use your existing MIW login.</strong> Sign in at
      <a href="${LOGIN_URL}" style="color:#0d9488">${LOGIN_URL}</a> with
      <strong>${email}</strong> and the password you already have — your new
      purchase has been added to that same account. No new password is issued.
    </p>
  </div>`;

const cta = (label) => `
  <div style="text-align:center;margin:1.5rem 0">
    <a href="${LOGIN_URL}" style="background:#0d9488;color:#fff;text-decoration:none;padding:13px 32px;border-radius:8px;font-weight:600;font-size:15px;display:inline-block">${label} →</a>
  </div>`;

const support = `
  <div style="border-top:1px solid #e2e8f0;padding-top:1rem;margin-top:1.5rem">
    <ul style="font-size:13px;color:#334155;padding-left:18px;margin:0;line-height:1.9">
      <li>Save this email — it contains your login details</li>
      <li>Access is personal — please do not share your password</li>
      <li>Help: <a href="mailto:contactus@marineintelligenceweekly.com" style="color:#0d9488">contactus@marineintelligenceweekly.com</a></li>
    </ul>
  </div>
  <p style="font-size:14px;color:#0f172a;font-weight:600;margin:1.5rem 0 0">Nixon Antony</p>
  <p style="font-size:12px;color:#64748b;margin:2px 0 0">Second Engineer, Maersk A/S | Marine Intelligence Weekly</p>`;

/**
 * @param {object} o
 * @param {string} o.productId     ORAL_QB_NOTES | SOLVED_QP
 * @param {string} o.buyerEmail
 * @param {string} o.buyerName
 * @param {string|null} o.password null => existing account, no new credential
 * @param {string} o.priceDisplay  e.g. "₹1,500"
 * @param {boolean} o.isUpgrade    true when added to an existing account
 */
export function buildAccessEmail(o) {
  const name = o.buyerName || "there";

  if (o.productId === "SOLVED_QP") {
    const body = `
      <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${name},</p>
      <p style="color:#334155;line-height:1.6;margin:0 0 16px">
        ${o.isUpgrade
          ? `Thank you — <strong>Solved Question Papers</strong> (${o.priceDisplay}) has been added to your existing MIW access. ⚓`
          : `Thank you for your purchase — <strong>MIW Solved Question Papers</strong> (${o.priceDisplay}). Your Written access is ready. ⚓`}
      </p>
      ${credentialsBlock(o.buyerEmail, o.password, o.issuedAt)}
      ${cta("Open Solved Question Papers")}
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
        <p style="font-size:14px;font-weight:600;color:#0f172a;margin:0 0 10px">📘 What's inside</p>
        <p style="font-size:13px;color:#334155;line-height:1.7;margin:0 0 10px">
          Complete solved MEO Class I <strong>Engineering Management</strong> Written papers, each
          question worked through five study modes: <strong>Understand → Exam Plan → Answer →
          Study Guide → Recall</strong>.
        </p>
        <p style="font-size:13px;color:#334155;line-height:1.7;margin:0">
          Start at <a href="https://marineintelligenceweekly.com/solvedQP/" style="color:#0d9488">the Solved QP home</a>
          — every sitting, searchable, with recurrence across papers marked.
        </p>
      </div>
      ${support}`;
    return {
      from: FROM,
      to: o.buyerEmail,
      subject: `MIW Solved Question Papers — Access Details`,
      html: shell(body, "Solved Question Papers — Written"),
    };
  }

  // ORAL_QB_NOTES
  const body = `
    <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${name},</p>
    <p style="color:#334155;line-height:1.6;margin:0 0 16px">
      ${o.isUpgrade
        ? `Thank you — <strong>Oral QB + Notes</strong> (${o.priceDisplay}) has been added to your existing MIW access. ⚓`
        : `Thank you for your purchase (${o.priceDisplay}). Your QB access is ready. ⚓`}
    </p>
    ${credentialsBlock(o.buyerEmail, o.password, o.issuedAt)}
    ${cta("Access Question Bank")}
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
      <p style="font-size:14px;font-weight:600;color:#0f172a;margin:0 0 10px">🧭 How to find anything fast</p>
      <table style="width:100%;font-size:13px;border-collapse:collapse">
        <tr><td style="padding:4px 0;color:#64748b;width:130px;vertical-align:top">By examiner</td>
            <td><a href="https://marineintelligenceweekly.com/meoclass1/examiner-index.html" style="color:#0d9488">Examiner Index</a></td></tr>
        <tr><td style="padding:4px 0;color:#64748b;vertical-align:top">By topic keyword</td>
            <td><a href="https://marineintelligenceweekly.com/meoclass1/oralnotes/notes-master-index.html" style="color:#0d9488">Notes Master Index</a></td></tr>
        <tr><td style="padding:4px 0;color:#64748b;vertical-align:top">Everything at once</td>
            <td><a href="https://marineintelligenceweekly.com/meoclass1/oralnotes/" style="color:#0d9488">Notes Home</a></td></tr>
      </table>
    </div>
    ${support}`;

  return {
    from: FROM,
    to: o.buyerEmail,
    subject: `🚢 Your MEO Class 1 QB Access`,
    html: shell(body, "MEO Class 1 Question Bank"),
  };
}

// -------------------------------------------------------------
// Security notification — credential rotation.
//
// This is an ACCESS notice, not marketing and not an apology letter.
// It answers the only three questions the customer actually has:
// what stopped working, what to use instead, and did I lose what I
// paid for. It says nothing about repositories, commits or internal
// architecture — that detail helps no customer and tells anyone who
// forwards the mail exactly where to go looking.
//
// The password is interpolated here and nowhere else. Delivery is the
// ONLY channel permitted to carry it; see api/_lib/rotation.js.
// -------------------------------------------------------------
/**
 * Self-service reset. Distinct from buildRotationEmail because the
 * customer ASKED for this one — it should read as a reply to their
 * request, not as an alarm. It also has to state plainly that the old
 * password is gone, since the natural expectation of "forgot password"
 * is that the original will be sent back, and it cannot be.
 */
export function buildResetEmail(email, password, { name = "", issuedAt = new Date() } = {}) {
  const greeting = name.trim() || "there";
  const body = `
    <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${greeting},</p>
    <p style="color:#334155;line-height:1.6;margin:0 0 16px">
      You asked to reset your Marine Intelligence Weekly password. Here is a
      new one. Your previous password no longer works.
    </p>
    <div style="background:#f0fdfa;border-left:3px solid #0d9488;padding:12px 16px;margin:0 0 8px">
      <p style="margin:0;font-size:14px;color:#134e4a">
        <strong>Everything you have purchased is still on your account.</strong>
        Only the password has changed.
      </p>
    </div>
    ${credentialsBlock(email, password, issuedAt)}
    ${cta("Sign in with your new password")}
    <p style="color:#334155;line-height:1.6;font-size:14px;margin:0 0 8px">
      You have been signed out on all devices, so you will need to sign in
      again on each one.
    </p>
    <p style="color:#64748b;line-height:1.6;font-size:13px;margin:0">
      If you did not request this, someone entered your address on the reset
      form. Your account is safe — simply use the new password above, or
      contact us and we will help.
    </p>
    ${support}`;

  return {
    from: FROM,
    to: email,
    subject: "Your new MIW password",
    html: shell(body, "Password reset"),
  };
}

export function buildRotationEmail(email, password, { name = "", issuedAt = new Date() } = {}) {
  const greeting = name.trim() || "there";
  const body = `
    <p style="font-size:16px;color:#0f172a;margin:0 0 12px">Hi ${greeting},</p>
    <p style="color:#334155;line-height:1.6;margin:0 0 16px">
      As a precaution, we have issued you a <strong>new password</strong> for your
      Marine Intelligence Weekly account. Your previous password has been
      retired and will no longer work.
    </p>
    <div style="background:#fffbeb;border-left:3px solid #f59e0b;padding:12px 16px;margin:0 0 8px">
      <p style="margin:0;font-size:14px;color:#78350f">
        <strong>Your access is unchanged.</strong> Everything you have purchased is
        still on your account exactly as before. Only the password has changed.
      </p>
    </div>
    ${credentialsBlock(email, password, issuedAt)}
    ${cta("Sign in with your new password")}
    <p style="color:#334155;line-height:1.6;font-size:14px;margin:0 0 8px">
      You will need to sign in again on each of your devices. If you were signed
      in on your phone and your laptop, both will ask for the new password once.
    </p>
    ${support}`;

  return {
    from: FROM,
    to: email,
    subject: "Your MIW password has been reset — action needed",
    html: shell(body, "Account security — new password issued"),
  };
}
