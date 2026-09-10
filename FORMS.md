# Forms

Every form on the site posts to `/api/lead`, which forwards the submission to a
webhook you choose. Nothing is stored on the site.

## Turn it on (about five minutes)

1. **Get a webhook URL.** Any of these gives you one:
   - **Power Automate** — "When an HTTP request is received" trigger
   - **Zapier** — "Webhooks by Zapier" → Catch Hook
   - **Make** — "Custom webhook"
   - **HubSpot** — a workflow with a webhook trigger
2. **Set it in Vercel** → Project → Settings → Environment Variables:
   - `LEAD_WEBHOOK_URL` = the URL from step 1
   - `LEAD_WEBHOOK_TOKEN` = optional; sent as `Authorization: Bearer <token>`
3. **Redeploy** (env var changes need one).
4. **Test** — submit the contact form and confirm the row arrives.

Until `LEAD_WEBHOOK_URL` is set, the endpoint returns 503 and every form tells
the visitor to email `info@tayanaacademy.com` instead. **This is deliberate**:
the visitor is never shown a success message when nothing was sent.

## What arrives

```json
{
  "form": "contact",
  "fields": { "name": "...", "email": "...", "interest": "...", "message": "..." },
  "submitted_at": "2026-09-10T02:44:37.958Z",
  "page": "/contact.html"
}
```

`form` is one of `contact`, `team-pilot`, `newsletter`. `fields` carries only
the non-empty fields, so map on key rather than position.

| Form | Where | Required |
|---|---|---|
| `contact` | contact.html | name, email |
| `team-pilot` | for-teams.html | email |
| `newsletter` | 7 pages | email |

## Editing a form

Fields are wired by `scripts/wire-forms.py`, which matches each control by its
`<label>` text and gives it a `name`. **If you rename a label, update the
mapping in that script and re-run it** — it is idempotent, so running it twice
is safe. Do not hand-add `name` attributes; the script is the source of truth.

```bash
python3 scripts/wire-forms.py     # after editing any form
node scripts/test-lead.js         # checks validation, honeypot, failure paths
```

## Spam

Each form carries an off-screen `company_website` honeypot. A filled honeypot
gets a normal `200` and is silently dropped, so bots cannot detect the trap.
There is no CAPTCHA; add one if volume becomes a problem.

## Notes

- Field values are capped at 2000 characters.
- A failed webhook returns 502 and the visitor is shown the email fallback, so a
  broken integration degrades to something usable rather than losing the lead
  silently. Failures are logged in the Vercel function logs.
- No submission is retried. If the webhook is down, the lead is not queued —
  the visitor is asked to email instead.
