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
  // The hero loop is SMIL, which CSS cannot stop: pause it when motion is reduced.
  if (reduced && reduced.matches) {
    Array.prototype.forEach.call(document.querySelectorAll('.hero-loop, .desks-loop'), function (svg) {
      if (svg.pauseAnimations) { svg.pauseAnimations(); svg.setCurrentTime(2.5); }
    });
  }

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
    var regions = list('.rail, .ideas-row, .track-row, .desks-row');
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
  // The home page's skill lanes, guide directory rows and report file cards
  // reveal one by one like the tiles they replaced; the scroll-driven marks
  // and wire inside them are CSS and need nothing from here.
  var REVEAL = '.band-head, .section-head, .tiles > li, .ideas:not(.track) > li, .shelves > li, .study, .tier, ' +
               '.hub-next, .pick li, .gallery .frame, .guide-seq, .study .findings > li, .ledger li, ' +
               '.lanes > li, .directory > li, .files > li, ' +
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

  // ------------------------------------------------------------ prompt
  /* Types the four skills as slash commands, one after another. Static text
     is already in the markup, so without this the prompt simply shows the
     first; under reduced motion it stays that way. Pauses while the tab is
     hidden so it never runs unwatched. */
  function prompt() {
    var el = document.querySelector('.prompt .typed');
    if (!el || (reduced && reduced.matches)) { return; }
    var lines = (el.getAttribute('data-lines') || '').split('|').filter(Boolean);
    if (lines.length < 2) { return; }
    var i = 0, text = lines[0], deleting = false;
    function tick() {
      if (document.hidden) { setTimeout(tick, 600); return; }
      var target = lines[i];
      var wait;
      if (!deleting) {
        text = target.slice(0, text.length + 1);
        wait = text === target ? 1700 : 42 + Math.random() * 40;
        if (text === target) { deleting = true; }
      } else {
        text = text.slice(0, -1);
        wait = 22;
        if (text === '/') { deleting = false; i = (i + 1) % lines.length; wait = 260; }
      }
      el.textContent = text;
      setTimeout(tick, wait);
    }
    setTimeout(tick, 1400);
  }

  // Analytics is independent of the reading enhancements and initializes once.
  function analytics() {
    if (window.__handbookAnalyticsInitialized) return;
    window.__handbookAnalyticsInitialized = true;
    var settings = {};
    try { settings = JSON.parse(document.getElementById('handbook-analytics-config').textContent); } catch (_) {}
    var key = 'handbook.analytics.v1';
    var lifetime = 180 * 24 * 60 * 60 * 1000;
    var choice = null;
    var started = false;
    var panel = document.querySelector('[data-analytics-panel]');
    var prefs = document.querySelector('[data-analytics-preferences]');
    var allow = document.querySelector('[data-analytics-choice="allow"]');
    var decline = document.querySelector('[data-analytics-choice="decline"]');
    var status = document.querySelector('[data-analytics-status]');
    if (!panel || !prefs || !allow || !decline || !status) return;
    var configured = settings.productionHostname === 'agent-engineering-handbook.dev' &&
      typeof settings.gtmId === 'string' && /^GTM-[A-Z0-9]+$/.test(settings.gtmId);
    function gpc() { return navigator.globalPrivacyControl === true; }
    function eligible() {
      return configured && window.location.hostname === settings.productionHostname &&
        window.location.protocol === 'https:' && !gpc();
    }
    try {
      var record = JSON.parse(localStorage.getItem(key));
      var now = Date.now();
      if (record && (record.choice === 'allow' || record.choice === 'decline') &&
          typeof record.decidedAt === 'number' && Number.isFinite(record.decidedAt) &&
          record.decidedAt <= now && now - record.decidedAt < lifetime) choice = record.choice;
    } catch (_) {}
    if (gpc()) choice = 'decline';
    function message() {
      if (gpc()) return 'Analytics is off because Global Privacy Control is enabled.';
      if (!configured) return 'Analytics is not configured and stays off.';
      if (!eligible()) return 'Analytics stays off outside the production website.';
      if (choice === 'decline') return 'Analytics is off. You have declined.';
      if (choice === 'allow') return 'You have allowed analytics.';
      return 'Analytics stays off unless you allow it.';
    }
    function open(focus) {
      status.textContent = message();
      panel.hidden = false;
      prefs.hidden = true; // one control for opening, only when the interface is closed
      if (focus) document.getElementById('analytics-heading').focus();
    }
    function close() { panel.hidden = true; prefs.hidden = false; }
    function consent(value) {
      window.dataLayer = window.dataLayer || [];
      // GTM consumes the standard consent command; no request is sent by this push.
      function command() { window.dataLayer.push(arguments); }
      command('consent', 'update', { analytics_storage: value, ad_storage: 'denied',
        ad_user_data: 'denied', ad_personalization: 'denied' });
    }
    function bootstrap() {
      if (started || choice !== 'allow' || !eligible()) return;
      started = true;
      window.dataLayer = window.dataLayer || [];
      var referrer = '';
      try {
        var ref = new URL(document.referrer);
        if (ref.protocol === 'http:' || ref.protocol === 'https:') referrer = ref.origin;
      } catch (_) {}
      window.dataLayer.push({ page_location: 'https://' + settings.productionHostname + window.location.pathname,
        page_referrer: referrer });
      consent('granted');
      window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(settings.gtmId);
      script.onerror = function () { status.textContent = 'Analytics could not load. Reading and preferences still work.'; };
      document.head.appendChild(script);
    }
    function clearCookies() {
      var names = document.cookie.split(';').map(function (part) { return part.trim().split('=')[0]; })
        .filter(function (name) { return /^(?:_ga(?:_|$)|_gid$|_gat(?:_|$)|_gac_|_gcl_)/.test(name); });
      var host = window.location.hostname.split('.');
      var domains = [''];
      for (var i = 0; i < host.length - 1; i++) {
        domains.push(host.slice(i).join('.')); domains.push('.' + host.slice(i).join('.'));
      }
      var segments = window.location.pathname.split('/');
      var paths = ['/'];
      for (var j = 1; j < segments.length; j++) {
        var path = segments.slice(0, j + 1).join('/');
        paths.push(path); paths.push(path + '/');
      }
      names.forEach(function (name) { domains.forEach(function (domain) { paths.forEach(function (path) {
        document.cookie = name + '=; Max-Age=0; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=' + path +
          (domain ? '; domain=' + domain : '');
      }); }); });
    }
    function decide(value) {
      choice = value;
      try { localStorage.setItem(key, JSON.stringify({ choice: value, decidedAt: Date.now() })); } catch (_) {}
      if (value === 'decline') {
        if (started) consent('denied');
        clearCookies();
        close();
        if (started) window.location.reload();
      } else { bootstrap(); close(); }
      prefs.focus();
    }
    allow.disabled = !eligible();
    allow.addEventListener('click', function () { decide('allow'); });
    decline.addEventListener('click', function () { decide('decline'); });
    prefs.addEventListener('click', function () { open(true); });
    if (choice === null && eligible()) open(false); else close();
    bootstrap();
    // A preference withdrawn in another tab also unloads this page's container.
    window.addEventListener('storage', function (event) {
      if (event.key === key && started) {
        var saved = null;
        try { saved = JSON.parse(event.newValue); } catch (_) {}
        if (!saved || saved.choice !== 'allow') { consent('denied'); clearCookies(); window.location.reload(); }
      }
    });
  }

  analytics();
  headerMenu();
  railCurrentSection();
  rows();
  overflowFades();
  reveals();
  prompt();
})();
