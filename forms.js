/* Form wiring. One handler for every form on the site.

   A form opts in with data-form="<id>" (contact | team-pilot | newsletter).
   Fields need a name attribute; anything without one is not submitted.

   Submissions POST to /api/lead, which forwards them to the webhook set in
   LEAD_WEBHOOK_URL. Until that env var is set the endpoint answers 503 and we
   show the admissions address — a visitor is never told "sent" when it wasn't.
   See FORMS.md.                                                              */
(function () {
  "use strict";
  var FALLBACK_EMAIL = "info@tayanaacademy.com";

  function setStatus(form, kind, msg) {
    var el = form.querySelector(".form-status");
    if (!el) {
      el = document.createElement("p");
      el.className = "form-status";
      el.setAttribute("role", "status");
      el.setAttribute("aria-live", "polite");
      form.appendChild(el);
    }
    el.className = "form-status is-" + kind;
    if (kind === "fallback") {
      el.innerHTML = msg + ' <a href="mailto:' + FALLBACK_EMAIL + '">' +
                     FALLBACK_EMAIL + "</a>.";
    } else {
      el.textContent = msg;
    }
  }

  function submitBtn(form) {
    return form.querySelector('button[type="submit"], button:not([type])');
  }

  function onSubmit(e) {
    e.preventDefault();
    var form = e.currentTarget;
    if (form.dataset.busy === "1") return;

    if (typeof form.reportValidity === "function" && !form.reportValidity()) return;

    var data = { form: form.dataset.form, page: location.pathname };
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.name && typeof el.value === "string") data[el.name] = el.value;
    });

    var btn = submitBtn(form), label = btn ? btn.textContent : "";
    form.dataset.busy = "1";
    if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
    setStatus(form, "pending", "Sending…");

    fetch("/api/lead", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; })
          .then(function (j) { return { ok: r.ok, status: r.status, body: j }; });
      })
      .then(function (r) {
        if (r.ok) {
          setStatus(form, "ok", form.dataset.success ||
            "Thank you — we'll be in touch.");
          form.reset();
          return;
        }
        if (r.status === 503 || r.body.error === "not_configured") {
          setStatus(form, "fallback",
            "This form isn't connected yet. Please email us at");
          return;
        }
        if (r.status === 400 && r.body.error) {
          setStatus(form, "error", r.body.error);
          return;
        }
        setStatus(form, "fallback",
          "Something went wrong sending that. Please email us at");
      })
      .catch(function () {
        setStatus(form, "fallback",
          "We couldn't reach the server. Please email us at");
      })
      .then(function () {
        form.dataset.busy = "0";
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
  }

  function init() {
    var forms = document.querySelectorAll("form[data-form]");
    Array.prototype.forEach.call(forms, function (f) {
      f.removeAttribute("onsubmit");
      f.addEventListener("submit", onSubmit);
    });
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
