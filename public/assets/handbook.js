/* Agent Engineering Handbook — progressive enhancement only.
   Every control works without this file: the header menu and the
   "On this page" disclosure are native <details>, and the section list is
   plain anchors.  This script adds three conveniences:
     1. the header menu closes on Escape (focus returns to its button) and on
        a click or tap outside it;
     2. the reader's rail holds like a card once its bottom reaches the foot of
        the screen;
     3. the reader's rail marks the section currently on screen.
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

  /* The rail is taller than the viewport on every reader page.  Let it travel
     with the article, then hold once its bottom reaches the foot of the screen,
     so its lower blocks come into view rather than being stranded.  CSS alone
     cannot do this: a bottom-anchored sticky element taller than the viewport
     never engages, and a top-anchored one pins the wrong edge.  So the offset is
     measured.  Without this file the rail simply scrolls with the article. */
  var card = document.querySelector('.rail');
  if (card) {
    var wide = window.matchMedia('(min-width: 1100px)');
    var gap = 24;
    var placing = false;
    var place = function () {
      if (!wide.matches) {
        card.style.position = '';
        card.style.top = '';
        return;
      }
      card.style.position = 'sticky';
      var over = card.offsetHeight + gap * 2 - window.innerHeight;
      card.style.top = (over > 0 ? gap - over : gap) + 'px';
    };
    var schedulePlace = function () {
      if (placing) { return; }
      placing = true;
      window.requestAnimationFrame(function () { placing = false; place(); });
    };
    window.addEventListener('resize', schedulePlace);
    window.addEventListener('load', schedulePlace);
    if (wide.addEventListener) { wide.addEventListener('change', schedulePlace); }
    place();
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
