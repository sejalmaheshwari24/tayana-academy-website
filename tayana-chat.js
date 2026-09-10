/* Tayana Concierge — chat widget.
   Scripted Orion-aware brain by default (no backend, instant).
   Set CHAT_ENDPOINT to a serverless proxy (POST {message, history} -> {reply})
   and it becomes a live LLM assistant. Keep API keys server-side only. */
(function () {
  var CHAT_ENDPOINT = '';

  var BRAIN = [
    { k: /pillar|which (path|track)|where do i start|beginner|no (coding|tech)/i,
      a: "Two pillars. <b>Builders</b> (Indigo) — you're entering an AI career: 4–6 week cohort, you leave with a deployed portfolio project and a placement pathway. <b>Consumers</b> (Spring) — you apply AI to the role you already have: 30 days, one workflow shipped to production. No tech background? The Consumers pillar was made for you.",
      c: [["See Builders", "builders.html"], ["See Consumers", "consumers.html"]] },
    { k: /track|agent engineer|agentic|machine learning|ml engineer|ai engineer|pro[- ]code|full[- ]code|low[- ]code|no[- ]code|curriculum|syllabus/i,
      a: "Four Builders career tracks on Orion: <b>No-Code Agent Engineers</b> (no coding required), <b>Pro-Code Agent Engineers</b> (Python · LangChain, CrewAI, MCP), <b>AI Engineer</b> (full-stack · RAG, LLM products), and <b>Machine Learning Engineers</b> (Python · training, evals, MLOps). Screening places you where you'll succeed.",
      c: [["View catalog", "catalog.html"], ["How screening works", "builders.html"]] },
    { k: /date|start|when|next cohort|masterclass|schedule/i,
      a: "Cohorts start on the <b>1st and 15th monthly</b>, small by design — 24 Builders or 20 Consumers seats. The free masterclass is the door: a live working session, pillar fit assessment, and the full curriculum walkthrough.",
      c: [["Register free", "contact.html"]] },
    { k: /price|cost|fee|pay|emi|money|afford/i,
      a: "Every seat includes the same three things: <b>hands-on experience</b>, a <b>certificate</b>, and <b>placement assistance</b> — nothing gated. Selection is application-based. Start with the free masterclass; admissions walks you through the rest on a call.",
      c: [["What's included", "pricing.html"], ["Apply", "contact.html"]] },
    { k: /mentor|teacher|instructor|who teaches/i,
      a: "Working operators, not lecturers — every mentor ships AI for a living and reviews your project weekly. Indigo mentors for Builders, Spring for Consumers.",
      c: [["Meet the mentors", "mentors.html"]] },
    { k: /outcome|job|placement|salary|hired|career/i,
      a: "9 in 10 alumni land or advance a role within months of finishing. You leave with proof of work — a deployed project, not a certificate wall. 2,000+ alumni across both pillars since 2023.",
      c: [["Read outcomes", "outcomes.html"]] },
    { k: /team|company|enterprise|business|corporate|pilot/i,
      a: "For teams we run <b>30-day pilots</b> scoped to one workflow, measured against your real baseline — 10,000+ hours of corporate training delivered. It starts with a scoping call.",
      c: [["Team pilots", "for-teams.html"]] },
    { k: /orion|lms|platform/i,
      a: "<b>Orion</b> is our in-house LMS. One pathway for everyone: Join → AI Foundation 1 & 2 → Career Assessment → Technical Screening → your track. Live sessions, project briefs, and mentor reviews all run on it.",
      c: [["See the pathway", "builders.html"]] },
    { k: /hi|hello|hey|namaste/i,
      a: "Welcome. I can help you pick a pillar, explain the four career tracks, or get you into the next free masterclass. What's the work in front of you?",
      c: [["Find my pillar", "pillars.html"], ["Free masterclass", "contact.html"]] }
  ];
  var FALLBACK = { a: "Good question — that one's better answered by a human. Register for the free masterclass and ask it live, or write to us from the contact page and admissions will come back to you.",
    c: [["Free masterclass", "contact.html"], ["Contact", "contact.html"]] };

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  var launcher = el('button', 'tc-launch', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22"><path d="M21 11.5a8.38 8.38 0 01-9 8.4 8.5 8.5 0 01-3.4-.7L3 21l1.8-4.6a8.38 8.38 0 01-1.3-4.9 8.5 8.5 0 018.5-8.5 8.38 8.38 0 019 8.5z"/></svg><span>Ask Tayana</span>');
  launcher.type = 'button'; launcher.setAttribute('aria-label', 'Open Tayana concierge chat');

  var panel = el('section', 'tc-panel');
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Tayana concierge');
  panel.innerHTML =
    '<header class="tc-head"><div><b>Tayana Concierge</b><span>Usually replies instantly</span></div><button type="button" class="tc-close" aria-label="Close chat">&#10005;</button></header>' +
    '<div class="tc-log" aria-live="polite"></div>' +
    '<form class="tc-form"><input type="text" placeholder="Ask about tracks, dates, pillars…" aria-label="Your question"><button type="submit" class="tc-send" aria-label="Send">&#8594;</button></form>';

  var log, input;
  function push(kind, html, chips) {
    var m = el('div', 'tc-msg ' + kind, html);
    log.appendChild(m);
    if (chips && chips.length) {
      var row = el('div', 'tc-chips');
      chips.forEach(function (c) { var a = el('a', 'tc-chip', c[0]); a.href = c[1]; row.appendChild(a); });
      log.appendChild(row);
    }
    log.scrollTop = log.scrollHeight;
  }
  function answer(q) {
    if (CHAT_ENDPOINT) {
      var typing = el('div', 'tc-msg bot tc-typing', '&#8230;'); log.appendChild(typing); log.scrollTop = log.scrollHeight;
      fetch(CHAT_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: q, page: location.pathname }) })
        .then(function (r) { return r.json(); })
        .then(function (d) { typing.remove(); push('bot', d.reply || FALLBACK.a, d.chips || FALLBACK.c); })
        .catch(function () { typing.remove(); var hit = match(q); push('bot', hit.a, hit.c); });
      return;
    }
    var hit = match(q);
    setTimeout(function () { push('bot', hit.a, hit.c); }, 380);
  }
  function match(q) { for (var i = 0; i < BRAIN.length; i++) if (BRAIN[i].k.test(q)) return BRAIN[i]; return FALLBACK; }

  function mount() {
    document.body.appendChild(launcher); document.body.appendChild(panel);
    log = panel.querySelector('.tc-log'); input = panel.querySelector('input');
    launcher.addEventListener('click', function () {
      var open = panel.classList.toggle('open'); launcher.classList.toggle('hide', open);
      if (open && !log.children.length) push('bot', BRAIN[BRAIN.length - 1].a, BRAIN[BRAIN.length - 1].c);
      if (open) input.focus();
    });
    panel.querySelector('.tc-close').addEventListener('click', function () { panel.classList.remove('open'); launcher.classList.remove('hide'); launcher.focus(); });
    panel.querySelector('.tc-form').addEventListener('submit', function (e) {
      e.preventDefault(); e.stopPropagation();
      var q = input.value.trim(); if (!q) return;
      push('user', q.replace(/</g, '&lt;')); input.value = '';
      answer(q);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('open')) { panel.classList.remove('open'); launcher.classList.remove('hide'); launcher.focus(); } });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
