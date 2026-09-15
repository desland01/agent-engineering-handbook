/*
 * Rendered check (T4): scrollbars and horizontal overflow.
 * Pure Node + puppeteer; serves public/ itself on an ephemeral port.
 * Optional: run via build/check.sh after `cd build && npm install`.
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..', 'public');
const PORT = 0; // ephemeral

const PAGES = [
  'index.html',
  'lessons.html',
  'lessons/resume-work.html',
  'skills.html',
  'investigations.html',
  'evidence.html',
  'lessons/recurring-mistakes.html',
  'lessons/better-environments.html',
  'examples/recurring-rule/README.html',
  'skills/agent-feedback-engineering/index.html',
  'skills/agent-artifact-recovery/index.html',
];

const VIEWPORTS = [{ width: 390, height: 844 }, { width: 1440, height: 900 }];

const HUBS = ['lessons.html', 'skills.html', 'investigations.html', 'evidence.html'];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.json': 'application/json',
  '.md': 'text/plain; charset=utf-8',
  '.yml': 'text/plain; charset=utf-8',
};

function serve(root) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      const redirect = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'vercel.json'), 'utf8')).redirects.find(row => row.source === urlPath);
      if (redirect) { res.writeHead(308, {Location: redirect.destination}); return res.end(); }
      let filePath = path.normalize(path.join(root, urlPath));
      if (filePath !== root && !filePath.startsWith(root + path.sep)) {
        res.writeHead(403);
        return res.end('forbidden');
      }
      fs.stat(filePath, (err, st) => {
        if (!err && st.isDirectory()) filePath = path.join(filePath, 'index.html');
        fs.readFile(filePath, (err2, data) => {
          if (err2) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            return res.end('not found: ' + urlPath);
          }
          const ext = path.extname(filePath).toLowerCase();
          res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
          res.end(data);
        });
      });
    });
    server.on('error', reject);
    server.listen(PORT, '127.0.0.1', () => resolve(server));
  });
}

// Runs in the page: returns overflow/scrollbar findings for one document.
function inspectPage() {
  const problems = [];
  const reports = document.querySelector('#reports');
  if (reports) {
    // A navigation class once hid the leading report on mobile. Test the
    // reader's three destinations, independently of their layout classes.
    for (const href of ['github-inspection.html', 'matt-pocock-inspection.html', 'boris-cherny-inspection.html']) {
      const link = reports.querySelector('a[href="' + href + '"]');
      const box = link && link.getBoundingClientRect();
      if (!box || box.width === 0 || box.height === 0) {
        problems.push('investigation destination hidden or missing — ' + href);
      }
    }
  }
  const doc = document.documentElement;
  if (doc.scrollWidth > window.innerWidth) {
    problems.push(
      'horizontal overflow — documentElement.scrollWidth ' +
        doc.scrollWidth + ' > innerWidth ' + window.innerWidth
    );
  }
  const all = document.querySelectorAll('*');
  for (const el of all) {
    const cs = getComputedStyle(el);
    const ox = cs.overflowX;
    const oy = cs.overflowY;
    const scrollsX = (ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth;
    const scrollsY = (oy === 'auto' || oy === 'scroll') && el.scrollHeight > el.clientHeight;
    if (!scrollsX && !scrollsY) continue;
    if (cs.scrollbarWidth && cs.scrollbarWidth !== 'none') {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() +
          (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
          '> computed scrollbar-width: ' + cs.scrollbarWidth
      );
    }
    const bs = cs.borderLeftWidth || '0';
    const be = cs.borderRightWidth || '0';
    const bt = cs.borderTopWidth || '0';
    const bb = cs.borderBottomWidth || '0';
    const borderX = (parseFloat(bs) || 0) + (parseFloat(be) || 0);
    const borderY = (parseFloat(bt) || 0) + (parseFloat(bb) || 0);
    if (scrollsX && el.offsetWidth - el.clientWidth - borderX !== 0) {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() + '> takes ' +
          (el.offsetWidth - el.clientWidth - borderX) + 'px horizontal gutter'
      );
    }
    if (scrollsY && el.offsetHeight - el.clientHeight - borderY !== 0) {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() + '> takes ' +
          (el.offsetHeight - el.clientHeight - borderY) + 'px vertical gutter'
      );
    }
  }
  return problems;
}

// Runs in the page: counts links inside .hub-next.
function countHubNext() {
  const el = document.querySelector('.hub-next');
  if (!el) return { present: false, links: 0 };
  return { present: true, links: el.querySelectorAll('a[href]').length };
}

async function checkLessonJourney(browser, base, failures) {
  const page = await browser.newPage();
  let checks = 0;
  const verify = (pass, detail) => { checks++; if (!pass) failures.push('lesson journey — ' + detail); };
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  try {
    await page.setViewport({width: 390, height: 850});
    await page.goto(base + '/', {waitUntil: 'networkidle0'});
    verify(await page.evaluate(() => {
      const copy = document.querySelector('.opening-copy');
      const pick = document.querySelector('.opening .pick');
      const hero = document.querySelector('.opening .hero-figure');
      return copy && pick && hero && !!(copy.compareDocumentPosition(pick) & 4) && !!(pick.compareDocumentPosition(hero) & 4);
    }), 'homepage reading order is not copy, problems, artwork');
    await Promise.all([page.waitForNavigation({waitUntil: 'domcontentloaded'}), page.click('.actions .primary')]);
    verify(page.url().endsWith('/lessons/recurring-mistakes.html'), 'primary action does not open lesson 1');
    verify(await page.$eval('h1', (el) => el.textContent === 'You turn repeated mistakes into reliable checks'), 'lesson 1 title differs');
    const tabLimit = await page.$$eval('.site-head a, .site-head summary', (els) => els.length + 2);
    let menuFocused = false;
    for (let i = 0; i < tabLimit; i++) {
      await page.keyboard.press('Tab');
      menuFocused = await page.evaluate(() => document.activeElement.matches('details.menu > summary'));
      if (menuFocused) break;
    }
    verify(menuFocused, 'menu summary cannot be reached by keyboard');
    if (menuFocused) {
      verify(await page.evaluate(() => { const s = getComputedStyle(document.activeElement); return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || s.boxShadow !== 'none'; }), 'keyboard focus has no visible outline or shadow');
      await page.keyboard.press('Enter');
      verify(await page.$eval('details.menu', (el) => el.open), 'Enter does not open the menu');
      const menuState = await page.$eval('details.menu nav', el => {
        const box = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        const last = el.querySelector('li.menu-repository a');
        const before = el.scrollTop;
        el.scrollTop = el.scrollHeight;
        const after = el.scrollTop;
        const lastBox = last.getBoundingClientRect();
        return {fits: box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight,
                wraps: [...el.querySelectorAll('a')].every(a => getComputedStyle(a).whiteSpace !== 'nowrap'),
                scrolls: after > before, lastVisible: lastBox.top >= box.top && lastBox.bottom <= box.bottom,
                final: last.textContent};
      });
      verify(menuState.fits && menuState.wraps && menuState.scrolls && menuState.lastVisible,
             'complete menu does not fit, wrap, scroll or expose its last link: ' + JSON.stringify(menuState));
      await page.keyboard.press('Escape');
      verify(await page.$eval('details.menu', (el) => !el.open), 'Escape does not close the menu');
    }
    await page.focus('.toc-mobile summary');
    await page.keyboard.press('Enter');
    verify(await page.$eval('.toc-mobile', (el) => el.open), 'keyboard cannot open lesson contents');
    await page.keyboard.press('Enter');
    verify(await page.$eval('.toc-mobile', (el) => !el.open), 'keyboard cannot close lesson contents');
    await page.goto(base + '/lessons.html', {waitUntil: 'domcontentloaded'});
    verify(await page.$$eval('.lesson-row', (els) => els.length === 10), 'index does not expose ten lessons');
    verify(await page.$$eval('.lesson-row .min', (els) => els.length === 10 && els.every(el => /estimated/.test(el.textContent))), 'index reading estimates are missing or unqualified');
    for (const name of ['agent-output-verification', 'agent-artifact-recovery', 'agent-contract-consistency']) {
      const response = await fetch(base + '/skills/' + name + '/SKILL.md');
      verify(response.ok && (await response.text()).includes('name: ' + name), 'raw skill download failed: ' + name);
    }
    await page.setJavaScriptEnabled(false);
    await page.goto(base + '/', {waitUntil: 'domcontentloaded'});
    verify(await page.$eval('.actions .primary', (el) => el.getBoundingClientRect().width > 0), 'primary action disappears without JavaScript');
    verify(await page.$$eval('.reveal-pending', (els) => els.length === 0), 'content is stranded without JavaScript');
    await page.setJavaScriptEnabled(true);
    await page.emulateMediaFeatures([{name: 'prefers-reduced-motion', value: 'reduce'}]);
    await page.goto(base + '/', {waitUntil: 'networkidle0'});
    verify(await page.$eval('.hero-loop', (svg) => svg.animationsPaused()), 'hero does not pause for reduced motion');
    verify(await page.evaluate(() => document.getAnimations().every(a => a.playState !== 'running')), 'CSS animation remains active under reduced motion');
    verify(errors.length === 0, 'page errors: ' + errors.join(' | '));
  } catch (error) {
    verify(false, error.message);
  } finally {
    await page.close();
  }
  return checks;
}

async function main() {
  const failures = [];
  let checks = 0;
  const server = await serve(ROOT);
  const port = server.address().port;
  let browser;
  try {
    browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    for (const pagePath of PAGES) {
      for (const vp of VIEWPORTS) {
        const page = await browser.newPage();
        const consoleErrors = [];
        const badResponses = [];
        page.on('console', (msg) => {
          if (msg.type() === 'error') consoleErrors.push(msg.text());
        });
        page.on('response', (res) => {
          if (res.status() >= 400) badResponses.push(res.status() + ' ' + res.url());
        });
        try {
          await page.setViewport({ width: vp.width, height: vp.height });
          await page.goto('http://127.0.0.1:' + port + '/' + pagePath, {
            waitUntil: 'networkidle0',
            timeout: 15000,
          });
          await page.evaluate(() => document.fonts ? document.fonts.ready : null);
        } catch (err) {
          failures.push(pagePath + ' @' + vp.width + ': navigation — ' + err.message);
          await page.close();
          continue;
        }

        checks++;
        const problems = await page.evaluate(inspectPage);
        for (const p of problems) failures.push(pagePath + ' @' + vp.width + ': ' + p);

        checks++;
        if (HUBS.includes(pagePath)) {
          const hub = await page.evaluate(countHubNext);
          if (!hub.present) {
            failures.push(pagePath + ' @' + vp.width + ': hub-next — no .hub-next element found');
          } else if (hub.links < 2) {
            failures.push(pagePath + ' @' + vp.width + ': hub-next — only ' + hub.links + ' link(s)');
          }
        }

        checks++;
        // Scroll capture: a vertical wheel over a horizontal region must still
        // move the page. Measured 0px on four regions before the per-axis fix.
        for (const sel of ['.lesson-list', '.track-row', '.table-scroll', '.reader pre']) {
          const box = await page.evaluate((s) => {
            const el = document.querySelector(s); if (!el) return null;
            document.documentElement.style.scrollBehavior = 'auto';
            const r = el.getBoundingClientRect(); window.scrollTo(0, Math.max(0, r.top + window.scrollY - 200));
            const q = el.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2, before: window.scrollY};
          }, sel);
          if (!box) continue;
          await page.mouse.move(box.x, box.y); await page.mouse.wheel({deltaY: 300});
          await new Promise((r) => setTimeout(r, 200));
          const after = await page.evaluate(() => window.scrollY);
          if (after - box.before < 50) failures.push(pagePath + ' @' + vp.width + ': scroll capture — ' + sel + ' swallows the vertical wheel (page moved ' + (after - box.before) + 'px)');
        }
        // Slop: the rules that break a model's defaults, as measurements. Taken
        // from gpt-taste's pre-flight and the owner's design language: these do
        // not judge taste, they prove the page did not fall into the standard
        // AI-page habits. Each failure names the rule and the measured value.
        const slop = await page.evaluate(() => {
          const out = [];
          const lines = (el) => { const r = document.createRange(); r.selectNodeContents(el); const tops = new Set(); for (const b of r.getClientRects()) tops.add(Math.round(b.top)); return tops.size; };
          const lineWidths = (el) => { const r = document.createRange(); r.selectNodeContents(el); const m = {}; for (const b of r.getClientRects()) { const k = Math.round(b.top); m[k] = (m[k] || 0) + b.width; } return Object.values(m); };
          // 1. Headlines: an h1 holds in three lines or fewer; its last line is not an orphan.
          for (const h of document.querySelectorAll('h1')) {
            const n = lines(h); if (n > 3) out.push('headline — h1 "' + h.textContent.trim().slice(0, 40) + '" wraps to ' + n + ' lines (max 3)');
            const w = lineWidths(h); if (w.length > 1 && w[w.length - 1] < 0.3 * w[0]) out.push('headline — h1 "' + h.textContent.trim().slice(0, 40) + '" ends in an orphan line (' + Math.round(w[w.length - 1]) + 'px of ' + Math.round(w[0]) + 'px)');
          }
          // 2. Headings are not clipped by their box.
          for (const h of document.querySelectorAll('h1, h2, h3')) if (h.scrollWidth > h.clientWidth + 1) out.push('headline — "' + h.textContent.trim().slice(0, 40) + '" is clipped horizontally');
          // 3. One figure per band, never the same figure in two adjacent bands (home page bands).
          const bands = [...document.querySelectorAll('main > section.band, main > header.opening')];
          const figureOf = (b) => { const el = b.querySelector('.ideas-row, .track-row, .tiles, .shelves, .timestamps, .pick, .ledger, .study, .tier'); if (!el) return null; return [...el.classList].filter((c) => !/^(is-|reveal)/.test(c)).sort().join('.'); };
          for (let i = 1; i < bands.length; i++) { const a = figureOf(bands[i - 1]), b = figureOf(bands[i]); if (a && b && a === b) out.push('composition — adjacent bands share the figure "' + a + '"'); }
          // 4. A band whose only drawing is its focal visual gives it a size that carries.
          for (const b of document.querySelectorAll('main > section')) { const svgs = [...b.querySelectorAll('svg')]; if (svgs.length === 1) { const w = svgs[0].getBoundingClientRect().width; if (w < 96) out.push('figure — the only drawing in #' + (b.id || b.className) + ' is ' + Math.round(w) + 'px wide (min 96)'); } }
          // 5. No enclosed empty grid cells: a bordered grid's last row is full, or the container draws no outline.
          // Measured by geometry, not by the computed track list: auto-fit grids report
          // tracks they have collapsed. An outlined empty exists only when the container
          // draws a border and its last row of items stops short of its right edge.
          for (const g of document.querySelectorAll('ul, ol')) { const cs = getComputedStyle(g); if (cs.display !== 'grid' || parseFloat(cs.borderLeftWidth) === 0 || parseFloat(cs.borderRightWidth) === 0) continue; const items = [...g.children]; if (items.length < 2) continue; const gr = g.getBoundingClientRect(); const bottoms = items.map((i) => Math.round(i.getBoundingClientRect().top)); const lastTop = Math.max(...bottoms); const lastRow = items.filter((i) => Math.round(i.getBoundingClientRect().top) === lastTop); const right = Math.max(...lastRow.map((i) => i.getBoundingClientRect().right)); const inner = gr.right - parseFloat(cs.borderRightWidth) - parseFloat(cs.paddingRight); if (inner - right > 8) out.push('grid — ' + (g.className || g.tagName) + ' outlines empty space after its last row (' + Math.round(inner - right) + 'px, ' + lastRow.length + ' item(s) in the row)'); }
          // 6. Buttons and primary actions are legible: text contrast against their own background.
          const lum = (c) => { const m = c.match(/\d+(\.\d+)?/g); if (!m) return null; const [r, g, b] = m.slice(0, 3).map((v) => { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
          for (const el of document.querySelectorAll('.btn, .row-controls button')) { const s = getComputedStyle(el); let bg = s.backgroundColor, p = el; while (bg === 'rgba(0, 0, 0, 0)' && p.parentElement) { p = p.parentElement; bg = getComputedStyle(p).backgroundColor; } const l1 = lum(s.color), l2 = lum(bg); if (l1 === null || l2 === null) continue; const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); if (ratio < 4.5) out.push('contrast — "' + el.textContent.trim().slice(0, 30) + '" text/background ' + ratio.toFixed(2) + ':1 (min 4.5)'); }
          // 8. No eyebrow above a heading: no small uppercase label as the element right before an h1/h2.
          for (const h of document.querySelectorAll('h1, h2')) { const prev = h.previousElementSibling; if (!prev) continue; const s = getComputedStyle(prev); const small = parseFloat(s.fontSize) <= 13 && (s.textTransform === 'uppercase' || /mono/i.test(s.fontFamily)); if (small && prev.textContent.trim().length > 0 && prev.textContent.trim().length < 40 && !prev.querySelector('a') && !/^\[\d+\]$/.test(prev.textContent.trim())) out.push('eyebrow — "' + prev.textContent.trim().slice(0, 30) + '" sits above "' + h.textContent.trim().slice(0, 30) + '"'); }
          // 9. Five seconds, from any viewpoint: no code spans, paths or hashes in front-facing copy.
          for (const el of document.querySelectorAll('.opening .lead, .band-head p, .section-head .lead, .tile .when, .tile .who, .ledger .what, .shelves .k, .shelf-head p, .hub-next .k, .study .claim, .study .findings li, .tier-lead')) {
            const txt = el.textContent.trim();
            if (el.querySelector('code')) out.push('jargon — code span in front-facing copy: "' + txt.slice(0, 50) + '"');
            else if (/\b[0-9a-f]{12,40}\b/.test(txt)) out.push('jargon — revision hash in front-facing copy: "' + txt.slice(0, 50) + '"');
            else if (/\b[\w-]+\/[\w.-]+\.(?:py|md|ts|js|json|yaml|yml)\b/.test(txt)) out.push('jargon — file path in front-facing copy: "' + txt.slice(0, 50) + '"');
          }
          // 10. A band's seam does not run over its own content. The dithered seam is
          // drawn by .band::after at the foot of the band, so a band whose padding is
          // tighter than the seam puts the seam on top of whatever ends the band - the
          // row controls on the guides track did exactly that.
          for (const band of document.querySelectorAll('.band')) {
            const seam = getComputedStyle(band, '::after');
            if (seam.content === 'none' || seam.display === 'none') continue;
            const seamH = parseFloat(seam.height); if (!seamH) continue;
            const seamTop = band.getBoundingClientRect().bottom - seamH;
            for (const el of band.querySelectorAll('a, button, p, h2, h3, li')) {
              const r = el.getBoundingClientRect();
              if (r.height === 0 || r.width === 0) continue;
              if (r.bottom > seamTop + 1 && r.top < band.getBoundingClientRect().bottom) {
                out.push('seam — the band seam runs over "' + (el.textContent.trim().slice(0, 30) || el.tagName) + '" in .' + band.className.split(' ').join('.'));
                break;
              }
            }
          }
          // 7. No emoji anywhere in the rendered text.
          if (/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(document.body.innerText)) out.push('emoji — rendered text contains an emoji');
          // 8. Text inside a drawing is measured at the size the reader gets, not the
          // size it was authored at. An inline SVG carries its own coordinate system, so
          // a caption set to 12.5 "px" inside a 1040-wide viewBox drawn 593px wide lands
          // at 7.1px on the page. Twice this check's threshold was missed by raising the
          // authored number and never converting it: the figure's scale is the whole bug.
          // Words must clear 10px; a single glyph (a prompt chevron, an arrow) may be
          // smaller because nobody reads it as a word.
          for (const svg of document.querySelectorAll('svg[viewBox]')) {
            const vb = svg.getAttribute('viewBox').split(/[ ,]+/).map(Number);
            const box = svg.getBoundingClientRect();
            if (!vb[2] || !box.width) continue;
            const scale = box.width / vb[2];
            for (const t of svg.querySelectorAll('text')) {
              const word = t.textContent.trim();
              if (word.length < 2 || getComputedStyle(t).display === 'none') continue;
              const px = parseFloat(getComputedStyle(t).fontSize) * scale;
              if (px < 10) out.push('figure text — "' + word.slice(0, 24) + '" renders at ' + px.toFixed(1) + 'px (min 10); the drawing is scaled to ' + scale.toFixed(2));
            }
          }
          return out;
        });
        for (const s of slop) failures.push(pagePath + ' @' + vp.width + ': slop — ' + s);
        // Reveal: after scrolling the whole page, nothing may remain hidden.
        const stuck = await page.evaluate(async () => {
          // The site scrolls smoothly; a harness must not depend on where an
          // animation happens to be when it retargets. Scroll instantly, in
          // half-viewport steps so every element is fully inside the observer's
          // root at some stop, and give the observer a frame at each.
          document.documentElement.style.scrollBehavior = 'auto';
          const step = Math.max(1, Math.floor(window.innerHeight / 2));
          const max = document.documentElement.scrollHeight;
          for (let y = 0; y <= max; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
          }
          await new Promise((r) => setTimeout(r, 700));
          const left = Array.from(document.querySelectorAll('.reveal-pending'));
          return left.slice(0, 3).map((el) => el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).trim().split(/\s+/).join('.') : ''))
            .concat(left.length > 3 ? ['+' + (left.length - 3) + ' more'] : []);
        });
        if (stuck.length) {
          failures.push(pagePath + ' @' + vp.width + ': reveal — ' + stuck.length + ' element(s) never revealed: ' + stuck.join(', '));
        }
        if (consoleErrors.length) {
          failures.push(pagePath + ' @' + vp.width + ': console — ' + consoleErrors.join(' | '));
        }

        checks++;
        if (badResponses.length) {
          failures.push(pagePath + ' @' + vp.width + ': failed request — ' + badResponses.join(' | '));
        }

        await page.close();
      }
    }
    checks += await checkLessonJourney(browser, 'http://127.0.0.1:' + port, failures);
  } finally {
    if (browser) await browser.close().catch(() => {});
    server.close();
  }

  if (failures.length) {
    for (const f of failures) console.log('FAIL ' + f);
  }
  const status = failures.length === 0 ? 'PASS' : 'FAIL';
  console.log(
    status + ': ' + PAGES.length + ' pages x ' + VIEWPORTS.length + ' viewports, ' +
      checks + ' rendered checks, ' + failures.length + ' failure(s)'
  );
  process.exit(failures.length ? 1 : 0);
}

main().catch((err) => {
  console.error('rendered check crashed: ' + (err && err.stack || err));
  process.exit(1);
});
