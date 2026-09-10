/* ============================================================
   TAYANA PAYMENTS — the ONE file the team edits to go live.
   1) Paste your Razorpay Key ID below (rzp_test_… or rzp_live_…).
      The key SECRET never goes here — it goes in Vercel env vars
      (see PAYMENTS.md).
   2) Set a price (in ₹) per track to enable its Pay button.
      null = "pricing announced at masterclass" (button disabled).
   ============================================================ */
window.TAYANA_PAY = {
  RAZORPAY_KEY_ID: "",          // e.g. "rzp_test_AbCdEf123456"
  CURRENCY: "INR",
  BUSINESS_NAME: "Tayana Academy",
  THEME_COLOR: "#4A38E8",

  TRACKS: {
    "no-code-agent":  { name: "No-Code Agent Engineers", weeks: 4, seats: 24, price: null },
    "pro-code-agent": { name: "Pro-Code Agent Engineers", weeks: 6, seats: 24, price: null },
    "ai-engineer":    { name: "AI Engineer",             weeks: 6, seats: 24, price: null },
    "ml-engineer":    { name: "Machine Learning Engineers", weeks: 6, seats: 24, price: null },
    "consumers":      { name: "Consumers — AI for your role", weeks: 4, seats: 20, price: null,
                       length: "30 days", pillar: "consumers" }
  },

  /* Optional: seat-reservation deposit (₹). null = full payment only. */
  DEPOSIT: null,

  /* After successful payment, POST the receipt to this webhook
     (e.g. your Make.com scenario) for cohort assignment + email.
     Leave empty to skip. */
  SUCCESS_WEBHOOK: ""
};
