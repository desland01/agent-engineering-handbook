/* Agent Engineering Handbook — progressive enhancement only.
   Every control works without this file: the header menu and the
   "On this page" disclosure are native <details>, the section list is plain
   anchors, and the horizontal rows are native scroll regions you can swipe,
   drag or arrow-key through.  This script adds conveniences on top:
     1. the header menu closes on Escape (focus returns to its button) and on
        a click or tap outside it;
     2. the reader's rail marks the section currently on screen;
     3. horizontal rows get previous/next buttons and a position counter.
   The rail's own scrolling is CSS: a sticky box with overflow and
   `overscroll-behavior: contain`.  Nothing here intercepts the wheel.
   Copied verbatim to public/assets/ by build/render.py. */
(function () {
  'use strict';

  var list = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');

  // ---------------------------------------------------------- header menu
  function headerMenu() {
    var menus = list('details.menu');
    if (!menus.length) { return; }
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

  // ------------------------------------------------------------- the rail
  function railCurrentSection() {
    var rail = document.querySelector('.rail .toc');
    if (!rail) { return; }
    var targets = list('a[href^="#"]', rail).map(function (link) {
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
    onScroll(update);
  }

  // --------------------------------------------------- horizontal rows
  /* The row itself is a native scroll region and needs nothing from here.
     What this adds is the pair of buttons and the counter, built in script so
     that a reader without JavaScript is never shown a control that cannot
     work.  The counter counts the first card whose left edge is at or past the
     region's own left edge, and `next` is disabled once the region is scrolled
     as far as it goes — without that the count sticks short of the total while
     the button still looks live. */
  function rows() {
    list('[data-row]').forEach(function (region) {
      var track = region.firstElementChild;
      if (!track || track.children.length < 2) { return; }
      var cards = Array.prototype.slice.call(track.children);

      var controls = document.createElement('div');
      controls.className = 'row-controls';
      var prev = document.createElement('button');
      var next = document.createElement('button');
      prev.type = next.type = 'button';
      prev.innerHTML = '<span aria-hidden="true">&#8592;</span>';
      next.innerHTML = '<span aria-hidden="true">&#8594;</span>';
      prev.setAttribute('aria-label', 'Scroll back');
      next.setAttribute('aria-label', 'Scroll forward');
      var count = document.createElement('p');
      count.className = 'count';
      count.setAttribute('aria-live', 'polite');
      controls.appendChild(prev);
      controls.appendChild(next);
      controls.appendChild(count);
      region.parentNode.insertBefore(controls, region.nextSibling);

      var label = region.getAttribute('data-row') || 'of';
      function atEnd() {
        return Math.ceil(region.scrollLeft) >= region.scrollWidth - region.clientWidth - 1;
      }
      function firstVisible() {
        var edge = region.getBoundingClientRect().left;
        for (var i = 0; i < cards.length; i++) {
          if (cards[i].getBoundingClientRect().right > edge + 4) { return i; }
        }
        return cards.length - 1;
      }
      function update() {
        // At the far end the last card is the one in view, whatever the maths
        // says: a final card narrower than the region never reaches the edge.
        var n = atEnd() ? cards.length : firstVisible() + 1;
        count.innerHTML = '<b>' + (n < 10 ? '0' + n : n) + '</b> ' + label + ' ' + cards.length;
        prev.disabled = region.scrollLeft <= 1;
        next.disabled = atEnd();
      }
      function step(dir) {
        var card = cards[0].getBoundingClientRect();
        var gap = cards.length > 1 ? cards[1].getBoundingClientRect().left - card.right : 1;
        region.scrollBy({ left: dir * (card.width + gap), behavior: reduced && reduced.matches ? 'auto' : 'smooth' });
      }
      prev.addEventListener('click', function () { step(-1); });
      next.addEventListener('click', function () { step(1); });
      region.addEventListener('scroll', function () { schedule(update); }, { passive: true });
      window.addEventListener('resize', function () { schedule(update); });
      update();
    });
  }

  // ------------------------------------------------------------- plumbing
  var frames = [];
  function schedule(fn) {
    if (frames.indexOf(fn) !== -1) { return; }
    frames.push(fn);
    window.requestAnimationFrame(function () {
      frames.splice(frames.indexOf(fn), 1);
      fn();
    });
  }
  function onScroll(fn) {
    window.addEventListener('scroll', function () { schedule(fn); }, { passive: true });
    window.addEventListener('resize', function () { schedule(fn); });
    fn();
  }

  // ------------------------------------------------- the overflow fades
  /* A region only fades at an edge it can actually scroll past, and the fade
     lifts once the reader reaches the end, so the page never implies there is
     more to see when there is not. Without this script the regions simply do
     not fade, which costs nothing: they still scroll. */
  function overflowFades() {
    var regions = list('.rail, .ideas-row, .track-row');
    if (!regions.length) { return; }
    function update() {
      regions.forEach(function (el) {
        var vertical = el.classList.contains('rail');
        var size = vertical ? el.scrollHeight - el.clientHeight : el.scrollWidth - el.clientWidth;
        var at = vertical ? el.scrollTop : el.scrollLeft;
        el.classList.toggle('is-overflowing', size > 2);
        el.classList.toggle('is-at-end', size > 2 && Math.ceil(at) >= size - 1);
      });
    }
    regions.forEach(function (el) {
      el.addEventListener('scroll', function () { schedule(update); }, { passive: true });
    });
    onScroll(update);
  }

  // ----------------------------------------------------------- reveals
  /* Fade-and-rise on entering the viewport, once, siblings staggered. Anything
     already on screen when this runs is shown immediately so the first
     screen never flashes; under reduced motion nothing is touched. */
  // A card inside a horizontal row can sit off screen sideways for ever, so a
  // vertical observer would never reveal it; the row reveals as one unit and
  // its cards are excluded.
  var REVEAL = '.band-head, .section-head, .tiles > li, .ideas:not(.track) > li, .shelves > li, .study, .tier, ' +
               '.hub-next, .pick li, .gallery .frame, .guide-seq, .study .findings > li, .ledger li, ' +
               '.ideas-row, .track-row';
  function reveals() {
    if ((reduced && reduced.matches) || !('IntersectionObserver' in window)) { return; }
    var pending = list(REVEAL).filter(function (el) {
      return el.getBoundingClientRect().top >= window.innerHeight;
    });
    pending.forEach(function (el) { el.classList.add('reveal-pending'); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        var el = entry.target;
        var siblings = pending.filter(function (o) { return o.parentNode === el.parentNode; });
        var i = siblings.indexOf(el);
        el.style.transitionDelay = Math.min(i < 0 ? 0 : i, 7) * 60 + 'ms';
        el.classList.add('reveal-in');
        el.classList.remove('reveal-pending');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    pending.forEach(function (el) { io.observe(el); });
  }

  headerMenu();
  railCurrentSection();
  rows();
  overflowFades();
  reveals();
})();
