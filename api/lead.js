/* Vercel serverless: receives a form submission and forwards it to a webhook.

   Requires (Vercel dashboard → Settings → Environment Variables):
     LEAD_WEBHOOK_URL   — where submissions are POSTed as JSON. Power Automate,
                          Zapier, Make and HubSpot all hand you such a URL.
   Optional:
     LEAD_WEBHOOK_TOKEN — sent as Authorization: Bearer <token> if your
                          endpoint expects one.

   Unset LEAD_WEBHOOK_URL returns 503 and the form shows the admissions email,
   so a visitor is never told "sent" when nothing was.  See FORMS.md.          */

const FORMS = {
  // form id           required fields
  "contact":      ["name", "email"],
  "team-pilot":   ["email"],
  "newsletter":   ["email"]
};
const MAX_FIELD = 2000;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const url = process.env.LEAD_WEBHOOK_URL;
  if (!url)
    return res.status(503).json({ error: "not_configured" });

  const body = req.body || {};

  // Honeypot: a real person leaves this empty. Accept silently so bots
  // cannot tell they were caught.
  if (body.company_website) return res.status(200).json({ ok: true });

  const form = String(body.form || "");
  if (!FORMS[form]) return res.status(400).json({ error: "Unknown form." });

  const fields = {};
  for (const [k, v] of Object.entries(body)) {
    if (k === "company_website" || k === "form" || k === "page") continue;
    if (typeof v !== "string") continue;
    const val = v.trim().slice(0, MAX_FIELD);
    if (val) fields[k] = val;
  }

  for (const req_ of FORMS[form])
    if (!fields[req_]) return res.status(400).json({ error: `Missing ${req_}.` });
  if (fields.email && !EMAIL_RE.test(fields.email))
    return res.status(400).json({ error: "That email address does not look right." });

  const headers = { "Content-Type": "application/json" };
  if (process.env.LEAD_WEBHOOK_TOKEN)
    headers.Authorization = `Bearer ${process.env.LEAD_WEBHOOK_TOKEN}`;

  try {
    const r = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify({
        form,
        fields,
        submitted_at: new Date().toISOString(),
        page: String(body.page || "").slice(0, 300)
      })
    });
    if (!r.ok) {
      console.error("lead webhook failed", r.status, await r.text().catch(() => ""));
      return res.status(502).json({ error: "delivery_failed" });
    }
  } catch (e) {
    console.error("lead webhook error", e && e.message);
    return res.status(502).json({ error: "delivery_failed" });
  }
  return res.status(200).json({ ok: true });
};
