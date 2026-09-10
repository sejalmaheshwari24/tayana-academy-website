# Payments — plug-and-play runbook (Razorpay · UPI-first)

Everything is wired. Three steps make it live. Nothing else to build.

## 1. Keys (5 min)
- Razorpay dashboard → Settings → API Keys → generate.
- **Key ID** (`rzp_live_…` / `rzp_test_…`) → paste into `payments-config.js` → `RAZORPAY_KEY_ID`.
- **Key Secret** → Vercel dashboard → project → Settings → Environment Variables:
  - `RAZORPAY_KEY_ID` = same key id
  - `RAZORPAY_KEY_SECRET` = the secret  ← never goes in any site file
- Redeploy (push to main, or `vercel --prod`).

## 2. Prices (2 min)
`payments-config.js` → set `price` per track in ₹ (e.g. `price: 49999`).
- `null` keeps that track's button as "Pricing at the masterclass".
- Optional `DEPOSIT` for a seat-reservation amount (not wired to UI yet — ask if needed).

## 3. Webhook (5 min, recommended)
- Razorpay dashboard → Webhooks → Add:
  - URL: `https://<your-domain>/api/razorpay-webhook`
  - Events: `payment.captured`, `order.paid`
  - Secret: anything strong → also add to Vercel env as `RAZORPAY_WEBHOOK_SECRET`.
- Optional: `FORWARD_WEBHOOK` env var = a Make.com/Zapier URL → verified payments
  are forwarded there for cohort assignment / receipt / CRM.
- `SUCCESS_WEBHOOK` in `payments-config.js` = optional client-side ping on success
  (webhook above is the authoritative one; this is for instant UX automations).

## Test before going live
Use `rzp_test_` keys first. Test UPI: any VPA like `success@razorpay`;
test card: 4111 1111 1111 1111, any future expiry, any CVV.
Flow: /enroll.html → pick track → pay → Razorpay modal (UPI/GPay/PhonePe/cards/
netbanking all appear automatically for INR).

## What's where
| File | Role |
|---|---|
| `payments-config.js` | THE config: key id, prices, names — team edits only this |
| `enroll.html` | Checkout page (track selector → Razorpay modal). Deep-linkable: `/enroll.html?track=ai-engineer` |
| `api/create-order.js` | Serverless: creates the Razorpay order (uses env secret) |
| `api/razorpay-webhook.js` | Serverless: signature-verified payment events → optional forward |

## Go-live checklist
- [ ] KYC approved on Razorpay account
- [ ] Live keys in config + Vercel env
- [ ] Prices set
- [ ] Webhook added + secret in env
- [ ] One real ₹1 test payment end-to-end, then refund it from the dashboard
