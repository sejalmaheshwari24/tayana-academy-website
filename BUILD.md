# Tayana Academy — Fable Build Package

This folder is a **self-contained, ready-to-open** Tayana Academy website: plain HTML/CSS/JS, no build step. Open `index.html` or point Fable / Claude Code at this folder. `CLAUDE.md` is the brand + content brief the agent should read first.

## Run it
Open any `.html` directly in a browser, or serve the folder statically (e.g. `python3 -m http.server`). No install, no dependencies — fonts load from Google Fonts CDN. There is intentionally **no framework and no bundler**; keep it that way so every page stays directly editable.

## What's inside
- **Site pages** — `index.html` (home) + `builders` `consumers` `pillars` `catalog` `pricing` `cohort` `contact` `mentors` `outcomes` `reviews` `resources` `about` `for-teams` + `track-ai-engineer` / `project-qa-chatbot` (detail templates).
- **System** — `ds-tokens.css` (Vibrant Magician tokens), `tayana-2026.css` (components), `tayana-2026.js` (interactions), `image-slot.js`.
- **`assets/`** — logo (colour / mono / white), favicons (svg + 32/180/192/512 png).
- **`CLAUDE.md`** — the persistent build brief. Read first.
- **Reference (not shipped pages)** — `Tayana Brand Book v5…`, `Tayana Logo Sheet`, `Tayana - Changelog and Status`, `Tayana × 365 - Site Blueprint`.

## Direction (locked)
**Vibrant Magician · light mode.** Indigo `#4A38E8` (Builders) · Spring `#368634` (Consumers) · Sun `#FFD23F` (attention) · Ink text. In `ds-tokens.css` the legacy names map `--copper`→Indigo and `--brass`→Spring — style against the `var(--*)` tokens and existing classes, never hardcode hex. Magician × Sage is retired (in `archive/` in the working project, not shipped here).

## Component system (how to extend)
Reuse these before inventing anything — full inventory in `tayana-2026.css`:
`.section` / `.section-tight` / `.section-dark` layout · `.wrap` container · `.eyebrow` + `.section-q` (with `.em` serif-italic accent) headings · `.tag-frame` with `.cb-*` plus-corners · buttons `.btn-primary` (Indigo) / `.btn-brass` (Spring) / `.btn-ghost` · `.reveal` scroll-in · `.glass` liquid-glass surface. Pillar discipline is strict: Indigo for Builders surfaces, Spring for Consumers, never mixed on one surface.

## Recent marketing additions (already in these files)
Shared components live in `tayana-2026.css`; page markup is inline per page.
- **Hero date-triad** (`.date-triad`) — cohort-facts band (next masterclass / next cohort / length) on `index`, `builders`, `consumers`.
- **Community feed** (`.community-feed` / `.cf-card`) — dark-band section of cohort messages on `index`.
- **Featured outcome cases** (`.case-grid` / `.case`) — three named, concrete-but-anonymized case cards on `outcomes.html`.
- **Expanded pricing** — strike + discounted price, interest-free EMI line, commitment/selection chips, and a "what every seat includes" band with deposit + admission facts on `pricing.html`.
- **Code vs No-Code stack table** (`.stack-cmp`) — two-column tool-stack comparison tied to Orion screening on `builders.html`.
- **Trust badges** (`.trust-strip` / `.trust-badge`) — sourced ratings strip on `index`.
- **Footer newsletter** (`.footer-news`) — capture band in the `index` footer.
- **Contact qualifiers** (`.qual`) — optional teams/partnerships fields (team size, function, timeline, budget owner) on `contact.html`.
- **Mentors** — 8 bios enriched with experience + track meta.

## Build / launch checklist
Done ✓ / To do ☐

- ✓ Single locked direction (Vibrant Magician, light); old direction archived.
- ✓ Logo mark + favicons generated and wired into every page `<head>`.
- ✓ Orion course model threaded through structure: pathway + screening paths + 4 tracks on Builders, catalog strip, cohort mapped to a track, home carousel + cohort names.
- ✓ 16 pages consistent on one component system; nav/footer synced.
- ☐ **Forms are front-end only** — replace toasts on registration, scoping-call, newsletter, and the contact form (incl. new partnership qualifiers) with real CRM/email + cohort-date assignment.
- ☐ **Make cohort data live** — seats and next-start dates are hardcoded (date-triads currently read "Mar 3 / Mar 15, 2026"; contact/pricing say 24 Builders / 20 Consumers).
- ☐ **Confirm real pricing** — figures on `pricing.html` (incl. strike prices, EMI, $200 deposit) are indicative.
- ☐ **Verify trust-badge scores** — G2 / Course Report / Google numbers on `index` are placeholders; the strip carries a visible "verify before launch" note. Wire to real review-platform data or remove.
- ☐ Real photography — people-first documentary shots; replace grayscale/initials placeholders.
- ☐ Optional: commission the 32-icon library (inline SVG placeholders today).
- ☐ Implement Liquid Glass material on live nav/modals/cohort cards (spec in brand book §14).
- ☐ Propagate the footer newsletter capture to subpage footers if desired (currently on `index` + `resources`), and wire the footer "Resources" placeholder links or remove.

## Information architecture
```
Home (index)
├── Pillars ─ Builders ─ (Orion pathway · screening · 4 tracks · Code/No-Code stack) ─ Catalog ─ Cohort detail
│           └ Consumers ─ (30-day model · themed cohorts) ─ Catalog
├── Catalog ─ track & project detail templates
├── Pricing (per pillar + financing + what's-included)
├── Outcomes · Mentors · Reviews · Resources · About · For-teams
└── Contact (admissions / partnerships + form with team qualifiers)
```

Full page-by-page wireframes and the 30-page IA map are in `Tayana × 365 - Site Blueprint.html`.

## For Claude Code / Fable
Point the agent at this folder. It will read `CLAUDE.md` (brand + content brief) automatically. When adding surfaces, keep them consistent with the Orion course model and the component system above, and preserve pillar colour discipline. Nav + footer markup is repeated per page — keep them in sync when editing.

## Social cards
`scripts/og-tags.py` writes the OG + Twitter block into every page from that
page's own `<title>` and `<meta name="description">`, between `<!-- OG:START -->`
fences. Idempotent — re-run after editing a title or description. The card image
is `assets/og-card.png` (1200x630). URLs are absolute against the live domain
(`DOMAIN` at the top of the script), not the preview.
