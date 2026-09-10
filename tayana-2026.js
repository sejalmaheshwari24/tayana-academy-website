/* ================================================================
   TAYANA ACADEMY 2026 · interactions
   Marquees · hero wall · pillar carousel · tabs · h-scroll ·
   outcome calculator · before/after drag · accordion · gantt ·
   count-ups · float · nav · toast
   ================================================================ */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- theme: light, locked (dark toggle retired Jul 2026) ---- */
  document.documentElement.setAttribute('data-theme', 'light');
  try { localStorage.removeItem('tayana-theme'); } catch (e) {}

  /* ---- form wiring: one endpoint, every form ----
     Paste your webhook URL (Make.com / Zoho Flow / Formspree) below and
     every form on the site goes live. Empty string = toast-only demo mode. */
  var FORMS_ENDPOINT = '';
  document.addEventListener('submit', function (e) {
    var f = e.target; if (!f || f.tagName !== 'FORM' || f.classList.contains('tc-form')) return;
    if (!FORMS_ENDPOINT) return; /* demo mode: existing toasts handle UX */
    e.preventDefault();
    var data = { page: location.pathname, ts: new Date().toISOString() };
    $$('input, select, textarea', f).forEach(function (el, i) {
      var k = el.name || (el.previousElementSibling && el.previousElementSibling.textContent) || ('field_' + i);
      data[k.trim().toLowerCase().replace(/[^a-z0-9]+/g, '_')] = el.value;
    });
    var btn = f.querySelector('button[type="submit"], .btn'); if (btn) btn.disabled = true;
    fetch(FORMS_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); showToast('Received — we\u2019ll be in touch shortly.'); f.reset(); })
      .catch(function () { showToast('Something went wrong — email hello@tayanaacademy.com and we\u2019ll take it from there.'); })
      .then(function () { if (btn) btn.disabled = false; });
  }, true);
  function showToast(msg) { var t = document.getElementById('toast'); if (!t) return; t.textContent = msg; t.classList.add('show'); setTimeout(function () { t.classList.remove('show'); }, 3200); }

  /* ---- mobile nav: hamburger + glass drawer ---- */
  (function () {
    var shell = document.querySelector('.nav-shell'); if (!shell) return;
    var links = shell.querySelector('.nav-links'); var right = shell.querySelector('.nav-right');
    if (!links || !right) return;
    var b = document.createElement('button');
    b.className = 'nav-burger'; b.type = 'button'; b.setAttribute('aria-label', 'Open menu'); b.setAttribute('aria-expanded', 'false');
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
    var d = document.createElement('nav'); d.className = 'nav-drawer'; d.setAttribute('aria-label', 'Mobile');
    $$('.nav-links a').forEach(function (a) { var x = a.cloneNode(true); var c = x.querySelector('.caret'); if (c) c.remove(); d.appendChild(x); });
    b.addEventListener('click', function () { var open = d.classList.toggle('open'); b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    d.addEventListener('click', function (e) { if (e.target.closest('a')) { d.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { d.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); } });
    right.appendChild(b); document.body.appendChild(d);
  })();

  /* ---- wrap the glass logo in a refraction "lens" so it looks magical
     on any background (bloom of colored light behind the glass) ---- */
  $$('.brand-mark img').forEach(function (im) {
    if (im.parentNode && im.parentNode.classList.contains('logo-lens')) return;
    var lens = document.createElement('span');
    lens.className = 'logo-lens';
    im.parentNode.insertBefore(lens, im);
    lens.appendChild(im);
  });

  /* ---- nav scroll state + scroll-top ---- */
  var nav = $('#nav'), top = $('#scrollTop');
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 10);
    if (top) top.classList.toggle('show', window.scrollY > 800);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---- reveal on scroll (+ safety net) ---- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -7% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
    setTimeout(function () { reveals.forEach(function (el) { el.classList.add('in'); }); }, 600);
  } else { reveals.forEach(function (el) { el.classList.add('in'); }); }

  /* ---- count-ups ---- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '';
    var dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    if (isNaN(target)) return;
    var dur = 1600, start = null;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      var v = target * e;
      el.textContent = pre + (dec ? v.toFixed(dec) : Math.round(v).toLocaleString()) + suf;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    /* rAF can stall (throttled/hidden tabs, some embeds) — guarantee the final value */
    setTimeout(function () {
      el.textContent = pre + (dec ? target.toFixed(dec) : Math.round(target).toLocaleString()) + suf;
    }, dur + 250);
  }
  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting && !e.target.dataset.done) { e.target.dataset.done = '1'; countUp(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
    setTimeout(function () { counters.forEach(function (el) { if (!el.dataset.done) { el.dataset.done = '1'; countUp(el); } }); }, 900);
  } else { counters.forEach(countUp); }

  /* ---- gantt reveal ---- */
  var gantt = $('.gantt');
  if (gantt && 'IntersectionObserver' in window) {
    var gio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { gantt.classList.add('in'); gio.disconnect(); } }); }, { threshold: 0.3 });
    gio.observe(gantt);
    setTimeout(function () { gantt.classList.add('in'); }, 1000);
  } else if (gantt) { gantt.classList.add('in'); }

  /* ---- hero wall: duplicate children for seamless loop ---- */
  $$('.hw-col').forEach(function (col) { col.innerHTML = col.innerHTML + col.innerHTML; });

  /* ---- horizontal marquees: duplicate track ---- */
  $$('.marquee-track').forEach(function (t) { t.innerHTML = t.innerHTML + t.innerHTML; });

  /* ---- pillar carousel ---- */
  var cpc = $('#cpc');
  if (cpc) {
    var slides = JSON.parse(cpc.getAttribute('data-slides'));
    var i = 0;
    var elE = $('.cpc-eyebrow', cpc), elT = $('.cpc-title', cpc), elO = $('.cpc-outcome', cpc), elD = $('.cpc-desc', cpc), elPanel = $('.cpc-panel', cpc);
    function render() {
      var s = slides[i];
      elPanel.style.opacity = 0;
      setTimeout(function () {
        elE.textContent = s.eyebrow; elT.textContent = s.title; elO.textContent = s.outcome; elD.textContent = s.desc;
        var copper = s.tone !== 'brass';
        elO.style.color = copper ? 'var(--copper-light)' : 'var(--brass-light)';
        elE.style.color = copper ? 'var(--copper-light)' : 'var(--brass-light)';
        elPanel.style.opacity = 1;
      }, 200);
    }
    elPanel.style.transition = 'opacity .3s ease';
    $('#cpcPrev').addEventListener('click', function () { i = (i - 1 + slides.length) % slides.length; render(); });
    $('#cpcNext').addEventListener('click', function () { i = (i + 1) % slides.length; render(); });
    var auto = setInterval(function () { i = (i + 1) % slides.length; render(); }, 5500);
    cpc.addEventListener('mouseenter', function () { clearInterval(auto); });
  }

  /* ---- tab browser ---- */
  function selectTab(key) {
    var btn = $$('.tab-btn').filter(function (b) { return b.getAttribute('data-tab') === key; })[0];
    if (!btn) return;
    $$('.tab-btn').forEach(function (x) { x.classList.toggle('on', x === btn); });
    $$('.tab-panel').forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-panel') === key); });
  }
  $$('.tab-btn').forEach(function (b) {
    b.addEventListener('click', function () { selectTab(b.getAttribute('data-tab')); });
  });
  // A link like catalog.html#consumers opens straight into that tab.
  if (location.hash) selectTab(location.hash.slice(1));

  /* ---- horizontal scroll controls ---- */
  $$('[data-hscroll]').forEach(function (ctrl) {
    var target = $('#' + ctrl.getAttribute('data-hscroll'));
    if (!target) return;
    ctrl.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var dir = btn.getAttribute('data-dir') === 'next' ? 1 : -1;
        target.scrollBy({ left: dir * 330, behavior: 'smooth' });
      });
    });
  });

  /* ---- outcome calculator ----
     Cohort length is FIXED, not hours-scalable: Builders run 4 or 6 weeks per
     track, Consumers runs 30 days. Hours/week shapes how much you get out of it,
     not when the cohort ends. Track data comes from payments-config.js. ---- */
  var calc = $('#calc');
  if (calc) {
    var roleSel = $('#calcRole'), hrs = $('#calcHrs'), hrsVal = $('#calcHrsVal');
    var rReady = $('#rReady'), rShip = $('#rShip'), rPlace = $('#rPlace');
    var CFG = (window.TAYANA_PAY && window.TAYANA_PAY.TRACKS) || {};
    var SHIP = {
      'no-code-agent':  'A production agent, handed over',
      'pro-code-agent': 'A deployed multi-agent system',
      'ai-engineer':    'An LLM product in production',
      'ml-engineer':    'An end-to-end ML system',
      'consumers':      'A workflow live in production'
    };
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    function compute() {
      var key = roleSel.value;
      var t = CFG[key] || {};
      var h = parseInt(hrs.value, 10);
      hrsVal.textContent = h + ' hrs';
      var isConsumers = key === 'consumers';
      var days = isConsumers ? 30 : (t.weeks || 6) * 7;
      var done = new Date(Date.now() + days * 86400000);
      rReady.textContent = months[done.getMonth()] + ' ' + done.getFullYear();
      rShip.textContent = SHIP[key] || 'Something shipped';
      rPlace.textContent = isConsumers ? '30 days' : (t.weeks || 6) + ' weeks';
    }
    roleSel.addEventListener('change', compute);
    hrs.addEventListener('input', compute);
    compute();
  }

  /* ---- before / after toggle (crossfade) ---- */
  var ba = $('#ba');
  if (ba) {
    $$('.ba-toggle button', ba).forEach(function (b) {
      b.addEventListener('click', function () {
        ba.classList.toggle('show-after', b.dataset.ba === 'after');
        $$('.ba-toggle button', ba).forEach(function (x) {
          var on = x === b;
          x.classList.toggle('on', on);
          x.setAttribute('aria-selected', on ? 'true' : 'false');
        });
      });
    });
  }

  /* ---- accordion ---- */
  $$('.acc-q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.acc-item');
      var wasCollapsed = item.classList.contains('collapsed');
      $$('.acc-item').forEach(function (x) { x.classList.add('collapsed'); });
      if (wasCollapsed) item.classList.remove('collapsed');
    });
  });

  /* ---- pricing toggle ---- */
  var psw = $('#priceSwitch');
  if (psw) {
    psw.addEventListener('click', function () {
      var monthly = psw.classList.toggle('monthly');
      $$('[data-annual]').forEach(function (el) { el.textContent = monthly ? el.getAttribute('data-monthly') : el.getAttribute('data-annual'); });
      var save = $('#priceSave'); if (save) save.style.visibility = monthly ? 'hidden' : 'visible';
    });
  }

  /* ---- CTA toast ---- */
  var toast = $('#toast'), tt = null;
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove('show'); }, 2600);
  }
  $$('[data-toast]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      if (b.getAttribute('href') === '#contact' || !b.getAttribute('href')) { /* allow scroll */ }
      showToast(b.getAttribute('data-toast'));
    });
  });

  /* ---- consultation CTA dropdown (email / call) ---- */
  // .consult-menu is moved to <body> and positioned as position:fixed
  // in viewport px. A plain position:fixed descendant is only
  // guaranteed to escape an ancestor's overflow:hidden clipping (e.g.
  // .quiz-banner's clipped stripe background) as long as no ancestor
  // has a transform/filter/will-change — several sections use .reveal,
  // which does — so re-parenting to <body> is the one fix that works
  // regardless of which section the trigger lives in.
  function placeConsultMenu(menu, btn) {
    var r = btn.getBoundingClientRect();
    var mw = menu.offsetWidth || 270;
    var left = r.left + r.width / 2 - mw / 2;
    left = Math.max(8, Math.min(left, window.innerWidth - mw - 8));
    menu.style.left = left + 'px';
    menu.style.top = (r.bottom + 10) + 'px';
  }
  function closeAllConsultMenus() {
    $$('.consult-menu.open').forEach(function (m) { m.classList.remove('open'); });
  }
  $$('.consult-trigger').forEach(function (btn) {
    var wrap = btn.closest('.consult-cta');
    var menu = wrap && wrap.querySelector('.consult-menu');
    if (!menu) return;
    if (menu.parentNode !== document.body) document.body.appendChild(menu);
    menu._trigger = btn;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = menu.classList.contains('open');
      closeAllConsultMenus();
      if (!isOpen) { placeConsultMenu(menu, btn); menu.classList.add('open'); }
    });
  });
  document.addEventListener('click', function (e) {
    if (e.target.closest('.consult-menu') || e.target.closest('.consult-trigger')) return;
    closeAllConsultMenus();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllConsultMenus();
  });
  // Reposition on resize; close on scroll (simplest correct behavior —
  // avoids the menu drifting away from its trigger as the page moves).
  window.addEventListener('resize', function () {
    $$('.consult-menu.open').forEach(function (m) { if (m._trigger) placeConsultMenu(m, m._trigger); });
  });
  window.addEventListener('scroll', function () {
    closeAllConsultMenus();
  }, { passive: true, capture: true });
})();
