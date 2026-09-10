# Contributing

Plain HTML, CSS and JS in one folder. **No framework, no build step** — every
page is directly editable. Please keep it that way.

Read `CLAUDE.md` first: it is the brief covering brand, the course model, and
the editing rules.

## Workflow

`main` deploys to production automatically, in about 25 seconds. So:

```bash
git checkout -b your-change
# edit
python3 scripts/audit-course-language.py   # must pass — it also gates the deploy
git push -u origin your-change
# open a pull request
```

Never push straight to `main`. CI runs the audit and the form tests on every
pull request.

To see what is actually deployed right now:

```bash
curl https://tayana-academycd.vercel.app/deploy-info.json
```

It is written during the build, so it reports the real live commit — not what
you hope is live.

## Before you push

```bash
python3 scripts/audit-course-language.py   # course language, prices, forms
node scripts/test-lead.js                  # form endpoint behaviour
```

The first one runs as the Vercel build command, so **a failing audit fails the
deploy** — the site simply will not update until it passes.

## Generated content — do not hand-edit

Some blocks are written by scripts and sit between HTML comment fences. Edit the
script and re-run it; hand edits are overwritten on the next run.

| Fence | Script | What |
|---|---|---|
| `<!-- ROLE:… -->` | `scripts/build-role-sections.py` | Track page role content |
| `<!-- SYLLABUS -->` | `scripts/syllabi.py` | Week-by-week syllabi |
| `<!-- OG:START -->` | `scripts/og-tags.py` | Social cards |
| form `name` attributes | `scripts/wire-forms.py` | Form wiring |

Each is idempotent — safe to re-run.

## House rules

- Style against `var(--*)` tokens and existing classes. **Never hardcode a hex
  value**; `ds-tokens.css` is canonical.
- Keep pillar discipline: Indigo (`--copper`) for Builders, Spring (`--brass`)
  for Consumers. Never mix on one surface.
- **No prices anywhere.** Everything reads "shared at the masterclass"; the
  audit fails on a rendered price.
- Use the canonical track names — No-Code Agent Engineers, Pro-Code Agent
  Engineers, AI Engineer, Machine Learning Engineers. The audit fails on
  retired names.
- The site is **light mode only**. There is no dark theme.

## Docs

| File | What |
|---|---|
| `CLAUDE.md` | The brief — brand, course model, editing rules |
| `BUILD.md` | The generator scripts |
| `FORMS.md` | Form wiring and how to switch it on |
| `PAYMENTS.md` | Razorpay setup |
| `docs/DNS-CUTOVER.md` | Launch checklist |
| `docs/brand-kit/` | Brand book and logo sheet |
