#!/usr/bin/env python3
"""Wire every form to /api/lead: name attributes, honeypot, data-form, script tag.

Idempotent — re-run after editing a form. Fields are matched by their <label>,
so a renamed label needs its entry updating here rather than hand-editing HTML.
"""
import re, os, glob

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SITE)

# label text -> field name, per form
CONTACT = {
    "Name": "name", "Email": "email", "I'm interested in": "interest",
    "Company / role (optional)": "company_role",
    "What do you want to build or apply?": "message",
    "Team size": "team_size", "Function": "function",
    "Timeline": "timeline", "Budget owner": "budget_owner",
}
TEAM = {
    "First name": "first_name", "Last name": "last_name",
    "Work email": "email", "Company": "company",
    "Which workflow would you pilot?": "workflow",
    "Team size for the pilot": "team_size",
}

HONEYPOT = ('<div class="hp" aria-hidden="true" '
            'style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden">'
            '<label>Company website<input type="text" name="company_website" '
            'tabindex="-1" autocomplete="off"></label></div>')

def name_by_label(html, mapping):
    """Give each labelled control a name attribute (idempotent)."""
    n = 0
    for label, field in mapping.items():
        # <label>Label</label> followed by the control it describes
        pat = re.compile(
            r'(<label>' + re.escape(label) + r'</label>\s*)'
            r'(<(?:input|textarea|select)\b)((?:(?!\bname=)[^>])*?)(/?>)',
            re.S)
        def add(m):
            return f'{m.group(1)}{m.group(2)} name="{field}"{m.group(3)}{m.group(4)}'
        html, k = pat.subn(add, html)
        n += k
    return html, n

def wire(path, form_re, form_id, mapping, success):
    s = open(path, encoding="utf-8").read()
    m = form_re.search(s)
    if not m:
        return None
    start = m.start()
    end = s.index("</form>", start) + len("</form>")
    block = s[start:end]

    block, named = name_by_label(block, mapping) if mapping else (block, 0)

    # replace the opening tag with a declarative one
    open_tag = re.match(r"<form[^>]*>", block, re.S).group(0)
    new_open = (f'<form data-form="{form_id}" '
                f'data-success="{success}" novalidate>')
    block = block.replace(open_tag, new_open, 1)

    if "company_website" not in block:
        block = block.replace(new_open, new_open + "\n        " + HONEYPOT, 1)

    if block != s[start:end]:
        s = s[:start] + block + s[end:]
        open(path, "w", encoding="utf-8").write(s)
        return named
    return 0

changed = {}

n = wire("contact.html", re.compile(r"<form[^>]*>", re.S), "contact", CONTACT,
         "Thanks — we'll be in touch with your cohort date.")
if n: changed["contact.html"] = n

n = wire("for-teams.html",
         re.compile(r'<form[^>]*(?:class="lead-form"|data-form="team-pilot")[^>]*>', re.S),
         "team-pilot", TEAM, "Thanks — we'll reach out to scope your pilot.")
if n: changed["for-teams.html"] = n

# newsletter forms: a single email input, repeated across pages
NEWS = re.compile(r'<form(?![^>]*data-form)[^>]*>(?:(?!</form>).)*?'
                  r'type="email"(?:(?!</form>).)*?</form>', re.S)
for path in sorted(glob.glob("*.html")):
    s = open(path, encoding="utf-8").read()
    out, k = s, 0
    for m in list(NEWS.finditer(s)):
        block = m.group(0)
        if 'data-form=' in block:
            continue
        nb = re.sub(r'(<input\b)((?:(?!\bname=)[^>])*?type="email")',
                    r'\1 name="email"\2', block)
        nb = re.sub(r"<form[^>]*>",
                    '<form data-form="newsletter" '
                    'data-success="You&#39;re subscribed — field notes land twice a month." '
                    'novalidate>', nb, count=1)
        if "company_website" not in nb:
            nb = nb.replace(">", ">\n        " + HONEYPOT, 1)
        out = out.replace(block, nb, 1); k += 1
    if k:
        open(path, "w", encoding="utf-8").write(out)
        changed[path] = changed.get(path, 0) + k

# make sure forms.js is loaded everywhere a wired form lives
for path in sorted(glob.glob("*.html")):
    s = open(path, encoding="utf-8").read()
    if 'data-form=' not in s or 'src="forms.js"' in s:
        continue
    s = s.replace("</body>", '  <script src="forms.js" defer></script>\n</body>', 1)
    open(path, "w", encoding="utf-8").write(s)

print("wired:", ", ".join(f"{k}" for k in sorted(changed)) or "nothing")
