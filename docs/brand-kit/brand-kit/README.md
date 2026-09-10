# Brand kit

Reference documents — not shipped pages. Open in a browser.

- **Tayana Brand Book v5 - Vibrant Magician Final.html** — the locked direction.
  Palette (dark-surface *and* light-canvas sets), type, voice, logo rules,
  and the Liquid Glass spec in §14.
- **Tayana Logo Sheet.html** — logo construction, clear space, misuse.

The logo files themselves are **not duplicated here** — they live in `assets/`,
where the site loads them from:
`tayana-mark.svg`, `tayana-mark-mono.svg`, `tayana-mark-white.svg`,
`tayana-logo-full.png`, `tayana-logo-mark.png`.

## Two accent sets, one system

The pillars have different values on dark and on light. Both are correct; use the
one that matches the surface.

| | Dark surfaces / imagery | Light canvas (what the site ships) |
|---|---|---|
| Builders indigo | `#5B47FF` | `#4A38E8` (`--copper`) |
| Consumers spring | `#9EE89C` | `#368634` (`--brass`) |

Light-canvas values are darkened for contrast on `--ash #F8F8F6`. Never put white
text on the dark-surface Spring `#9EE89C` — it is a light colour and takes ink text.

Contrast: white on `--brass #368634` measures **4.55** — passes AA for normal text.
As *text* on the ash canvas it is **4.28**, which is AA Large only, so accent-coloured
copy under 24px (or under 19px bold) uses `--brass-deep #2B7629` instead (5.30 on ash).
Builders indigo needs no such care: 6.95 on fill, 6.53 as text.

Soft-surface chips (entry badges, path requirements) pair `--brass-deep` on
`--brass-soft`: **4.70**. These chips run 10.5–11px, so they need the full 4.5 —
that pairing is why `--brass-deep` is #2B7629 and not lighter.

Canonical token values live in `ds-tokens.css`; that file wins on any disagreement.
