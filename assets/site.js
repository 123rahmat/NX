/* Linqore site script: navigation, hero canvas, reveals, filters, contact form. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  root.classList.add('js');

  // Refuse to run inside someone else's frame (clickjacking guard; Pages cannot send X-Frame-Options).
  if (window.top !== window.self) {
    root.style.display = 'none';
    try { window.top.location = window.self.location.href; } catch (e) { /* cross-origin parent */ }
    return;
  }

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ready(fn) {
    if (doc.readyState !== 'loading') fn(); else doc.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    nav();
    reveal();
    heroCanvas();
    filters();
    form();
    spotlight();
    var y = doc.getElementById('yr');
    if (y) y.textContent = String(new Date().getFullYear());
  });

  /* ---------- Top navigation ---------- */
  function nav() {
    var burger = doc.querySelector('.burger');
    var menu = doc.getElementById('nav');
    if (burger && menu) {
      burger.addEventListener('click', function () {
        var open = root.classList.toggle('menu-open');
        burger.setAttribute('aria-expanded', String(open));
      });
      menu.addEventListener('click', function (e) {
        if (e.target.closest('a')) close();
      });
    }
    function close() {
      root.classList.remove('menu-open');
      if (burger) burger.setAttribute('aria-expanded', 'false');
      doc.querySelectorAll('.dd.open').forEach(function (d) {
        d.classList.remove('open');
        d.querySelector('button').setAttribute('aria-expanded', 'false');
      });
    }
    doc.querySelectorAll('.dd > button').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var dd = btn.parentElement, open = !dd.classList.contains('open');
        dd.classList.toggle('open', open);
        btn.setAttribute('aria-expanded', String(open));
      });
    });
    // Keyboard: close a dropdown once focus leaves it.
    doc.querySelectorAll('.dd').forEach(function (dd) {
      dd.addEventListener('focusout', function (e) {
        if (!dd.contains(e.relatedTarget) && dd.classList.contains('open') && window.innerWidth > 960) {
          dd.classList.remove('open');
          dd.querySelector('button').setAttribute('aria-expanded', 'false');
        }
      });
    });
    doc.addEventListener('click', function (e) {
      if (!e.target.closest('.dd')) doc.querySelectorAll('.dd.open').forEach(function (d) {
        d.classList.remove('open');
        d.querySelector('button').setAttribute('aria-expanded', 'false');
      });
    });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    window.addEventListener('resize', function () { if (window.innerWidth > 960) close(); });
  }

  /* ---------- Reveal on scroll (only for elements that start off-screen) ---------- */
  function reveal() {
    if (reduce || !('IntersectionObserver' in window)) return;
    var els = doc.querySelectorAll('[data-rv]');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    var vh = window.innerHeight;
    els.forEach(function (el, i) {
      if (el.getBoundingClientRect().top < vh) return;
      el.classList.add('rv');
      el.style.transitionDelay = (i % 3) * 80 + 'ms';
      io.observe(el);
    });
  }

  /* ---------- Hero canvas: devices connected in a live network ---------- */
  function heroCanvas() {
    var cv = doc.getElementById('net');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d'), w = 0, h = 0, dpr = 1, nodes = [], packets = [], raf = 0, visible = true, last = 0;

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.round(Math.min(70, Math.max(26, (w * h) / 22000)));
      nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.22, vy: (Math.random() - 0.5) * 0.22,
          r: Math.random() < 0.18 ? 2.6 : 1.5, hub: Math.random() < 0.18
        });
      }
      packets = [];
    }

    var LINK = 150;
    function frame(t) {
      raf = 0;
      var dt = Math.min(48, t - last || 16); last = t;
      ctx.clearRect(0, 0, w, h);
      var i, j, a, b, dx, dy, d;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (!reduce) {
          a.x += a.vx * dt * 0.06; a.y += a.vy * dt * 0.06;
          if (a.x < -20) a.x = w + 20; else if (a.x > w + 20) a.x = -20;
          if (a.y < -20) a.y = h + 20; else if (a.y > h + 20) a.y = -20;
        }
      }
      ctx.lineWidth = 1;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j]; dx = a.x - b.x; dy = a.y - b.y; d = dx * dx + dy * dy;
          if (d < LINK * LINK) {
            var o = 1 - Math.sqrt(d) / LINK;
            ctx.strokeStyle = 'rgba(120,160,240,' + (o * 0.28).toFixed(3) + ')';
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
            if (!reduce && o > 0.45 && packets.length < 18 && Math.random() < 0.0016 * dt) {
              packets.push({ a: a, b: b, p: 0, s: 0.0006 + Math.random() * 0.0008 });
            }
          }
        }
      }
      for (i = packets.length - 1; i >= 0; i--) {
        var k = packets[i]; k.p += k.s * dt;
        if (k.p >= 1) { packets.splice(i, 1); continue; }
        var px = k.a.x + (k.b.x - k.a.x) * k.p, py = k.a.y + (k.b.y - k.a.y) * k.p;
        var g = ctx.createRadialGradient(px, py, 0, px, py, 7);
        g.addColorStop(0, 'rgba(34,211,238,.95)'); g.addColorStop(1, 'rgba(34,211,238,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, 7, 0, 6.283); ctx.fill();
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        ctx.fillStyle = a.hub ? 'rgba(143,180,255,.95)' : 'rgba(143,180,255,.55)';
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill();
        if (a.hub) {
          ctx.strokeStyle = 'rgba(143,180,255,.18)';
          ctx.beginPath(); ctx.arc(a.x, a.y, 7, 0, 6.283); ctx.stroke();
        }
      }
      if (!reduce && visible && !doc.hidden) raf = requestAnimationFrame(frame);
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }

    size();
    start();
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { size(); start(); }, 150); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) start(); }).observe(cv);
    }
    doc.addEventListener('visibilitychange', function () { if (!doc.hidden) start(); });
  }


  /* ---------- Spotlight hover (pointer devices only) ---------- */
  function spotlight() {
    if (!window.matchMedia || !matchMedia('(hover: hover)').matches) return;
    doc.addEventListener('pointermove', function (e) {
      var el = e.target.closest && e.target.closest('.spot');
      if (!el) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }

  /* ---------- Project filters ---------- */
  function filters() {
    var bar = doc.querySelector('.filters');
    if (!bar) return;
    var cards = doc.querySelectorAll('.proj[data-cat]');
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      var cat = btn.getAttribute('data-f');
      cards.forEach(function (c) { c.hidden = cat !== 'all' && c.getAttribute('data-cat') !== cat; });
    });
  }

  /* ---------- Contact form (FormSubmit) ---------- */
  function form() {
    var f = doc.getElementById('quote');
    if (!f) return;
    var endpoint = f.getAttribute('data-endpoint');
    var msg = doc.getElementById('form-msg');
    var btn = f.querySelector('button[type=submit]');
    var params = new URLSearchParams(location.search);
    var pre = params.get('service');
    if (pre) {
      var sel = f.elements.service;
      for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === pre) sel.selectedIndex = i;
    }
    var started = Date.now();

    function show(text, kind) { msg.hidden = false; msg.className = 'msg ' + kind; msg.textContent = text; }

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      msg.hidden = true;
      var el = f.elements, bad = null;
      ['name', 'contact', 'details'].forEach(function (n) {
        var ok = el[n].value.trim().length >= (n === 'details' ? 10 : 2);
        el[n].setAttribute('aria-invalid', String(!ok));
        if (!ok && !bad) bad = el[n];
      });
      if (bad) { show('Please fill in your name, a phone number or email, and a short description.', 'err'); bad.focus(); return; }
      // Bots: filled honeypot or submitted inhumanly fast. Pretend success, send nothing.
      if (el._honey.value || Date.now() - started < 2500) { done(); return; }
      var contact = el.contact.value.trim();
      var data = {
        _subject: 'New enquiry: ' + el.name.value.trim() + (el.service.value ? ' - ' + el.service.value : ''),
        _template: 'table', _captcha: 'false',
        name: el.name.value.trim(), contact: contact, city: el.city.value.trim(),
        service: el.service.value, budget: el.budget.value.trim(), message: el.details.value.trim(), _honey: ''
      };
      if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(contact)) data._replyto = contact;
      btn.disabled = true; btn.textContent = 'Sending...';
      fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data), referrerPolicy: 'strict-origin-when-cross-origin'
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (o) {
          if (!r.ok || o.success === false || o.success === 'false') throw new Error(o.message || 'failed');
          done();
        });
      }).catch(function () {
        btn.disabled = false; btn.textContent = 'Send request';
        show('The message could not be sent. Please try again, or contact us on WhatsApp.', 'err');
      });
    });

    function done() {
      f.innerHTML = '';
      var d = doc.createElement('div'); d.className = 'done';
      d.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m7.5 12.5 3 3 6-6.5"/></svg><h3>Thank you, message received</h3><p>We will reply by WhatsApp, phone or email with a scope, timeline and quotation.</p>';
      f.appendChild(d);
      d.setAttribute('tabindex', '-1'); d.focus();
    }
  }
})();
