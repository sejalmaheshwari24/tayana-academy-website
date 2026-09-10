# Tayana × 100x — Comb-Scan Audit & Final Work Plan
*Jul 2026 · built from 3 screen recordings (landing 50 frames · enterprise 21 · detail 11) + live DOM verification.*

## Legend
✅ implemented & verified · 🔧 implemented this round · ⏳ needs real assets/data (user) · 🚫 intentionally not copied (brand rules win)

---

## Section-by-section: index

| # | Segment | 100x nuance | Tayana state |
|---|---------|-------------|--------------|
| 1 | Nav | mono uppercase links in gray shell, gradient CTA w/ offset border | ✅ mono links, gradient CTA, §14 glass shell |
| 2 | Hero headline | condensed all-caps 3-line, accent line 2 | 🚫 kept Tayana serif-em sentence case (brand book locked); tension moved to copy |
| 3 | Hero sub | mono body | ✅ + concrete promise (6 wks / 30 days) |
| 4 | Hero CTAs | ghost + tinted, both with → arrows, zero-risk microcopy near | 🔧 arrows added, "Free · live session · no card" microcopy |
| 5 | Hero ticker | full-bleed dark panel, glyph-matrix texture, WHITE msg cards, colored header bands (orange staff / black member), avatars overlapping card edge w/ ring, emoji reaction counters hanging off bottom edge, continuous scroll | 🔧 rebuilt to exact anatomy: right-edge bleed, indigo glyph-matrix (data-URI), white cards, indigo/spring/sun bands, −24px overlapping ringed avatars, reaction chips overlapping card bottom, scroll + pause-on-hover |
| 6 | Date chips | gray panels, 4 crop corners, mono caps label, bold accent value | 🔧 4-corner crop (layered gradients), ember corners, copper values |
| 7 | Stats | flat panels + striped pocket cards w/ peeking photos that lift on hover, giant accent numerals | ✅ 2 pockets (alumni initials, partner chips) + 2 flat panels w/ 4-corner crops, 54px numerals |
| 8 | Tick ruler | measuring-tape divider strip before statement | 🔧 `.ruler` two-layer tick gradient |
| 9 | Statement | giant claim, accent second line, mono sub | ✅ |
| 10 | Leader quote wall | duotone B/W portraits + red quote chips (Jensen/Varun) | ⏳ needs licensed portraits — quote-chip pattern built on reviews; wire wall when photos exist |
| 11 | Capability grid | gray panels, accent outline icons, 4 crop corners | ✅ 8 panels, 4-corner crops |
| 12 | Persona quotes | red quote chip, mono accent attribution | ✅ persona cards w/ pillar-accent routes |
| 13 | Curriculum | week-range accordion on SOLID accent band, white cards, duotone module images | ✅ indigo band + white cards (builders.html) · ⏳ duotone module images |
| 14 | Success story | duotone portrait panel + SUCCESS STORY crop chip + accent-highlight headline | ✅ chip + case layout · ⏳ real portrait for duotone |
| 15 | Community band | masonry chat cards, light | ✅ light paper cards |
| 16 | Alumni logos | real brand logos | ⏳ verify employer list before using real marks (text cells now) |
| 17 | Partners band | OpenAI/Meta co-brand panels on accent bg | ✅ text band (Anthropic·Microsoft·Zoho·n8n·CrewAI) · ⏳ real logo assets + co-brand panels |
| 18 | Event photos | photo grid w/ red crop corners | ⏳ real photography |
| 19 | Pricing card | strike price/EMI/reserve | 🚫 removed by founder decision; What-you-get + Apply instead |
| 20 | FAQ | "Still wondering if this is for you?" | ✅ (pricing) |
| 21 | Footer | LIGHT, mono accent labels, ascii brand graphic, contact mono block | ✅ light footer + Tayana-mark ASCII |

## Subpages
- **reviews**: 🔧 quote chips (indigo/spring), mono uppercase accent names, cohort labels, video slots (⏳ real videos)
- **builders**: ✅ indigo curriculum band, Orion pathway, stack table · ⏳ module duotone images
- **pricing**: ✅ no figures, chips, apply CTAs
- **catalog**: ✅ outcome-led kickers · consider pocket cards for track categories (next round if wanted)
- **enterprise/for-teams**: ⏳ rebuild to 100x /workshop pattern — giant "For Businesses" two-tone headline, partner strip, crop-chip labels, mono-label light form, ascii footer (form fields exist; **form wiring = user**)

## Remaining (user-owned or asset-gated)
1. **Form wiring** — user does (registration, scoping, newsletter, contact).
2. Real photography (people-first documentary) → unlocks duotone treatments, quote wall, event grid.
3. Video testimonials → 3 slots ready on reviews.
4. Real cohort dates/seats + confirmed pricing.
5. Partner/alumni logo licenses → swap text cells for marks.
6. Deploy (Vercel recommended, DNS cutover from Lovable).
