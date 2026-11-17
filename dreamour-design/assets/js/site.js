/* Dreamour Design — site interactions (no dependencies) */
(function () {
  'use strict';
  var WA = '919600125599';
  var EMAIL = 'info@design.dreamour.in';
  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- split headings into words for the reveal ---------- */
  $$('.tsplit').forEach(function (el) {
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement('span'); w.className = 'w';
            var i = document.createElement('span'); i.textContent = part;
            w.appendChild(i); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    })(el);
    $$('.w > span', el).forEach(function (s, i) { s.style.transitionDelay = (0.08 * i + 0.15) + 's'; });
  });
  requestAnimationFrame(function () {
    root.classList.add('loaded');
    $$('.tsplit').forEach(function (el) { el.classList.add('in'); });
  });

  /* ---------- header: solid after hero, hides on scroll down ---------- */
  var hdr = $('#hdr'), lastY = 0;
  function headerState(y) {
    var solid = y > 60 || document.body.classList.contains('no-hero');
    hdr.classList.toggle('solid', solid);
    hdr.classList.toggle('hide', y > 500 && y > lastY + 4 && !document.body.classList.contains('locked'));
    if (y < lastY - 4 || y < 500) hdr.classList.remove('hide');
    lastY = y;
  }

  /* ---------- mobile overlay menu ---------- */
  var burger = $('.burger'), ov = $('#overlay');
  function menu(open) {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('locked', open);
    if (open) { ov.hidden = false; requestAnimationFrame(function () { ov.classList.add('open'); }); }
    else { ov.classList.remove('open'); setTimeout(function () { if (!ov.classList.contains('open')) ov.hidden = true; }, 450); }
  }
  burger.addEventListener('click', function () { menu(burger.getAttribute('aria-expanded') !== 'true'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('locked')) menu(false); });

  /* ---------- parallax + scroll-driven effects ---------- */
  var heroMedia = $('[data-hero]');
  var layers = $$('[data-parallax]');
  var fills = $$('.fill-text');
  fills.forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w) { return '<span class="fw">' + w + '</span>'; }).join(' ');
  });

  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY, vh = window.innerHeight;
    headerState(y);
    if (reduced) { fills.forEach(function (el) { $$('.fw', el).forEach(function (w) { w.classList.add('on'); }); }); return; }
    if (heroMedia && y < vh * 1.2) heroMedia.style.transform = 'translate3d(0,' + (y * 0.35).toFixed(1) + 'px,0) scale(' + (1 + y / vh * 0.08).toFixed(4) + ')';
    layers.forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      if (box.bottom < -100 || box.top > vh + 100) return;
      var speed = parseFloat(el.getAttribute('data-parallax')) || 0.2;
      var off = (box.top + box.height / 2 - vh / 2) * -speed;
      el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
    });
    fills.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = Math.min(Math.max((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0), 1);
      var ws = $$('.fw', el), n = Math.round(p * ws.length);
      ws.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  frame();

  /* ---------- reveal on scroll + count-up ---------- */
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in'); io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    $$('.reveal').forEach(function (el, i) { io.observe(el); });

    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, end = +el.getAttribute('data-count'), t0;
        (function step(t) {
          t0 = t0 || t;
          var k = Math.min((t - t0) / 1600, 1);
          el.textContent = Math.round(end * (1 - Math.pow(1 - k, 4)));
          if (k < 1) requestAnimationFrame(step);
        })(performance.now());
      });
    }, { threshold: 0.6 });
    $$('[data-count]').forEach(function (el) { el.textContent = '0'; co.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- services: floating image follows the cursor ---------- */
  var float = $('.svc-float');
  if (float && window.matchMedia('(hover: hover)').matches && !reduced) {
    var img = $('img', float), fx = 0, fy = 0, tx = 0, ty = 0, raf;
    $$('.svc-row').forEach(function (row) {
      row.addEventListener('mouseenter', function () { img.src = row.getAttribute('data-img'); float.classList.add('on'); });
      row.addEventListener('mouseleave', function () { float.classList.remove('on'); });
    });
    document.addEventListener('mousemove', function (e) {
      tx = e.clientX + 180; ty = e.clientY;
      if (!raf) raf = requestAnimationFrame(function loop() {
        fx += (tx - fx) * 0.18; fy += (ty - fy) * 0.18;
        float.style.left = fx + 'px'; float.style.top = fy + 'px';
        raf = Math.abs(tx - fx) + Math.abs(ty - fy) > 0.5 ? requestAnimationFrame(loop) : null;
      });
    });
  }

  /* ---------- works filter ---------- */
  var chips = $$('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-f');
      chips.forEach(function (x) { var on = x === c; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
      $$('.pgrid .pcard').forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-cat') === f;
        card.hidden = !show;
        if (show) { card.classList.remove('in'); requestAnimationFrame(function () { card.classList.add('in'); }); }
      });
    });
  });

  /* ---------- services sub-nav highlight ---------- */
  var subLinks = $$('.subnav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) subLinks.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    $$('.svc-block').forEach(function (b) { so.observe(b); });
  }

  /* ---------- lightbox ---------- */
  var lb = $('.lb');
  if (lb && typeof lb.showModal === 'function') {
    var items = $$('[data-lb]'), cur = 0, lbImg = $('img', lb), cap = $('figcaption', lb);
    function show(i) {
      cur = (i + items.length) % items.length;
      var a = items[cur];
      lbImg.src = a.getAttribute('href');
      lbImg.alt = a.getAttribute('data-cap');
      cap.textContent = a.getAttribute('data-cap') + '  ·  ' + (cur + 1) + ' / ' + items.length;
    }
    items.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); show(i); lb.showModal(); });
    });
    var single = items.length < 2;
    $('.lb-prev', lb).hidden = single; $('.lb-next', lb).hidden = single;
    $('.lb-prev', lb).addEventListener('click', function () { show(cur - 1); });
    $('.lb-next', lb).addEventListener('click', function () { show(cur + 1); });
    $('.lb-x', lb).addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
      sx = null;
    });
  }

  /* ---------- forms: send by WhatsApp or email ---------- */
  function collect(form) {
    var lines = [], idx = {};
    new FormData(form).forEach(function (v, k) {
      v = String(v).trim(); if (!v) return;
      if (k in idx) { lines[idx[k]] += ', ' + v; return; }
      idx[k] = lines.length; lines.push(k + ': ' + v);
    });
    return lines;
  }
  function checkFields(scope, names) {
    var bad = [];
    names.forEach(function (n) {
      var group = $$('[name="' + n + '"]', scope);
      if (!group.length) return;
      if (group[0].type === 'radio' || group[0].type === 'checkbox') {
        var ok = group.some(function (g) { return g.checked; });
        var box = group[0].closest('.opts');
        if (box) box.classList.toggle('bad', !ok);
        if (!ok) bad.push(group[0]);
      } else {
        var el = group[0];
        var ok2 = el.value.trim().length > 1 && (el.type !== 'email' || el.checkValidity());
        el.classList.toggle('bad', !ok2);
        if (!ok2) bad.push(el);
      }
    });
    return bad;
  }
  function send(form, via) {
    var subject = form.getAttribute('data-subject');
    var text = subject + '\n\n' + collect(form).join('\n');
    var note = $('.f-note', form);
    if (via === 'email') {
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text);
      note.textContent = 'Your email app should open with everything filled in. Just press send.';
    } else {
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
      note.textContent = 'WhatsApp should open with your message ready. Just press send.';
    }
    note.className = 'f-note ok';
  }

  var cf = $('#contact-form');
  if (cf) cf.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = checkFields(cf, ['Name', 'Phone', 'Message']);
    var em = cf.elements.Email;
    if (em.value && !em.checkValidity()) { em.classList.add('bad'); bad.push(em); } else em.classList.remove('bad');
    var note = $('.f-note', cf);
    if (bad.length) { note.textContent = 'Please fill in the highlighted fields.'; note.className = 'f-note err'; bad[0].focus(); return; }
    send(cf, (e.submitter && e.submitter.value) || 'whatsapp');
  });

  var wz = $('#builder-form');
  if (wz) {
    var steps = $$('.step', wz), at = 0, bar = $('.w-progress i', wz), note = $('.f-note', wz);
    var range = $('input[type=range]', wz), out = $('output', wz);
    if (range) range.addEventListener('input', function () { out.textContent = range.value; });
    function go(i) {
      at = Math.max(0, Math.min(i, steps.length - 1));
      steps.forEach(function (s, k) { s.classList.toggle('cur', k === at); });
      wz.classList.toggle('first', at === 0);
      wz.classList.toggle('last', at === steps.length - 1);
      bar.style.width = ((at + 1) / steps.length * 100) + '%';
      note.textContent = ''; note.className = 'f-note';
    }
    function stepOk(i) {
      var need = (steps[i].getAttribute('data-need') || '').split(',').filter(Boolean);
      var bad = checkFields(steps[i], need);
      if (bad.length) {
        note.textContent = 'Please complete this step to continue.'; note.className = 'f-note err';
        bad[0].focus(); return false;
      }
      return true;
    }
    $('.w-next', wz).addEventListener('click', function () {
      if (stepOk(at)) { go(at + 1); wz.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }); var f = $('input,textarea', steps[at]); if (f && f.type !== 'radio' && f.type !== 'checkbox') f.focus({ preventScroll: true }); }
    });
    $('.w-back', wz).addEventListener('click', function () { go(at - 1); });
    wz.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT' && !wz.classList.contains('last')) { e.preventDefault(); $('.w-next', wz).click(); }
    });
    wz.addEventListener('submit', function (e) {
      e.preventDefault();
      for (var i = 0; i < steps.length; i++) { if (!stepOk(i)) { go(i); stepOk(i); return; } }
      send(wz, (e.submitter && e.submitter.value) || 'whatsapp');
    });
    go(0);
  }
})();
