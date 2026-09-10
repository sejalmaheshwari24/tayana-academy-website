#!/usr/bin/env python3
"""Inject Open Graph + Twitter card tags into every page.

Idempotent: re-run after editing a <title> or description and the block is
rewritten from the page's own values. Absolute URLs point at the LIVE domain,
not the preview — cards are what people see after launch, and hardcoding the
vercel.app host would leak the preview and break when it is removed.
"""
import re, os, glob, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SITE)

DOMAIN = "https://tayanaacademy.com"          # apex; see docs/DNS-CUTOVER.md
CARD   = f"{DOMAIN}/assets/og-card.png"       # 1200x630
NAME   = "Tayana Academy"
START, END = "<!-- OG:START -->", "<!-- OG:END -->"

def esc(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))

def block(title, desc, url):
    t, d = esc(title), esc(desc)
    return f"""{START}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{CARD}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{CARD}">
  {END}"""

changed = []
for path in sorted(glob.glob("*.html")):
    s = open(path, encoding="utf-8").read()
    mt = re.search(r"<title>(.*?)</title>", s, re.S)
    md = re.search(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', s, re.S)
    if not mt or not md:
        print(f"  SKIP {path}: missing title or description"); continue
    title = " ".join(mt.group(1).split())
    desc  = " ".join(md.group(1).split())
    url = DOMAIN + "/" + ("" if path == "index.html" else path)
    new = block(title, desc, url)

    if START in s:                                  # rewrite in place
        s2 = re.sub(re.escape(START) + r".*?" + re.escape(END), new, s, flags=re.S)
    else:                                           # insert after the description
        s2 = s[:md.end()] + "\n  " + new + s[md.end():]
    if s2 != s:
        open(path, "w", encoding="utf-8").write(s2); changed.append(path)

print(f"og tags written: {len(changed)} page(s)")
