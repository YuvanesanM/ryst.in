(function () {
  var WA = '919600125599';
  var EMAIL = 'info@design.dreamour.in';

  // Header shadow once scrolled
  var header = document.querySelector('.site-header');
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');
  function setMenu(open) {
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  // Footer year
  document.querySelectorAll('.year').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Works filter
  var chips = document.querySelectorAll('.chip');
  var works = document.querySelectorAll('.work');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.dataset.filter;
      chips.forEach(function (c) {
        var on = c === chip;
        c.classList.toggle('is-active', on);
        c.setAttribute('aria-pressed', String(on));
      });
      works.forEach(function (w) { w.hidden = !(f === 'all' || w.dataset.cat === f); });
    });
  });

  // Lightbox
  var lb = document.querySelector('.lightbox');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.lb-cap');
    document.querySelectorAll('.work-img').forEach(function (b) {
      b.addEventListener('click', function () {
        lbImg.src = b.dataset.full;
        lbImg.alt = b.dataset.caption;
        lbCap.textContent = b.dataset.caption;
        lb.showModal();
      });
    });
    lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
  }

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Count-up stats + reveal on scroll
  if ('IntersectionObserver' in window && !reduced) {
    var counters = document.querySelectorAll('.num[data-count]');
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = +el.dataset.count, t0 = null;
        cio.unobserve(el);
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 1400, 1);
          el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = '0';
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });

    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rio.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.section-head, .svc, .svc-row, .feature, .work, .venture, .c-card, .split > *, .two-col > *')
      .forEach(function (el) { el.classList.add('reveal'); rio.observe(el); });
  }

  // Function vs aesthetics slider
  var range = document.querySelector('input[type=range][name=Balance]');
  if (range) {
    var out = document.getElementById('balance-val');
    range.addEventListener('input', function () { out.textContent = range.value; });
  }

  // Forms -> WhatsApp or email, nothing stored on a server
  function wire(form, subject, check) {
    if (!form) return;
    var note = form.querySelector('.form-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var via = (e.submitter && e.submitter.value) || 'whatsapp';
      var problems = check(form);
      if (problems.length) {
        note.textContent = 'Please complete: ' + problems.map(function (p) { return p.label; }).join(', ') + '.';
        note.className = 'form-note error';
        problems[0].el.focus();
        return;
      }
      var lines = [], seen = {};
      new FormData(form).forEach(function (v, k) {
        v = String(v).trim();
        if (!v) return;
        if (seen[k] !== undefined) { lines[seen[k]] += ', ' + v; return; }
        seen[k] = lines.length;
        lines.push(k + ': ' + v);
      });
      var text = subject + '\n\n' + lines.join('\n');
      if (via === 'email') {
        window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text);
        note.textContent = 'Your email app should open with everything filled in. Just press send.';
      } else {
        window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
        note.textContent = 'WhatsApp should open with your message ready. Just press send.';
      }
      note.className = 'form-note ok';
    });
  }

  function req(form, names) {
    var bad = [];
    names.forEach(function (n) {
      var el = form.elements[n[0]];
      var ok = el.value.trim().length > 1 && (el.type !== 'email' || el.checkValidity());
      el.classList.toggle('invalid', !ok);
      if (!ok) bad.push({ el: el, label: n[1] });
    });
    return bad;
  }

  wire(document.getElementById('contact-form'), 'Enquiry from design.dreamour.in', function (f) {
    var bad = req(f, [['Name', 'name'], ['Phone', 'phone'], ['Message', 'message']]);
    var em = f.elements.Email;
    if (em.value && !em.checkValidity()) { em.classList.add('invalid'); bad.push({ el: em, label: 'a valid email' }); }
    else em.classList.remove('invalid');
    return bad;
  });

  wire(document.getElementById('builder-form'), 'Dream Builder questionnaire', function (f) {
    var bad = req(f, [['Name', 'name'], ['Phone', 'phone'], ['Email', 'email']]);
    [['Building', 'what you are building'], ['Requirement', 'design requirement'], ['Style', 'style'], ['Shape', 'shape']].forEach(function (g) {
      var inputs = f.querySelectorAll('[name="' + g[0] + '"]');
      var any = Array.prototype.some.call(inputs, function (i) { return i.checked; });
      var fs = inputs[0].closest('fieldset');
      fs.classList.toggle('invalid', !any);
      if (!any) bad.push({ el: inputs[0], label: g[1] });
    });
    return bad;
  });
})();
