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
     measured.  Without this file the rail simply scrolls with the article.

     While it is holding, the card has travel of its own: however much taller
     than the screen it is.  A wheel over the card moves it through that travel
     instead of moving the page, so a reader halfway down an article can bring
     the top of the rail back without losing their place.  At either end the
     page takes the scroll again.  Keyboard focus moves the card the same way,
     so a tabbed-to link is never left off-screen.  No scroll region and no
     second scrollbar: the card is positioned, not scrolled. */
  var card = document.querySelector('.rail');
  if (card) {
    var wide = window.matchMedia('(min-width: 1100px)');
    var gap = 24;
    var travel = 0;
    var offset = null;
    var placing = false;

    var clamp = function (value) {
      return Math.min(travel, Math.max(0, value));
    };
    var apply = function () {
      card.style.position = 'sticky';
      card.style.top = (gap - offset) + 'px';
    };
    var place = function () {
      if (!wide.matches) {
        card.style.position = '';
        card.style.top = '';
        offset = null;
        return;
      }
      travel = Math.max(0, card.offsetHeight + gap * 2 - window.innerHeight);
      offset = offset === null ? travel : clamp(offset);
      apply();
    };
    var schedulePlace = function () {
      if (placing) { return; }
      placing = true;
      window.requestAnimationFrame(function () { placing = false; place(); });
    };
    // Only while the card is actually holding; before that the page scrolls.
    var holding = function () {
      return card.getBoundingClientRect().top <= gap - offset + 1;
    };
    var move = function (delta) {
      var next = clamp(offset + delta);
      if (next === offset) { return false; }
      offset = next;
      apply();
      return true;
    };

    // deltaY is not always pixels: Firefox reports lines, and some setups pages.
    var pixels = function (event) {
      if (event.deltaMode === 1) { return event.deltaY * 16; }
      if (event.deltaMode === 2) { return event.deltaY * window.innerHeight; }
      return event.deltaY;
    };
    card.addEventListener('wheel', function (event) {
      if (!wide.matches || travel <= 0 || event.ctrlKey || !holding()) { return; }
      if (move(pixels(event))) { event.preventDefault(); }
    }, { passive: false });

    card.addEventListener('focusin', function (event) {
      if (!wide.matches || travel <= 0) { return; }
      var box = event.target.getBoundingClientRect();
      if (box.top < gap) { move(box.top - gap); }
      else if (box.bottom > window.innerHeight - gap) { move(box.bottom - window.innerHeight + gap); }
    });

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
