(function () {
  var header = document.querySelector('.site-header');
  var btn = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');

  // Sticky header border once scrolled
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  function setMenu(open) {
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  // Project filters
  var chips = document.querySelectorAll('.chip');
  var tiles = document.querySelectorAll('.tile');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.dataset.filter;
      chips.forEach(function (c) {
        var on = c === chip;
        c.classList.toggle('is-active', on);
        c.setAttribute('aria-pressed', String(on));
      });
      tiles.forEach(function (t) { t.hidden = !(f === 'all' || t.dataset.cat === f); });
    });
  });

  // Reveal on scroll
  var revealEls = document.querySelectorAll('.section-head, .service, .tile, .steps li, .why-list li, .faq details, .big-quote');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }

  // Enquiry form -> opens the visitor's email app with details filled in
  var form = document.getElementById('enquiry');
  var note = form.querySelector('.form-note');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var bad = [];
    ['name', 'phone'].forEach(function (k) {
      var el = form.elements[k];
      var ok = String(d.get(k) || '').trim().length > 1;
      el.classList.toggle('invalid', !ok);
      if (!ok) bad.push(el);
    });
    var email = form.elements.email;
    var emailOk = !email.value || email.checkValidity();
    email.classList.toggle('invalid', !emailOk);
    if (!emailOk) bad.push(email);
    if (bad.length) {
      note.textContent = 'Please add your name and phone number' + (emailOk ? '.' : ', and check your email address.');
      note.className = 'form-note error';
      bad[0].focus();
      return;
    }
    var subject = 'Interior enquiry — ' + d.get('type') + ' (' + d.get('name') + ')';
    var body = [
      'Name: ' + d.get('name'),
      'Phone: ' + d.get('phone'),
      'Email: ' + (d.get('email') || '-'),
      'Project type: ' + d.get('type'),
      'Property: ' + d.get('property'),
      '',
      String(d.get('message') || '')
    ].join('\n');
    window.location.href = 'mailto:' + form.dataset.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    note.textContent = 'Thanks! Your email app should open now — just press send.';
    note.className = 'form-note ok';
  });

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
