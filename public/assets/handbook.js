/* Agent Engineering Handbook — progressive enhancement only.
   Every control works without this file: the header menu and the
   "On this page" disclosure are native <details>, and the section list is
   plain anchors.  This script adds two conveniences:
     1. the header menu closes on Escape (focus returns to its button) and on
        a click or tap outside it;
     2. the reader's rail marks the section currently on screen.
   Copied verbatim to public/assets/ by build/render.py. */
(function () {
  'use strict';

  var menus = Array.prototype.slice.call(document.querySelectorAll('details.menu'));
  if (menus.length) {
    document.addEventListener('click', function (event) {
      menus.forEach(function (menu) {
        if (menu.open && !menu.contains(event.target)) { menu.open = false; }
      });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') { return; }
      menus.forEach(function (menu) {
        if (menu.open) {
          menu.open = false;
          var summary = menu.querySelector('summary');
          if (summary) { summary.focus(); }
        }
      });
    });
  }

  var rail = document.querySelector('.rail .toc');
  if (!rail) { return; }
  var links = Array.prototype.slice.call(rail.querySelectorAll('a[href^="#"]'));
  var targets = links.map(function (link) {
    var id = decodeURIComponent(link.getAttribute('href').slice(1));
    return { link: link, el: document.getElementById(id) };
  }).filter(function (t) { return t.el; });
  if (!targets.length) { return; }

  var current = null;
  function update() {
    var threshold = 96;
    var active = targets[0];
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].el.getBoundingClientRect().top <= threshold) { active = targets[i]; }
    }
    // At the very bottom, the last section is the one being read.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      active = targets[targets.length - 1];
    }
    if (active === current) { return; }
    if (current) { current.link.removeAttribute('aria-current'); }
    active.link.setAttribute('aria-current', 'true');
    current = active;
  }
  var pending = false;
  function schedule() {
    if (pending) { return; }
    pending = true;
    window.requestAnimationFrame(function () { pending = false; update(); });
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  update();
})();
