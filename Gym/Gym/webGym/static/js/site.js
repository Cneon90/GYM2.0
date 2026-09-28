/* ============================================================
   GYM 2.0 — интерактив: меню, шапка при прокрутке,
   reveal-анимации, табы, слайдеры, JS-счётчики
   ============================================================ */
(function () {
  'use strict';

  /* Шапка — появление при скролле */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScrollHeader = function () {
      header.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScrollHeader, { passive: true });
    onScrollHeader();
  }

  /* Мобильное меню */
  var burger = document.querySelector('.burger');
  var mobile = document.querySelector('.mobile-nav');
  var closeNav = document.querySelector('.close-nav');
  var openMobile = function () { if (mobile) mobile.style.display = 'block'; };
  var closeMob = function () { if (mobile) mobile.style.display = 'none'; };
  if (burger) burger.addEventListener('click', openMobile);
  if (closeNav) closeNav.addEventListener('click', closeMob);
  if (mobile) {
    mobile.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeMob();
    });
  }

  /* Reveal-анимации при появлении в зоне видимости */
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window) {
    var revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { revealObs.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('visible'); });
  }

  /* Табы (направления / тарифы) */
  var tabButtons = document.querySelectorAll('.tabs button');
  tabButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = btn.closest('.tabs');
      var target = document.getElementById(btn.dataset.tab);
      if (!wrap || !target) return;
      (wrap.querySelectorAll('button')).forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var pages = wrap.parentElement.querySelectorAll('.pane');
      pages.forEach(function (p) { p.classList.remove('active'); });
      target.classList.add('active');
    });
  });

  /* Плавная прокрутка к якорям */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length > 1) {
        var t = document.getElementById(id.substring(1));
        if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
      }
    });
  });
})();