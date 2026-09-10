/* Vercel serverless: creates a Razorpay order.
   Requires env vars (Vercel dashboard → Settings → Environment Variables):
     RAZORPAY_KEY_ID      — same key id as payments-config.js
     RAZORPAY_KEY_SECRET  — the secret (NEVER put this in client files)   */
module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const key_id = process.env.RAZORPAY_KEY_ID;
  const key_secret = process.env.RAZORPAY_KEY_SECRET;
  if (!key_id || !key_secret)
    return res.status(503).json({ error: "Payments not configured — set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in Vercel env vars (see PAYMENTS.md)." });

  const { amount, track, email, name, phone } = req.body || {};
  const amt = Math.round(Number(amount));
  if (!amt || amt < 100 || amt > 50000000)
    return res.status(400).json({ error: "Invalid amount (paise)." });

  const auth = Buffer.from(`${key_id}:${key_secret}`).toString("base64");
  const r = await fetch("https://api.razorpay.com/v1/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Basic ${auth}` },
    body: JSON.stringify({
      amount: amt,
      currency: "INR",
      receipt: `tayana_${(track || "track").slice(0, 24)}_${Date.now()}`,
      notes: { track: track || "", email: email || "", name: name || "", phone: phone || "" }
    })
  });
  const data = await r.json();
  if (!r.ok) return res.status(502).json({ error: data.error && data.error.description || "Razorpay order failed" });
  return res.status(200).json({ order_id: data.id, amount: data.amount, key_id });
};
