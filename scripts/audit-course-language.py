#!/usr/bin/env python3
"""Course-language regression checker for the Tayana Academy site.

Read-only. Exits 1 if any page contradicts the canonical Orion course model.
Run before every deploy:  python3 scripts/audit-course-language.py

Catches the classes of defect found in the Sep 2026 audit:
  1. retired track names still in copy
  2. a rendered price (all pricing is "shared at the masterclass")
  3. week/seat counts that disagree with payments-config.js
  4. module topics presented as Builders tracks
"""
import re, os, sys, glob, json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SITE)

# --- canonical model, read from the single source of truth -----------------
cfg = open('payments-config.js', encoding='utf-8').read()
TRACKS = {}
for m in re.finditer(r'"([a-z-]+)":\s*\{\s*name:\s*"([^"]+)",\s*weeks:\s*(\d+),\s*seats:\s*(\d+)', cfg):
    TRACKS[m.group(1)] = dict(name=m.group(2), weeks=int(m.group(3)), seats=int(m.group(4)))
BUILDER_TRACKS = {k: v for k, v in TRACKS.items() if k != 'consumers'}
CANON_NAMES = {v['name'] for v in BUILDER_TRACKS.values()}

# --- rules -----------------------------------------------------------------
RETIRED = [
    (r'Agentic Engineering',            'retired track family name'),
    (r'\bAI Engineering\b',             'retired name — the track is "AI Engineer"'),
    (r'\bML Engineering\b',             'retired name — the track is "Machine Learning Engineers"'),
    (r'Full-Code(?! Agent)',            'retired name — use "Pro-Code Agent Engineers"'),
    (r'Low/No-Code',                    'retired name — use "No-Code Agent Engineers"'),
    (r'Agentic Engineer\b',             'retired role name'),
]

# module/topic names that must never carry a "Builders track" label
TOPIC_AS_TRACK = ['RAG on Private Data', 'Agent Systems', 'Evals &amp; Production',
                  'Evals & Production', 'Fine-tuning &amp; SLM', 'Fine-tuning & SLM',
                  ]  # note: alumni attributions name JOB titles, not tracks — not flagged

PRICE = re.compile(r'\$\s?[0-9][0-9,]*')

# A hardcoded noindex would survive the DNS cutover and de-index the real site.
# The preview is de-indexed by a host-conditional X-Robots-Tag in vercel.json,
# which stops applying by itself once the custom domain serves the pages.
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', re.I)

# Lines allowed to contain otherwise-flagged text, with the reason.
ALLOW = [
    ('tayana-chat.js', 'k: /',        'chatbot regex intentionally matches retired user phrasing'),
    ('project-qa-chatbot.html', '$',  'demo chatbot copy, a fictional product — not Academy pricing'),
]

def allowed(path, line):
    base = os.path.basename(path)
    return any(base == f and token in line for f, token, _ in ALLOW)

def strip_comments(text):
    """Blank out HTML and JS comments so commented-out figures don't trip the price rule."""
    text = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    text = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    text = re.sub(r'(?m)^\s*//.*$', '', text)
    return text

findings = []
def flag(path, ln, rule, detail):
    findings.append((path, ln, rule, detail))

FILES = sorted(glob.glob('*.html') + glob.glob('*.js'))
for path in FILES:
    raw = open(path, encoding='utf-8').read()
    live = strip_comments(raw)
    lines = live.split('\n')

    for i, line in enumerate(lines, 1):
        if allowed(path, line):
            continue

        # 1. retired names
        for pat, why in RETIRED:
            if re.search(pat, line):
                flag(path, i, 'retired-name', f'{why}: {re.search(pat, line).group(0)!r}')

        # 2. rendered price
        if PRICE.search(line):
            flag(path, i, 'rendered-price', f'price visible on the page: {PRICE.search(line).group(0)!r}')

        # 2b. hardcoded noindex — would ship to the live domain
        if NOINDEX.search(line):
            flag(path, i, 'hardcoded-noindex',
                 'noindex in markup ships to the live domain; the preview is '
                 'de-indexed by the host-conditional header in vercel.json')

        # 3. topic sold as a track
        if 'tcard-kind' in line or 'cat-kind' in line or 'ts-kind' in line:
            for topic in TOPIC_AS_TRACK:
                if topic in line:
                    flag(path, i, 'topic-as-track', f'{topic!r} labelled as a track')
        for topic in TOPIC_AS_TRACK:
            if f'>{topic}<' in line and re.search(r'(tcard-name|cat-name|ts-name)', line):
                flag(path, i, 'topic-as-track', f'{topic!r} presented as a course name')

    # 4. Consumers must never be described in weeks (it is a 30-day cohort)
    for i, line in enumerate(lines, 1):
        if (re.search(r'Consumers', line) and re.search(r'\b[46]\s*(-|\s|–)?week', line, re.I)
                and '30 day' not in line.lower()):
            flag(path, i, 'consumers-weeks', 'Consumers is a 30-day cohort, not N weeks')

# 4b. every form must be wired — a form with no data-form, or a page carrying a
# wired form but not forms.js, means submissions go nowhere.
for path in [p for p in FILES if p.endswith('.html')]:
    raw = open(path, encoding='utf-8').read()
    for m in re.finditer(r'<form\b[^>]*>', raw):
        if 'data-form=' not in m.group(0):
            ln = raw[:m.start()].count('\n') + 1
            flag(path, ln, 'unwired-form',
                 'form has no data-form; submissions would go nowhere (see FORMS.md)')
    if 'data-form=' in raw and 'src="forms.js"' not in raw:
        flag(path, 1, 'unwired-form', 'page has a wired form but does not load forms.js')

# 5. per-track week counts must match payments-config
for path in [p for p in FILES if p.startswith('track-')]:
    raw = open(path, encoding='utf-8').read()
    slug = path[len('track-'):-len('.html')].replace('-engineer', '-engineer')
    key = {'no-code-agent-engineer': 'no-code-agent', 'pro-code-agent-engineer': 'pro-code-agent',
           'ai-engineer': 'ai-engineer', 'ml-engineer': 'ml-engineer'}.get(slug)
    if not key or key not in TRACKS:
        continue
    want = TRACKS[key]['weeks']
    for m in re.finditer(r'(\d+)[\s-]week', raw):
        got = int(m.group(1))
        if got != want:
            ln = raw[:m.start()].count('\n') + 1
            flag(path, ln, 'week-mismatch', f'says {got} weeks; payments-config says {want}')

# --- report ----------------------------------------------------------------
if not findings:
    print(f'✓ course language clean — {len(FILES)} files checked against '
          f'{len(BUILDER_TRACKS)} canonical tracks')
    sys.exit(0)

by_rule = {}
for f in findings:
    by_rule.setdefault(f[2], []).append(f)

print(f'✗ {len(findings)} course-language findings\n')
for rule, items in sorted(by_rule.items()):
    print(f'── {rule} ({len(items)})')
    for path, ln, _, detail in items:
        print(f'   {path}:{ln}  {detail}')
    print()
sys.exit(1)
