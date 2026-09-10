# Tayana Academy — Website Build Brief

This is the persistent brief for building/maintaining the **Tayana Academy** marketing site. Read it before editing. It is the single source of truth for direction, brand, content model, and structure.

## What this is
A static, multi-page marketing website — **plain HTML + CSS + JS in one folder, no framework, no build pipeline.** Every page is directly editable HTML. This is intentional; keep it that way. Do not introduce React/Vue/bundlers/site-builders.

## The one direction (do not reopen)
- **Vibrant Magician · light mode.** This is locked and approved.
- The old **Magician × Sage** direction (coral/sage, `v4-site.*`) is **retired** and lives in `archive/`. Never pull from it.
- Tokens live in `ds-tokens.css` (titled "VIBRANT MAGICIAN"). Variable names are legacy on purpose:
  - `--copper` = **Indigo `#4A38E8`** (PRIMARY · Builders accent)
  - `--brass` = **Spring `#368634`** (SUPPORTING · Consumers accent)
  - `--iron` = ink / text / dark anchor
  - `--sun` = attention · cohort badges (never body text)
- Style against `var(--*)` and the existing classes — never hardcode new hex values.

## The company (context)
Tayana Academy — a two-pillar AI academy, founded 2023, Atlanta (AFC Towers, 3343 Peachtree Road, STE# 180-1142, Atlanta GA 30326). Domain `tayanaacademy.com`.
- **Builders** (Indigo) — people *entering* AI careers. Outcome: a shipped portfolio project + placement pathway. 4–6 week cohorts, 24 seats.
- **Consumers** (Spring) — professionals *applying* AI to the role they already have. Outcome: a workflow shipped to production. 30-day cohorts + optional 2-hr pilot, 20 seats.
- The **masterclass** is the door: Builders → *Register for the masterclass*; Consumers → *Book a scoping call*.
- Cohorts are small, themed "AI for [Topic] · [Season Year]", run 1st & 15th monthly, taught on **Orion** (the in-house LMS).

## ⭐ Orion course model (the content spine — keep every surface consistent with this)
Everyone follows one pathway on Orion:
1. **Join Orion** → 2. **AI Foundation 1 & 2** → 3. **Career Assessment** → 4. **Technical Screening**.
Screening routes to one of two paths:
- **Python path** (Python required) → *Pro-Code Agent Engineers* & *Machine Learning Engineers*. Fail → **Python Foundation** → re-assess.
- **Full-Stack path** (full-stack required) → *AI Engineer*. Fail → **Full-Stack Foundation** (frontend, backend, DBs & APIs) → re-assess.
- No background? Start with a Foundation course, then re-assess anytime.

**The 4 AI Career Tracks (Builders products):**
1. **No-Code Agent Engineers** · *no coding required* · visual builders, templates, automated workflows.
2. **Pro-Code Agent Engineers** · *Python required* · LangChain, CrewAI, LangGraph, MCP, multi-agent systems.
3. **AI Engineer** · *full-stack required* · LLM apps/products, RAG, vector DBs, deployed to production.
4. **Machine Learning Engineers** · *Python required* · model training/eval, end-to-end ML systems, MLOps.

**Entry per track** (shown as a badge on every track surface):
No-Code → *AI Foundation + Career Assessment* · Pro-Code and ML → *Python Assessment / Python Foundation* ·
AI Engineer → *Full Stack Assessment / Full Stack Foundation*.

**Role model (Sep 2026 — from the four course infographics).** Every track page carries, in order:
positioning triad → entry badge → role description → core capabilities → technologies & tools (real
logos) → enterprise solutions delivered → *Why hire X?* → sample professional profile. The content is
held in `scripts/build-role-sections.py` (TRACKS dict) and injected between `<!-- ROLE:… -->` fences —
**edit the script and re-run it, never hand-edit those blocks.**

Consumers cohorts are themed by function: *AI for Financial Operations · Marketing · People & L&D · IT & Operations*.

Canonical implementation of the pathway: `catalog.html` (the strip) and `builders.html` (first-class pathway section + screening paths). Reference infographic: `uploads/Orion1.png`.

## Surface material — Liquid Glass (signature)
Floating chrome (nav, cohort cards over imagery, masterclass modal, sticky enroll rail, toasts) uses translucent, blurred **liquid glass** that refracts the palette behind it:
```
backdrop-filter: blur(20–30px) saturate(180%);
background: rgba(255,255,255,.14);        /* white veil on colour */
border: 1px solid rgba(255,255,255,.28);  /* top-lit edge */
box-shadow: inset 0 1px 0 rgba(255,255,255,.45), 0 12px 40px rgba(14,14,20,.24);
```
Always ship a solid fallback. **Chrome only** — never a reading surface, never glass-on-glass, always ≥AA contrast. Full spec + live demo in `docs/brand-kit/Tayana Brand Book v5 - Vibrant Magician Final.html` §14.

## Type & voice
- Inter (400→900 display/body), JetBrains Mono (all labels/nav/ledes/data), Instrument Serif italic (emphasis spans in H1/H2 only — the `.em` class). All on Google Fonts.
- Voice: institutional, premium, invitation-led. Reader = "you", academy = "we". Headlines capitalize, ≤12 words, no exclamation marks, no emoji, no hype. Middot `·` separator. Proof is concrete + anonymized. Never append "AI" to the master mark; pillars are never standalone brands.

## Logo
`assets/tayana-mark.svg` (full colour), `-mono.svg`, `-white.svg`. Favicons in `assets/` (svg + 32/180/192/512 png). The mark = mortarboard + Sun tassel over three ascending bars (Indigo · Ink · Spring). Never skew, shadow, recolour off-palette, or add "AI". Brand-book logo page: `Tayana Logo Sheet.html`.

## Page inventory
| File | Purpose |
|---|---|
| `index.html` | Home — long-scroll one-pager (hero, pillar carousel, tabs, outcomes calculator, pricing, FAQ, CTA) |
| `builders.html` | Builders pillar — **Orion pathway + screening paths + 4 tracks** |
| `consumers.html` | Consumers pillar — 30-day model + themed cohorts |
| `pillars.html` | Side-by-side Builders vs Consumers comparison |
| `catalog.html` | Course catalog — Orion pathway strip + 4 tracks + Consumers + Projects tabs |
| `pricing.html` | Per-pillar pricing + financing + FAQ (figures indicative — confirm before launch) |
| `cohort.html` | Cohort detail template (AI Engineer · Spring 2026) — gated syllabus + sticky enroll |
| `contact.html` | Admissions vs partnerships routing + form + Atlanta address |
| `hire-talent.html` | **Employer surface** — all four roles, what they deliver, why hire, sample profiles |
| `enroll.html` | Razorpay checkout (UPI-first) — see `PAYMENTS.md` |
| `mentors · outcomes · reviews · resources · about · for-teams` | Supporting pages |
| `track-no-code-agent-engineer` · `track-pro-code-agent-engineer` · `track-ai-engineer` · `track-ml-engineer` | The four track detail pages |
| `project-qa-chatbot.html` | Project detail template |

Shared: `ds-tokens.css` (tokens), `tayana-2026.css` (components), `tayana-2026.js` (interactions), `image-slot.js`,
`tayana-chat.js` (concierge), `payments-config.js` (prices/keys). `assets/logos/` holds 25 official third-party
tool marks — these carry their vendors' own brand colours and are the one place hex values outside the palette are allowed. Nav + footer markup is repeated per page — keep them in sync when editing.

## Still to wire before launch (fakes to replace)
See `docs/DNS-CUTOVER.md` for the full cutover checklist, including the
noindex header that must stop applying on the real domain.
- Forms are wired to `/api/lead` → set `LEAD_WEBHOOK_URL` in Vercel to receive submissions (see `FORMS.md`). Until then they show the admissions email rather than a false success.
- Cohort seats / next-start dates are hardcoded → make live.
- Pricing figures are **indicative** → confirm real numbers.
- Photography is placeholder (grayscale + initials) → real documentary shots, people-first (no AI-brain/blue-glow stock).
- Icons are inline SVG placeholders → optional 32-icon library commission.

## Editing rules
- Match the existing visual vocabulary (`.section`, `.wrap`, `.section-q`+`.em`, `.tag-frame` with `.cb-*` corners, `.btn-primary`/`.btn-brass`/`.btn-ghost`, `.reveal`). Don't invent new components when one exists.
- Keep pillar discipline: Indigo (`--copper`) for Builders surfaces, Spring (`--brass`) for Consumers. Never mix on one surface.
- Close every element, double-quote attributes, use flex/grid + `gap`.
- Reference docs (not shipped pages): `docs/brand-kit/` holds the **brand book** (palette, type,
  voice, logo rules, Liquid Glass §14) and the **logo sheet** — see `docs/brand-kit/README.md`.
  The pillars have two accent sets, dark-surface and light-canvas; `ds-tokens.css` is canonical.
  The site is **light mode only** — there is no dark theme and no toggle. Every page pins
  `data-theme="light"` and the `[data-theme="light"]` selectors depend on it, so keep the
  attribute. The book's dark-surface accents document print/imagery use, not a site theme.
  Not in this repo: `Tayana - Changelog and Status.html`, `Tayana × 365 - Site Blueprint.html`.
