/* Vercel serverless: Razorpay webhook receiver.
   Set in Razorpay dashboard → Webhooks → URL: https://<your-domain>/api/razorpay-webhook
   Env vars required:
     RAZORPAY_WEBHOOK_SECRET — the secret you type when creating the webhook
   Optional:
     FORWARD_WEBHOOK — a Make.com/Zapier URL to forward verified payment
                       events to (cohort assignment, receipt email, CRM). */
const crypto = require("crypto");

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).end();

  const secret = process.env.RAZORPAY_WEBHOOK_SECRET;
  if (!secret) return res.status(503).json({ error: "RAZORPAY_WEBHOOK_SECRET not set" });

  const body = JSON.stringify(req.body);
  const expected = crypto.createHmac("sha256", secret).update(body).digest("hex");
  const got = req.headers["x-razorpay-signature"];
  if (!got || !crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(String(got))))
    return res.status(400).json({ error: "Bad signature" });

  const event = req.body && req.body.event;
  if (event === "payment.captured" || event === "order.paid") {
    const fwd = process.env.FORWARD_WEBHOOK;
    if (fwd) {
      try {
        await fetch(fwd, { method: "POST", headers: { "Content-Type": "application/json" }, body });
      } catch (e) { /* forwarding is best-effort; Razorpay retries on non-200 only */ }
    }
  }
  return res.status(200).json({ ok: true });
};
