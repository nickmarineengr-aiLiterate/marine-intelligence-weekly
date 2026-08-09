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

const credentialsBlock = (email, password) => password ? `
  <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1.25rem;margin:1.5rem 0">
    <p style="font-size:12px;color:#64748b;margin:0 0 12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em">Your Login Credentials</p>
    <table style="width:100%;font-size:14px;border-collapse:collapse">
      <tr><td style="color:#64748b;padding:5px 0;width:90px;vertical-align:top">Login page</td>
          <td><a href="${LOGIN_URL}" style="color:#0d9488">${LOGIN_URL}</a></td></tr>
      <tr><td style="color:#64748b;padding:5px 0">Email</td>
          <td style="color:#0f172a;font-weight:500">${email}</td></tr>
      <tr><td style="color:#64748b;padding:5px 0">Password</td>
          <td style="color:#0f172a;font-weight:700;font-family:monospace;font-size:16px;letter-spacing:1px">${password}</td></tr>
    </table>
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
      ${credentialsBlock(o.buyerEmail, o.password)}
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
    ${credentialsBlock(o.buyerEmail, o.password)}
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
